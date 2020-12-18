from datetime import datetime, timedelta
import time
import logging
import json
import requests
from telegram import Bot 
from tpsf_package.tools.db import PyODBCHandler
from tpsf_package.tools.db.configs import QA_Sys_DB_CONFIG_28, DBCONFIG_DEV



logging.basicConfig(level=logging.DEBUG)

# 導入環境檔案ENV
try:
    from ENV import ENV
except ModuleNotFoundError:
    ENV = "DEV"

if ENV == "PROD":
    """
    db Production 
    """
    db = PyODBCHandler(host=QA_Sys_DB_CONFIG_28["HOST"],
                    db="QASys",
                    uid=QA_Sys_DB_CONFIG_28["UID"],
                    pwd=QA_Sys_DB_CONFIG_28["PWD"])
elif ENV == "DEV":
    """
    db development
    """
    db = PyODBCHandler(host=DBCONFIG_DEV["HOST"],
                    db="QASys",
                    uid=DBCONFIG_DEV["UID"],
                    pwd=DBCONFIG_DEV["PWD"])

def TelegramBotMessage(msg=None, photopath=None, filepath=None, chatid="-366226628"):
    with open("/workspace/setting.json",mode="r",encoding="utf-8") as f:
        config = json.load(f)
    print(config)
    bot = Bot(token=config["token"])
    if msg:
        bot.sendMessage(chatid,text=msg)
        # url = f"https://api.telegram.org/bot{config['token']}/sendMessage?"
        # params = {"chat_id": chatid, "text": msg}
        # requests.get(url, params = params)

    if filepath: 
        bot.send_document(chatid,document=open(file=filepath,mode="rb"),timeout=60)
        # requests.get(f"https://api.telegram.org/bot{token}/sendDocument?chat_id={chatid}&document={file_URL}")

    if photopath:
        bot.send_photo(chatid,photo=open(file=photopath,mode="rb"),timeout=60)
        # requests.get(f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatid}&photo={photo_URL}")
  
def UpdatedPublishedDate(_id):
    sql = "UPDATE MessagePush SET PushedDate = \'{}\' WHERE id=\'{}\'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),_id)
    db.exec(sql)


while True: # for testing time being.
    date = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    stat = "SELECT a.id, a.Context, a.PushedDate, b.ChatId FROM MessagePush a join MessageType b on a.SourceFrom=b.MessageID WHERE a.Context is not NULL and a.PushedDate IS NULL AND a.CreatedDate > \'{}\'".format(date)
    res = db.query(stat)
    if res:
        for i in res:
            # [0]id, [1]Context, [2]PushedDate, [3]ChatId
            msg = i[1] # only send [1]Context
            logging.debug(msg)
            TelegramBotMessage(msg=msg, chatid=i[3])
            UpdatedPublishedDate(i[0])
            logging.debug("msg done update PushedDate..")

##
    stat = "SELECT a.id, a.FilePath, a.PushedDate, b.ChatId FROM MessagePush a join MessageType b on a.SourceFrom=b.MessageID WHERE a.FilePath is not NULL and a.PushedDate IS NULL AND a.CreatedDate > \'{}\'".format(date)
    res = db.query(stat)
    if res:
        for i in res:
            # [0]id, [1]FilePath, [2]PushedDate, [3]ChatId
            filepath = i[1] # only send [1]FilePath
            logging.debug(filepath)
            TelegramBotMessage(filepath=filepath, chatid=i[3])
            UpdatedPublishedDate(i[0])
            logging.debug("filepath done update PushedDate..")

##
    stat = "SELECT a.id, a.PhotoPath, a.PushedDate, b.ChatId FROM MessagePush a join MessageType b on a.SourceFrom=b.MessageID WHERE a.PhotoPath is not NULL and a.PushedDate IS NULL AND a.CreatedDate > \'{}\'".format(date)
    res = db.query(stat)
    if res:
        for i in res:
            # [0]id, [1]PhotoPath, [2]PushedDate, [3]ChatId
            photopath = i[1] # only send [1]PhotoPath
            logging.debug(photopath)
            TelegramBotMessage(photopath=photopath, chatid=i[3])
            UpdatedPublishedDate(i[0])
            logging.debug("photopath done update PushedDate..")

    time.sleep(10)


db.close()


# TelegramBotMessage(msg="hello from sys")
