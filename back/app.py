from app import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to CloudSoft!'

if __name__ == '__main__':
    app.run(debug=True)
