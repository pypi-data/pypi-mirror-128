import click
import twitlim.helpers as helpers
import os

from click_option_group import optgroup
from datetime import datetime
from time import sleep as pause_execution


DEFAULT_CONFIG_FILE = os.path.expanduser("~") + "/.config/twitlim.ini"

LOG, QUIET = False, False


def _echo(msg, **kwargs):
    if not QUIET:
        click.echo(msg, **kwargs)
    if LOG:
        kwargs["file"] = LOG
        click.echo(msg, **kwargs)


@click.command()
@click.version_option(helpers.read_version())
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Be quiet and only output errors.",
)
@click.option(
    "--delete",
    is_flag=True,
    default=False,
    help=(
        "Because deleting tweets is very final, you need to set this option to actually delete tweets. By default this"
        " script only does a dry-run."
    ),
)
@click.option(
    "--config",
    metavar="CONFIG_FILE_PATH",
    type=click.Path(dir_okay=False),
    default=DEFAULT_CONFIG_FILE,
    callback=helpers.configure,
    is_eager=True,
    expose_value=False,
    show_default=True,
    help=(
        "Use your own config file to make running twitlim easier. By default twitlim looks for default, but you can"
        " specify your own config file, which can be usefull if you want to manage multiple Twitter accounts."
    ),
)
@click.option(
    "--log",
    metavar="LOG_FILE_PATH",
    type=click.File("a"),
    help=(
        "If you give a path to a log file, twitlim will print anything that is would print to the terminal to the log"
        " file too. This also works if the output is set to quiet."
    ),
)
@optgroup.group(
    "Twitter Configuration",
    help=(
        "Use the following filters to limit the tweets that will be deleted. PLEASE NOTE that the filters are applied"
        " in the same order as they are listed below."
    ),
)
@optgroup.option("--consumer-key", metavar="KEY", required=True)
@optgroup.option("--consumer-secret", metavar="SECRET", required=True)
@optgroup.option("--access-token", metavar="SECRET", required=True)
@optgroup.option("--access-token-secret", metavar="SECRET", required=True)
@optgroup.group(
    "Filter options",
    help=(
        "Use the following filters to limit the tweets that will be deleted. PLEASE NOTE that the filters are applied"
        " in the same order as they are listed below."
    ),
)
@optgroup.option(
    "--count",
    metavar="INT",
    type=click.INT,
    default=100,
    help=(
        "You can get up to 200 tweets per api call. By default twitlim requests 100 tweets at a time, but you can"
        " change this amount by setting COUNT."
    ),
)
@optgroup.option(
    "--include",
    multiple=True,
    help=(
        'Id of a tweet to include, you can also use "replies", "retweets", or "favorites" to include all replies, all'
        " retweets and/or all favorite tweets. You can set one id or category at a time but you can set this option"
        " times."
    ),
)
@optgroup.option(
    "--exclude",
    multiple=True,
    help='Ids of tweets to exclude, you can use "replies" "retweets" or "favorites", similar to include.',
)
@optgroup.option(
    "--skip-no",
    type=click.INT,
    metavar="INT",
    help="Do not delete the first NUMBER of tweets, but skip them.",
)
@optgroup.option(
    "--min-age",
    type=click.INT,
    metavar="NO_OF_DAYS",
    help="Only delete tweets that are older than a minimal number of days.",
)
@optgroup.option(
    "--before-date",
    type=click.DateTime("%Y-%m-%d"),
    metavar="YYYY-MM-DD",
    help="Only delete tweets posted before this date. Use YYYY-MM-DD as format.",
)
@optgroup.option(
    "--after-date",
    type=click.DateTime("%Y-%m-%d"),
    metavar="YYYY-MM-DD",
    help="Only delete tweets posted after this date. Use YYYY-MM-DD as format.",
)
@optgroup.option(
    "--max-no",
    type=click.INT,
    metavar="INT",
    help="Limit the maximum number of tweets to delete. The newest tweets are skipped, the oldest are deleted.",
)
@optgroup.group(
    "Backup options",
    help="You can backup your tweets to a SQLite database, but to do so you'll need to set the appropriate options.",
)
@optgroup.option(
    "--database-file",
    metavar="DB_FILE_PATH",
    type=click.Path(dir_okay=False, writable=True, exists=False, resolve_path=True),
    help=(
        "This is the only option that you need to set to make backups work. Just give a full path to a database file."
        " The file doesn't need to exist, but the path needs to be writable."
    ),
)
@optgroup.option(
    "--identifier",
    metavar="ID",
    type=click.STRING,
    help=(
        "If you want to back up multiple twitter accounts in the same database file, you can use the identifier to"
        " connect your tweets to a specific account."
    ),
)
@optgroup.option(
    "--update_profile",
    metavar="PROFILE_TEXT",
    type=click.STRING,
    help=(
        "This is option that becomes available if you use a backup database. You can update your profile to set the"
        " number of tweets you have deleted. You can create your own text and use the %no variable which will be"
        " replaced with the number of tweets you have deleted. This text is appended to your original profile"
        " description (or replaced if it's already there). Make sure the total amount of characters is less than 160"
        " characters. E.g.: (%no deleted tweets)"
    ),
)
def twitlim(*args, **opts):
    global LOG, QUIET
    # CHECKING OPTIONS and CONFIGURATION
    # Can we read the config file.

    QUIET = opts["quiet"]
    LOG = opts["log"]

    # If we want to backup, we need to check if the configuration is correct.
    if opts["database_file"]:
        connection, cursor = helpers.init_database(opts)

    # # Now let's get to work.
    api = helpers.init_api(opts)
    tweets = helpers.fetch_tweets(api, opts)
    if opts["database_file"] and connection and cursor:
        helpers.backup_tweets(connection, cursor, tweets, opts["identifier"])

    # Now filter out the tweets that you want to keep.
    tweets = helpers.filter_tweets(tweets, opts)

    # # Now let's show the Tweets, that we've found.
    if len(tweets) > 0 and opts["delete"]:
        _echo("THE FOLLOWING TWEETS WILL BE DELETED!")
    elif len(tweets) > 0:
        _echo("The following Tweets were selected.")
        _echo("Use the -d or --delete, to actually delete them.")
    else:
        _echo("No tweets matched your criteria and NOTHING will be deleted.")

    for i, t in enumerate(tweets, start=1):
        summary = []
        characteristics = {
            "favorited": "FAVORITE",
            "retweeted": "RETWEET",
            "in_reply_to": "REPLY",
        }
        for c in characteristics:
            if t[c]:
                summary.append(characteristics[c])

        _echo("")
        _echo("{:03d}: {:s}".format(i, t["id_str"]))
        _echo(t["text"])
        _echo("# posted at:  {:s}".format(t["created_at"].strftime("%Y-%m-%d, %H:%M:%S")))
        if summary:
            _echo(", ".join(summary))

        if opts["delete"]:
            if api.destroy_status(id=int(t["id_str"])):
                # Pause execution.
                # This prevents hitting the API limit too soon.
                pause_execution(0.25)
                # If you chose to backup, we mark the deleted tweets as
                # deleted.
                if opts["database_file"] and cursor:
                    cursor.execute("UPDATE tweets SET deleted=1 WHERE id_str = ?", (t["id_str"],))
                    connection.commit()
                _echo("# DELETED!")

    if opts["database_file"]:
        cursor.execute("SELECT id_str FROM tweets WHERE deleted = 1")
        no_deleted = len(cursor.fetchall())
        _echo(f"So far you have deleted {no_deleted} tweets.")
        if opts["update_profile"] and opts["delete"]:
            profile = helpers.update_profile(opts, api, no_deleted)
            if profile:
                _echo(f"Profile description updated to: \n{profile}\n")
            else:
                _echo("Profile NOT UPDATED. The length of your description was too long (max 160).")

    # See what's the users api limit.
    rate = api.rate_limit_status()
    limits = rate.get("resources", {}).get("application", {}).get("/application/rate_limit_status", False)
    if limits:
        reset_time = datetime.fromtimestamp(limits["reset"])
        _echo(
            "\nYou have {:d} api calls left. At {:s} the limit will be reset to {:d}.".format(
                limits["remaining"], reset_time.strftime("%H:%M"), limits["limit"]
            )
        )
        _echo("Deleting 1 tweet equals 1 api call.")

    # Cleanup
    if opts["database_file"] and connection:
        connection.commit()
        cursor.close()
    if LOG:
        LOG.close()
