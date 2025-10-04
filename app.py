from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    lang = request.args.get('lang', 'en')
    return render_template('index.html', lang=lang)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
