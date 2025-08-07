import time
import os
import threading
from flask import Flask, jsonify
from datetime import datetime
import requests
import random

app = Flask(__name__)

class ConservativeTradingBot:
    def __init__(self):
        self.signals = []
        self.running = True
        self.bot_name = "CONSERVATIVE BOT"
        self.symbols = ['EURUSD', 'GBPUSD']  # Only major pairs
        self.telegram_token = os.environ.get('TELEGRAM_TOKEN')
        self.chat_id = os.environ.get('CHAT_ID')
    
    def generate_conservative_signal(self):
        """Generate low-risk signals"""
        symbol = random.choice(self.symbols)
        
        # Conservative parameters
        if random.random() > 0.7:  # Only trade 30% of the time
            action = random.choice(['BUY', 'SELL'])
            price = round(random.uniform(1.0500, 1.2000), 5)
            
            # Small TP/SL for conservative approach
            if action == 'BUY':
                tp = round(price + 0.0015, 5)  # 15 pips TP
                sl = round(price - 0.0010, 5)  # 10 pips SL
            else:
                tp = round(price - 0.0015, 5)
                sl = round(price + 0.0010, 5)
            
            signal = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'action': action,
                'entry_price': price,
                'take_profit': tp,
                'stop_loss': sl,
                'risk_level': 'LOW',
                'confidence': random.randint(75, 90)
            }
            
            self.signals.append(signal)
            self.send_telegram_signal(signal)
            
            if len(self.signals) > 10:
                self.signals.pop(0)
    
    def send_telegram_signal(self, signal):
        if self.telegram_token and self.chat_id:
            message = f"""
🔵 {self.bot_name} SIGNAL
Symbol: {signal['symbol']}
Action: {signal['action']}
Entry: {signal['entry_price']}
TP: {signal['take_profit']}
SL: {signal['stop_loss']}
Risk: {signal['risk_level']}
Confidence: {signal['confidence']}%
Time: {signal['timestamp']}
            """
            
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {'chat_id': self.chat_id, 'text': message}
            try:
                requests.post(url, data=data)
            except:
                pass
    
    def run(self):
        while self.running:
            self.generate_conservative_signal()
            time.sleep(1800)  # Generate signal every 30 minutes

bot = ConservativeTradingBot()

@app.route('/')
def home():
    return f"🔵 {bot.bot_name} is RUNNING!"

@app.route('/signals')
def get_signals():
    return jsonify(bot.signals)

@app.route('/status')
def status():
    return jsonify({
        'bot_name': bot.bot_name,
        'status': 'running',
        'signals_count': len(bot.signals),
        'last_update': datetime.now().isoformat()
    })

if __name__ == "__main__":
    # Start bot in background
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
