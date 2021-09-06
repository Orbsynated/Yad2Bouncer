# Yad2 Bouncer

A script for bouncing Yad2 ads. The script runs in 2 ways:

* Windows mode - runs with a normal chrome instance
* Linux mode - runs with a headless chrome instance (without GUI)

# Usage

In order to run the script execute for next command or use docker(recommended):

## Linux

```
make EMAIL=<username> PASSWORD=<password> FLAGS=<flags> run
```

## Windows

```
python3 src\main.py [...flags] <username> <password>
```

# Flags

| Short flag  | Long Flag | Description | Required |
| ----------  | --------- | ----------- | -------- |
| -d  | -driver  | Chrome driver path | True |
| -s  | --schedule  | Whether to bounce automaticlly every 4 hours and 5 minutes | False |
| -v | --verbosity | Verbosity level for debugging | False |
| No Short Flag | --logs-path | Log file Path | False |

# Requirements

* Python 3
* Pip
* Python packages
    + Run `pip3 install -r requirements.txt`
* Chrome driver
    + For linux - run `make chromedrive`
    + For Windows - Download at https://sites.google.com/a/chromium.org/chromedriver/home.

## Credits

This is a fork of [yoavravid's Yad2Bouncer](https://github.com/yoavravid/Yad2Bouncer) with added feature, sanity checks
and fixes.