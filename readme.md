# parse-t-me-message

Parse Telegram messages in public groups through t.me links

## Build

```bash
pip install -r requirements.txt
```

## Help
```bash
usage: main.py [-h] -g GROUP_NAME -s START_ID -c COUNT

Parse Telegram messages in public groups through t.me links

options:
  -h, --help            show this help message and exit
  -g GROUP_NAME, --group-name GROUP_NAME
                        short link of a public group withow @
  -s START_ID, --start-id START_ID
                        start message id
  -c COUNT, --count COUNT
                        message count
```
