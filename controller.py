from flask import Flask
from crawler.crawler import Crawler

app = Flask(__name__)

@app.route("/sh")
def crawlingSh():
    try:
        Crawler().read()
        response = {
            "resultCd": "S",
            "errMsg": ""
        }
    except Exception as e:
        print(e)
        response = {
            "resultCd": "E",
            "errMsg": "internal server error"
        }
    return response

@app.route("/")
def hello():
    return "Hello Flask!"

@app.route("/test1")
def test1():
    return "test1"

@app.route("/test2")
def test2():
    return "test2"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8082, debug=True)