from flask import Flask

app = Flask(__name__, static_url_path='/dada/static', static_folder='static')
app.config['APPLICATION_ROOT'] = '/dada'

@app.route('/dada/')
def home():
    return "Welcome to the Dada App!"

if __name__ == '__main__':
    app.run()
