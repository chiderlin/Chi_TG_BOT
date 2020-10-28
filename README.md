
## 使用說明

### 推播文字
| Method | path | 參數 | 類型 | 說明 |
| ------ | ------ | ------ | ------ |------ |
| GET | /api/tg/msg | *ID | str |tg群組MessageID |
| GET | /api/tg/msg | *context | str | 要推播的內容 (輸入內容不可超過1000字元) |

### 系統訊息顯示說明
1.  {"Status": "200"}  : 傳送成功
2.  {"Error": "Please insert current MsgID"} : 錯誤ID或者目前資料庫無此ID
3.  {"Error": "Please insert ID & context args at the same time"} : ID和context參數要同時使用


### 推播檔案
| Method | path | 參數 | 類型 | 說明 |
| ------ | ------ | ------ | ------ |------ |
| GET | /api/tg/sendfile | *ID | str | tg群組MessageID |
| GET | /api/tg/sendfile | *path | str | 推播檔案的路徑 |

### 系統訊息顯示說明
1. {"Status": "200"}  : 傳送成功
2. {"Error": "Please insert current MsgID"} : 錯誤ID或者目前資料庫無此ID
3. {"Error": "insert current path"} : 路徑格式錯誤
4. {"Error": "insert file location."} : 沒輸入path值
5. {"Error": "Please insert ID & File Path at the same time"} : ID和path參數要同時使用
6. {"PathExample": "C:/User/filename.txt"} : 路徑範例


### 推播圖片
| Method | path | 參數 | 類型 | 說明 |
| ------ | ------ | ------ | ------ |------ |
| GET | /api/tg/sendphoto | *ID | str | tg群組MessageID |
| GET | /api/tg/sendphoto | *path | str | 推播圖片檔案的路徑 |

### 系統訊息顯示說明
1. {"Status": "200"}  : 傳送成功
2. {"Error": "Please insert current MsgID"} : 錯誤ID或者目前資料庫無此ID
3. {"Error": "insert current path"} : 路徑格式錯誤
4. {"Error": "insert file location."} : 沒輸入path值
5. {"Error": "Please insert ID & Photo Path at the same time"} : ID和path參數要同時使用
6. ("PathExample": "C:/User/filename.jpg"} : 路徑範例



## Get Start 

Base URL: https://10.80.1.18



