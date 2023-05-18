from flask import Flask
from flask import request
import requests
import json
import flask
from prometheus_client import Counter, Gauge, Histogram, start_http_server, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

from prometheus_flask_exporter import PrometheusMetrics
from datetime import datetime, timedelta



app = Flask(__name__)
app.config.from_pyfile('settings.py')
metrics = PrometheusMetrics(app)

#rps_counter = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint', 'status'])
http_requests_total = Counter("http_requests_total", "Total HTTP Requests")



@app.route('/metrics')
def metrics():
    """Функция `metrics()` обрабатывает HTTP-запрос к этой конечной точке и возвращает текущее значение метрик в формате `Prometheus`"""
    return generate_latest(), 200, {'ContentType': CONTENT_TYPE_LATEST}

@app.route("/rps")
def rps():
    # получаем текущее время и время, на 1 минуту раньше
    now = datetime.utcnow()
    minute_ago = now - timedelta(minutes=1)

    # получаем число запросов за последнюю минуту
    num_requests = http_requests_total.count_over_time(f"[1m]")

    # рассчитываем rps
    rps = num_requests / 60

    # возвращаем результат в виде текстового ответа
    return f"RPS: {rps}"


@app.route('/')
def hello_world():
    #rps_counter.labels(method=request.method, endpoint=request.path, status=200).inc()
    http_requests_total.inc()
    return 'Hello, this is weather-service!'



@app.route('/forecast_weather', methods=['GET'])
def get():
    city = request.args.get('city')
    dt = request.args.get('dt')
    #url = 'http://api.weatherapi.com/v1/forecast.json?key=92b2b54828074632897211731232702&q={}&days=14'
    url = app.config.get("URL")
    url = url.format(city)
    data = requests.get(url).content
    data = json.loads(data.decode('utf-8'))
    print(type(data))
    if len(dt.split("_")) == 2:
        dt = dt.replace("_", " ")
        for date in data["forecast"]["forecastday"]:
            for dtime in date["hour"]:
                print(dtime)
                print(str(dt))
                if str(dtime["time"]) == str(dt):
                    print("da2")
                    resp_date = str(dtime["temp_c"])
    elif len(dt.split("_")) == 1:
        for date in data["forecast"]["forecastday"]:
            if date["date"] == dt:
                print(date["hour"][1])
                resp_date = str(date["day"]["avgtemp_c"])

    print(resp_date)
    resp = {"city": data["location"]["name"], "unit": "celsius", "temperature": resp_date}
    #rps_counter.labels(method=request.method, endpoint=request.path, status=200).inc()
    http_requests_total.inc()

    return flask.jsonify(resp)


@app.route('/current_weather', methods=['GET'])
def cur():
    city = request.args.get('city')
    #url = 'http://api.weatherapi.com/v1/forecast.json?key=92b2b54828074632897211731232702&q={}&days=14'
    print("da, zashel")
    url = app.config.get("URL")
    url = url.format(city)
    data = requests.get(url).content
    data = json.loads(data.decode('utf-8'))
    #print(app.config.get("URL"))
    resp = {"city": data["location"]["name"], "unit": "celsius","temperature": data["current"]["temp_c"]}
    #rps_counter.labels(method=request.method, endpoint=request.path, status=200).inc()
    http_requests_total.inc()

    return flask.jsonify(resp)



if __name__ == '__main__':
    start_http_server(8000)
    app.run(debug=True)
