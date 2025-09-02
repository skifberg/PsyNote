from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "✅ Сервер работает! Порт свободен."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)