import click
import os
import pickle
import re
import sqlite3
import time
import tweepy

from configparser import RawConfigParser
from datetime import datetime, timedelta, timezone


def _get_source_url(t):
    try:
        return t.source_url
    except AttributeError:
        return ""


def backup_tweets(connection, cursor, tweets, identifier):
    for t in tweets:
        cursor.execute("SELECT id_str FROM tweets WHERE id_str=?", (t["id_str"],))
        values = [
            identifier,
            t["text"],
            t["source"],
            t["source_url"],
            t["favorited"],
            t["retweeted"],
            t["retweet_count"],
            t["in_reply_to"],
            t["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            memoryview(pickle.dumps(t["entities"])),
        ]
        if len(cursor.fetchall()) == 0:
            values.insert(0, t["id_str"])
            cursor.execute(
                """
                INSERT INTO tweets (
                    id_str,
                    identifier,
                    text, source,
                    source_url,
                    favorited,
                    retweeted,
                    retweet_count,
                    in_reply_to,
                    created_at,
                    pickled_entities
                )
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?)
            """,
                values,
            )
        else:
            values.append(t["id_str"])
            cursor.execute(
                """
                UPDATE tweets SET
                identifier = ?, text = ?, source = ? , source_url = ?,
                favorited = ?, retweeted = ?, retweet_count = ?,
                in_reply_to = ?, created_at = ?, pickled_entities = ?
                WHERE id_str = ?;
            """,
                values,
            )
        connection.commit()


def configure(ctx, param, filename):
    cfg = RawConfigParser()
    cfg.read(filename)
    try:
        options = dict(cfg["options"])
    except KeyError:
        options = {}
    for opt in ["exclude", "include"]:
        if opt in options:
            options[opt] = re.split(r"\s*,\s*", options[opt])
    ctx.default_map = options


def fetch_tweets(api, opts):
    raw_tweets = api.user_timeline(
        count=opts["count"],
        include_rts=True,
        trim_user=True,
    )
    tweets = []
    for t in raw_tweets:
        tweets.append(
            {
                "id_str": t.id_str,
                "text": t.text,
                "source": t.source,
                "source_url": _get_source_url(t),
                "favorited": t.favorited,
                "retweeted": t.retweeted,
                "retweet_count": t.retweet_count,
                "in_reply_to": t.in_reply_to_user_id_str,
                "created_at": t.created_at,
                "entities": t.entities,
            }
        )
    return tweets


def filter_tweets(tweets, opts):
    if opts["include"]:
        tweets = list(
            filter(
                lambda x: (x["id_str"] in opts["include"])
                or (x["in_reply_to"] and "replies" in opts["include"])
                or (x["retweeted"] and "retweets" in opts["include"])
                or (x["favorited"] and "favorites" in opts["include"]),
                tweets,
            )
        )
    if opts["exclude"]:
        tweets = list(
            filter(
                lambda x: not (x["id_str"] in opts["exclude"])
                and not (x["in_reply_to"] and "replies" in opts["exclude"])
                and not (x["retweeted"] and "retweets" in opts["exclude"])
                and not (x["favorited"] and "favorites" in opts["exclude"]),
                tweets,
            )
        )
    if opts["skip_no"]:
        if len(tweets) > int(opts["skip_no"]):
            tweets = tweets[int(opts["skip_no"]) :]
        else:
            tweets = []
    if opts["min_age"]:
        today = datetime.fromtimestamp(time.time(), timezone.utc)
        min_date = datetime(today.year, today.month, today.day, tzinfo=timezone.utc) - timedelta(int(opts["min_age"]))
        tweets = list(filter(lambda x: x["created_at"] < min_date, tweets))
    if opts["before_date"]:
        tweets = list(filter(lambda x: x["created_at"] < opts["before_date"], tweets))
    if opts["after_date"]:
        tweets = list(filter(lambda x: x["created_at"] > opts["after_date"], tweets))
    if opts["max_no"]:
        if len(tweets) > int(opts["max_no"]):
            tweets = tweets[-int(opts["max_no"]) :]
        else:
            tweets = []
    return tweets


def init_api(opts):
    auth = tweepy.OAuthHandler(opts["consumer_key"], opts["consumer_secret"])
    auth.set_access_token(opts["access_token"], opts["access_token_secret"])
    return tweepy.API(auth)


def init_database(opts):
    try:
        connection = sqlite3.connect(opts["database_file"])
    except Exception as e:
        click.echo(f"Tried opening database file {opts['database_file']}", err=True)
        click.echo(f"All options: \n{opts}\n\n", err=True)
        raise e
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS "tweets" (
            "id_str" varchar(255) NOT NULL PRIMARY KEY,
            "identifier" varchar(255),
            "text" varchar(255) NOT NULL,
            "source" varchar(255) NOT NULL,
            "source_url" varchar(255),
            "favorited" bool NOT NULL,
            "retweeted" bool NOT NULL,
            "retweet_count" integer NOT NULL,
            "in_reply_to" varchar(100),
            "created_at" datetime NOT NULL,
            "pickled_entities" text NOT NULL,
            "deleted" bool NOT NULL DEFAULT 0
        );
    """
    )
    return connection, cursor


def read_version():
    with open(os.path.join(os.path.dirname(__file__), "VERSION")) as file:
        return file.read().strip()


def update_profile(opts, api, no_deleted):
    settings = api.get_settings()
    me = api.get_user(screen_name=settings["screen_name"])
    text_parts = opts["update_profile"].split("%no")
    replace_with = str(no_deleted).join(text_parts)
    search_for = r"\d+".join([re.escape(t) for t in text_parts])
    profile = re.sub(search_for, replace_with, me.description)
    if not profile:
        profile = replace_with
    elif not profile[-len(replace_with) :] == replace_with:
        profile = profile + " " + replace_with
    if len(profile) > 160:
        return None
    if profile and api.update_profile(description=profile):
        return profile
    return None
