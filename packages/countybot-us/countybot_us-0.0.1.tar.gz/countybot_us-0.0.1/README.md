# US Counties Bot

A friendly Twitter bot built with [Munibot](https://github.com/amercader/munibot) that tweets imagery of US Counties and equivalent administrative units.

## Install and setup

Install it with pip:

```
pip install countybot-us
```

And follow the instructions on [Munibot's documentation](https://github.com/amercader/munibot#usage) regarding configuration and setup.

This particular bot requires:

* The backend SQLite database, which you can download from this repo (`data` folder)


This should be referenced in the `[profile:us]` section of your `munibot.ini` file:

```
[profile:us]
twitter_key=CHANGE_ME
twitter_secret=CHANGE_ME
db_path=/path/to/data/countybot_us.sqlite
```

## License

[MIT](/amercader/munibot/blob/master/LICENSE.txt)
