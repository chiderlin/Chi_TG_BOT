import logging 
from flask import Flask
from flask import request
from tpsf_package.tools.db import PyODBCHandler
from tpsf_package.tools.db.configs import QA_Sys_DB_CONFIG_28, DBCONFIG_DEV

app = Flask(__name__) 
app.config["DEBUG"] = True 

logging.basicConfig(level=logging.DEBUG) # DEBUG, INFO, WARNING, ERROR, CRITICAL 


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


@app.route("/",methods = ["GET"])
def home():
    return "Please insert your info"

@app.route("/api/tg/msg", methods = ["GET"])
def send_msg():
    logging.info(request.args)

    if 'ID' not in request.args:
        return {"Error": "Please insert ID & context args at the same time"}
    if 'context' not in request.args:
        return {"Error": "Please insert ID & context args at the same time"}
    
    ID = request.args["ID"]
    context = request.args["context"]
    id_num, _ = query_Msgid()
    if ID in id_num:
        if context != "":
            if len(context) >= 1000:
                context = context[0:1000]
            # logging.info(ID)
            # logging.info(context)
            sqlstr = "insert into MessagePush (Context,SourceFrom) values ('{}', '{}')".format(context, ID)

            try: 
                db.exec(sqlstr)
                logging.info("成功")
            except Exception as e: #記錄錯誤訊息(所有ERROR)
                logging.error(e)                
                return {"Error": f"{e}"}
            
            chatid, groupname = return_msg_type(ID)
            return {"Status": "200","SourceFrom": f"{ID}","ChatId":f"{chatid}","GroupName":f"{groupname}"}
        else:
            return {"Error": "Please insert ID & context args at the same time"}
    elif ID not in id_num:
        return {"Error": "Please insert current MsgID"}

@app.route("/api/tg/sendfile", methods=["GET"])
def send_file():
    if 'ID' not in request.args:
        return {"Error": "Please insert ID & File Path at the same time"}
    
    if "path" not in request.args:
        return {
            "Error": "Please insert ID & File Path at the same time", 
            "PathExample": "C:/User/filename.txt", 
            }

    ID = request.args["ID"]
    path = request.args["path"]
    id_num, _ = query_Msgid()
    if ID in id_num:
        if path != "":
            if len(path) >= 1000:
                return {"Error": "insert current path"}
            else:
                sqlstr = "insert into MessagePush (FilePath,SourceFrom) values ('{}', '{}')".format(path, ID)

                try: 
                    db.exec(sqlstr)
                    logging.info("成功")
                except Exception as e: #記錄錯誤訊息(所有ERROR)
                    logging.error(e)                
                    return {"Error": f"{e}"}

            chatid, groupname = return_msg_type(ID)
            return {
                    "Status": "200", 
                    "SourceFrom": f"{ID}", 
                    "ChatId": f"{chatid}", 
                    "GroupName": f"{groupname}", 
                    "successed": f"You send {path}",         
                    }
        else:
            return {"Error": "insert file location."}

    elif ID not in id_num:
        return {"Error": "Please insert current MsgID"}

@app.route("/api/tg/sendphoto", methods=["GET"])    
def send_photo():
    if 'ID' not in request.args:
        return {"Error": "Please insert ID & Photo Path at the same time"}
    
    if "path" not in request.args:
        return {
            "Error": "Please insert ID & Photo Path at the same time", 
            "PathExample": "C:/User/filename.jpg", 
            }

    ID = request.args["ID"]
    path = request.args["path"]
    id_num, _ = query_Msgid()
    if ID in id_num:
        if path != "":
            if len(path) >= 1000:
                return {"Error": "insert current path"}
            else:
                sqlstr = "insert into MessagePush (PhotoPath,SourceFrom) values ('{}', '{}')".format(path, ID)

                try: 
                    db.exec(sqlstr)
                    logging.info("成功")
                except Exception as e: #記錄錯誤訊息(所有ERROR)
                    logging.error(e)                
                    return {"Error": f"{e}"}

            chatid, groupname = return_msg_type(ID)
            return {
                    "Status": "200", 
                    "SourceFrom": f"{ID}", 
                    "ChatId": f"{chatid}", 
                    "GroupName": f"{groupname}", 
                    "successed": f"You send {path}",         
                    }
        else:
            return {"Error": "insert file location."}

    elif ID not in id_num:
        return {"Error": "Please insert current MsgID"}


def query_Msgid():
    sqlstr = "select MessageID,ChatId,GroupName from MessageType"
    sql = "select MessageID from MessageType"
    rows = db.query(sqlstr) #for 顯示資訊
    id_ = db.query(sql) #for 輸入資料
    id_num = []
    # id_num = ["110", "111", "112", "113"]
    for row in id_:
        id_num.append(row.MessageID)
    return id_num, rows


def return_msg_type(ID):
        _, rows = query_Msgid()
        for i in rows:
            if i[0] == ID:
                chatid = i[1]
                groupname = i[2]
        return chatid, groupname



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7002)

db.close()

