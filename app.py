from flask import Flask, jsonify

# 建立 Flask 應用程式
app = Flask(__name__)

# --- 你的第一個 API 路由 (Route) ---
# @app.route() 是一個「裝飾器」，它告訴 Flask：
# 當有人用 GET 請求訪問 "/" (網站根目錄) 時，
# 就執行下面的函式。
@app.route("/")
def get_hello_world():
    # jsonify 會把 Python 的字典 (dict) 轉換成
    # 業界標準的 JSON 格式回傳
    return jsonify({ "message": "Hello, World!" })

# 確保這個檔案是被直接執行的，而不是被匯入的
if __name__ == "__main__":
    # app.run(debug=True) 會啟動伺服器
    # debug=True 讓我們在修改程式碼後，伺服器會自動重啟
    app.run(debug=True)