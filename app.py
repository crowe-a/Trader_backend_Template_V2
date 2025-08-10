from flask import Flask, render_template, redirect, url_for,request
import threading
from bot import open_browser
from backend import get_ballance,buy,sell
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from backend import trade_executor
# from flask_socketio import SocketIO
app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")
bot_thread = None

# def log_message(msg):
#     """log message"""
#     print(msg)
#     socketio.emit("log", msg)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    global bot_thread
    if open_browser.running:  # Bot zaten çalışıyorsa
        return render_template("start.html", message="Bot has already started .")
    
    bot_thread = threading.Thread(target=open_browser.run)  # Fonksiyon veriyoruz
    bot_thread.start()
    return render_template("start.html", message="Bot started.")

@app.route("/stop")
def stop():
    if open_browser.running:
        open_browser.stop()  # Durdurma fonksiyonu
        return render_template("stop.html", message="Bot stoped.")
    return render_template("stop.html", message="The bot has already stoppedr.")
from flask import jsonify

@app.route("/get_balance")
def get_balance():
    try:
        balance = get_ballance.get_bl()  # Backend işlemi
        return jsonify({"status": "success", "balance": balance})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/market")
def market():
    if hasattr(open_browser, "running") and open_browser.running:
        msg = "Market işlemleri için hazırsınız."
    else:
        msg = "Lütfen önce botu başlatın (/start)."

    return render_template("market.html", message=msg)



@app.route("/trade", methods=["POST"])
def trade():
    try:
        pair = request.json.get("pair")
        action = request.json.get("action")
        
        if action == "buy":
            result = buy.run_buy(pair)
        elif action == "sell":
            result = sell.run_sell(pair)
        else:

            return jsonify({"status": "error", "message": "Invalid action"})
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.route("/execute_trade", methods=["POST"])
def execute_trade():
    try:
        pair = request.json.get("pair")
        action = request.json.get("action")
        amount = request.json.get("amount")
        market_data = trade_executor.search()
        if action == "buy":
            result = trade_executor.execute_buy(pair, amount)
            
        elif action == "sell":
            result = trade_executor.execute_sell(pair, amount)
            
        else:
            return jsonify({"status": "error", "message": "Invalid action"})

        return jsonify({"status": "success", "data": result, "market_data": market_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    
@app.route("/get_market_data", methods=["GET"])
def get_market_data():
    try:
        market_data = trade_executor.search()
        return jsonify({"status": "success", "market_data": market_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0", port=5000)
if __name__ == "__main__":
    app.run(debug=True)
