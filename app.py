from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Irving Yahir Hernandez Mateo -20211042, 9º "A"'

if __name__ == '__main__':
    app.run(debug=True)
