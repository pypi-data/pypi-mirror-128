# Twitlim

Twitlim is a tool for deleting tweets from your Twitter stream based upon a set of filters.

With a simple cron job you can make it run at specific intervals. This way you can limit the amount of tweets that remain online.

## Why I made it.

Twitter is for short messages. It excels for praising and ranting and sharing your feelings on something or someone. It shows your current status and their question is always: _What's happening?_ It's about the now, yet your tweets remain online forever and your feelings or thoughts of a year ago might not be the same today, yet they remain online as if they are just as valid today. I wanted to tackle this discrepancy and that's why I made Twitlim.


## Installation

Just use pip. 

```
pip install -u twitlim
```


## Usage options

Type `twitlim -h` for help and you can see some information there. Basically there are **two ways** to configure the use. Via the command line or via a config file. Keep in mind: **Command line options overrule configuration file options.**

## The config file

You can put any option that you set on the command line also in the config file (except for the --config parameter). This is an example:

```
[options]
consumer_key = adae0eFwtEF002lds0gdsA
consumer_secret = adalkjWwe47583aafssxZXCXAfafodLKDadddsdlklkSDSEDsc
access_token = 3907823242-aDSDlakwsdSEO40320sDASa323wssasadaf2242
access_token_secret = adalkjWwe47583aafssxZXCXAfafodLKDadddsdlklk
database_file = /home/username/twitlim.sqlite
exclude = favorites,34093092840982
log = /home/username/twitlim.log
```

Please note:

- You should always use full paths. The not use the `~` (e.g. `~/twitlim.log`) in the config file as expansion of the `~` is done by shell and not by the script.
- For the `include` and `exclude` options you can make a list by comma-separating the values. See the example above.
- The default location for the config file is at `~/.config/twitlim.ini`. No need to provide the `--config` option if your file just lives there.

## Authenticating Twitter API.

The steps to authenticate your version of twitlim are pretty straightforward and easy.

1. Go to: [https://dev.twitter.com/user/login]() and sign in with your username and password.
2. After logging in, hover over your username in the top right corner and a submenu will appear. In the submenu click _My applications_.
3. Click the button _Create a new application_.
4. In the form that appears fill in `twitlim` as _Name_, `Twitter stream limiter` as _Description_ and `http://example.com` or something else as _Website_. Agree to the terms, fill in the Captcha and click the button _Create your Twitter application_.
5. You will now see a details page for your application. Click on the _Settings_ tab.
6. Under _Application Type_ change the access type to: _Read, Write and Access direct messages_. Then click _Update this Twitter application's settings_.
7. Click on the _Details_ tab.
8. Under _Your access token_ click _Create my access token_.
9. You can now copy paste the _Consumer key_, _Consumer secret_, _Access token_ and _Access token secret_ to your config file or to the appropriate config options on the command line.

## License

This code is available under the [MIT License](./LICENSE.txt).
