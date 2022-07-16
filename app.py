from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import get_cities, get_lines, route

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

c = 'mashhad'


@app.route('/', methods=['GET', 'Post'])
def index():
    if request.method == 'GET':
        cities = sorted(get_cities())
        try:
            cc = session['city']
        except:
            cc = c
        stations = list()
        for i, line in enumerate(get_lines(cc), 1):
            stations.append(f'Line {i} stations:')
            for station in line:
                stations.append(station)
        return render_template('index.html', stations=stations, cities=cities, ct=cc)

    elif request.method == 'POST':
        try:
            cc = session['city']
        except:
            cc = c
        start = request.form.get('start')
        end = request.form.get('dest')
        city = request.form.get('city')
        get_in = int(request.form.get('getinInput'))
        get_out = int(request.form.get('getoutInput'))
        change_line = int(request.form.get('chlInput'))
        station_time = int(request.form.get('estInput'))
        routes = route(start, end, city, get_in, get_out,
                       change_line, station_time)
        return render_template('results.html', routes=sorted(routes, key=lambda x: x[2]), ct=cc, start=start, end=end)


@app.route('/changecity', methods=['Post'])
def changecity():
    if request.method == 'POST':
        new_city = request.form.get('city')
        # global c
        # c = new_city
        session['city'] = new_city
        return redirect('/')


if __name__ == '__main__':
    app.run()
