from flask import Flask
({SQL_ALCH_IMPORT})

app = Flask(__name__)
({SQL_ALCH_DB_CONTENT})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
  app.run()
