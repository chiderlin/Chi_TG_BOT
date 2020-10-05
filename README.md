
## 使用說明

| Method | path | 參數 | 類型 | 說明 |
| ------ | ------ | ------ | ------ |------ |
| GET | /api/tg | *ID | str |tg群組MessageID |
| GET | /api/tg | *context | str | 要推播的內容 (輸入內容不可超過1000字元) |



## Get Start 

Base URL: https://10.80.1.18



## 系統訊息顯示說明


1.  {"Status": "200"}  : 傳送成功
2.  {"Error": "Please insert current MsgID"} : 錯誤ID或者目前資料庫無此ID
3.  {"Error": "Please insert ID & context args at the same time"} : ID和context參數要同時使用