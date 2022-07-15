from flask import Flask, render_template, request, Response
from helpers import *

app = Flask(__name__)
city = 'mashhad'

@app.route('/', methods=['GET', 'Post'])
def index():
    if request.method == 'GET':
        stations = set()
        for line in get_lines(city):
            for station in line:
                stations.add(station)
        return render_template('index.html', stations=sorted(stations), city=city.title())
    elif request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('dest')
        return Response(f'<h1>{route(start, end)}</h1></br><a href="/">Home</a>'.replace('\n','</br>'))

if __name__ == '__main__':
    app.run()

