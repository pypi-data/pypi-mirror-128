# pixiv-save
save pixiv user illusts

```shell
usage: pixivsave.py [-h] [-u USERID] [-t TOKEN] [-p PROXY] [-d DOWNLOADTO] [-s] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -u USERID, --userid USERID
                        pixiv userid which you want to download pictures from.
  -t TOKEN, --token TOKEN
                        your pixiv refresh token.once you run this program,it will be saved in config.json file.you dont need to input it last time.
  -p PROXY, --proxy PROXY
                        proxy like 127.0.0.1:7890.once you run this program,it will be saved in config.json file.you dont need to input it last time.
  -d DOWNLOADTO, --downloadto DOWNLOADTO
                        download path.
  -s, --separate        if make directory for every illusts.
  -c, --config          load config.json file
```