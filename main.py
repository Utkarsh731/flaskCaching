from flask import Flask
import requests
from operator import itemgetter
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object('config.Config')
cache = Cache(app)

@app.route("/api")
@cache.cached(timeout=3600, query_string=True)
def hello_world():
    response = requests.get("https://api.covidtracking.com/v1/us/daily.json")
    response = response.json()
    response = sorted(response,key=itemgetter("date"))
    return_response = []
    for data in response:
        return_response.append({"date":data["date"],"positive":data["positive"]})
    return {"data": return_response}

if __name__ == "__main__":
    app.run()
