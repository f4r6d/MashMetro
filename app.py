from flask import Flask, render_template, request, Response, redirect

app = Flask(__name__)

get_in = 17
get_out = 12
change_line = 10
station_time = 2
c = 'tehran'

def get_lines(c):
        lines = []
        with open(f'{c}.txt','r') as f:
            for line in f:
                lines.append(line.strip().split())
        return lines

def which_line(s):
    lines = get_lines(c)
    in_lines = list()
    for i,l in enumerate(lines):
        if s in l:
            in_lines.append(i)
    return in_lines

def get_intersextions():
    intersections = dict()
    lines = get_lines(c)
    for line in lines:
        for station in line:
            if len(which_line(station)) > 1:
                intersections[station] = which_line(station)
    return intersections
    

def get_ints(s,e):
    intersections = get_intersextions()
    s_lines = which_line(s)
    e_lines = which_line(e)
    intss = []
    for sl in s_lines:
            for el in e_lines:
                for ints in intersections:
                    if [sl, el] == intersections[ints] or [el, sl] == intersections[ints]:
                        intss.append([sl, el, ints])
    return intss

def get_ints_lvl_2(s,e):
    intersections = get_intersextions()
    s_lines = which_line(s)
    e_lines = which_line(e)
    intss = []
    for sl in s_lines:
            for el in e_lines:
                for ii in intersections:
                    for jj in intersections:
                        if ii == jj:
                            continue
                        if (intersections[ii][0] == sl and intersections[jj][1] == el):
                            if intersections[ii][1] == intersections[jj][0]:
                                intss.append([intersections[ii][0],intersections[ii][1],intersections[jj][1],ii,jj])
                        if (intersections[jj][0] == el and intersections[ii][1] == sl):
                            if intersections[jj][1] == intersections[ii][0]:
                                intss.append([intersections[jj][0],intersections[jj][1],intersections[ii][1],jj,ii])
    return intss

def route(s,e):
    lines = get_lines(c)
    s_lines = which_line(s)
    e_lines = which_line(e)

    for sl in s_lines:
        if sl in e_lines:
            route = ''
            stations_count = lines[sl].index(s) - lines[sl].index(e)
            total = get_in + get_out + abs(stations_count) * station_time
            route += f'\n{s} >>>>>Toward {lines[sl][0] if stations_count > 0 else lines[sl][-1]}>>>>> {e}\n'
            route += f'\nTotal Stations: {abs(stations_count)}'
            route += f'\nEstimatad time: {total} minutes\n'
            return route
    else:
        if intss := get_ints(s,e):
            route = ''
            for j, i in enumerate(intss, 1):
                ss, ee, ints = i
                stations_count = abs(lines[ss].index(s) - lines[ss].index(ints)) + abs(lines[ee].index(e) - lines[ee].index(ints))
                total = get_in + get_out + change_line + stations_count * station_time

                route += f'\nRoute {j}:'
                route += f'\n{s} >>>>>Toward {lines[ss][0] if lines[ss].index(s) - lines[ss].index(ints) > 0 else lines[ss][-1]}>>>>> {ints}'
                route += f'\n{ints} >>>>>Toward {lines[ee][0] if lines[ee].index(ints) - lines[ee].index(e) > 0 else lines[ee][-1]}>>>>> {e}'
                route += f'\nTotal Stations: {stations_count}'
                route += f'\nEstimatad time: {total} minutes\n'

            return route
        else:
            intss_2 = get_ints_lvl_2(s,e)
            route = ''
            for j, i in enumerate(intss_2,1):
                try:
                    ss, mm, ee, ints_1, ints_2 = i
                    stations_count = abs(lines[ss].index(s) - lines[ss].index(ints_1)) + abs(lines[mm].index(ints_1) - lines[mm].index(ints_2)) + abs(lines[ee].index(e) - lines[ee].index(ints_2))
                except:
                    ee, mm, ss, ints_2, ints_1 = i
                    stations_count = abs(lines[ss].index(s) - lines[ss].index(ints_1)) + abs(lines[mm].index(ints_1) - lines[mm].index(ints_2)) + abs(lines[ee].index(e) - lines[ee].index(ints_2))
                total = get_in + get_out + change_line * 2 + stations_count * station_time
                route += f'\nRoute {j}:'
                route += f'\n{s} >>>>>Toward {lines[ss][0] if lines[ss].index(s) - lines[ss].index(ints_1) > 0 else lines[ss][-1]}>>>>> {ints_1}'
                route += f'\n{ints_1} >>>>>Toward {lines[mm][0] if lines[mm].index(ints_1) - lines[mm].index(ints_2) > 0 else lines[mm][-1]}>>>>> {ints_2}'
                route += f'\n{ints_2} >>>>>Toward {lines[ee][0] if lines[ee].index(ints_2) - lines[ee].index(e) > 0 else lines[ee][-1]}>>>>> {e}'
                route += f'\nTotal Stations: {stations_count}'
                route += f'\nEstimatad time: {total} minutes\n'
            return route


@app.route('/', methods=['GET', 'Post'])
def index():
    if request.method == 'GET':
        stations = set()
        for line in get_lines(c):
            for station in line:
                stations.add(station)
        return render_template('index.html', stations=sorted(stations), city=c.title())
    elif request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('dest')
        return Response(f'<h1>{route(start, end)}</h1></br><a href="/">Home</a>'.replace('\n','</br></br>'))


@app.route('/changecity',methods=['Post'])
def changecity():
    if request.method == 'POST':
        new_city = request.form.get('city')
        global c
        c = new_city
        return redirect('/')

if __name__ == '__main__':
    app.run()