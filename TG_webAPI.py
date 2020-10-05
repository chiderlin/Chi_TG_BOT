from flask import Flask
from flask import request
from config import *
import logging 
app = Flask(__name__) 
app.config["DEBUG"] = True 

logging.basicConfig(level=logging.ERROR) # DEBUG, INFO, WARNING, ERROR, CRITICAL 




@app.route("/", methods = ["GET"])
def home():
    return "Please insert your info"

@app.route("/api/tg", methods = ["GET"])

def args_id():
    # id_num = ["110", "111", "112", "113"]
    sqlstr = "select MessageID from MessageType"
    cursor.execute(sqlstr)
    rows = cursor.fetchall()
    id_num = []
    for row in rows:
        # print(row.MessageID)
        id_num.append(row.MessageID)
   
    logging.info(request.args)

    if 'ID' not in request.args:
        return {"Error": "Please insert ID & context args at the same time"}
    if 'context' not in request.args:
        return {"Error": "Please insert ID & context args at the same time"}
    
    ID = request.args["ID"]
    context = request.args["context"]

    if ID in id_num:
        if context != "":
            if len(context) >= 1000:
                context = context[0:1000]
            logging.info(ID)
            logging.info(context)
            sqlstr = "insert into MessagePush (Context,SourceFrom) values ('{}', '{}')".format(context, ID)
            try: 
                cursor.execute(sqlstr)
                conn.commit()
                logging.info("成功")
            except Exception as e: #記錄錯誤訊息(所有ERROR)
                logging.error(e)
                
                return {"Error": f"{e}"}
            return {"Status": "200"}
        else:
            return {"Error": "Please insert ID & context args at the same time"}
    elif ID not in id_num:
        return {"Error": "Please insert current MsgID"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7001)

conn.close()

