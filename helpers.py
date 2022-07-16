import os


def get_cities(p='static/'):
    cities = set()
    for file in os.listdir(p):
        if file.endswith('.txt'):
            cities.add(file[:-4])
    return cities


def get_lines(city):
    lines = []
    with open(f'static/{city}.txt', 'r') as f:
        for line in f:
            lines.append(line.strip().split())
    return lines


def which_line(s, city):
    lines = get_lines(city)
    in_lines = list()
    for i, l in enumerate(lines):
        if s in l:
            in_lines.append(i)
    return in_lines


def get_intersextions(city):
    intersections = dict()
    lines = get_lines(city)
    for line in lines:
        for station in line:
            if len(which_line(station, city)) > 1:
                intersections[station] = which_line(station, city)
    return intersections


def get_ints(s, e, city):
    intersections = get_intersextions(city)
    s_lines = which_line(s, city)
    e_lines = which_line(e, city)
    intss = []
    for sl in s_lines:
        for el in e_lines:
            for ints in intersections:
                if [sl, el] == intersections[ints] or [el, sl] == intersections[ints]:
                    intss.append([sl, el, ints])
    return intss


def get_ints_lvl_2(s, e, city):
    intersections = get_intersextions(city)
    s_lines = which_line(s, city)
    e_lines = which_line(e, city)
    intss = []
    for sl in s_lines:
        for el in e_lines:
            for ii in intersections:
                for jj in intersections:
                    if ii == jj:
                        continue
                    if (intersections[ii][0] == sl and intersections[jj][1] == el):
                        if intersections[ii][1] == intersections[jj][0]:
                            intss.append(
                                [intersections[ii][0], intersections[ii][1], intersections[jj][1], ii, jj])
                    if (intersections[jj][0] == el and intersections[ii][1] == sl):
                        if intersections[jj][1] == intersections[ii][0]:
                            intss.append(
                                [intersections[jj][0], intersections[jj][1], intersections[ii][1], jj, ii])
    return intss


def get_ints_lvl_3(s, e, city):
    intersections = get_intersextions(city)
    s_lines = which_line(s, city)
    e_lines = which_line(e, city)
    intss = []
    for sl in s_lines:
        for el in e_lines:
            for ii in intersections:
                for kk in intersections:
                    for jj in intersections:
                        if ii == jj:
                            continue
                        if (intersections[ii][0] == sl and intersections[jj][1] == el):
                            if (intersections[ii][1] == intersections[kk][0]) and (intersections[kk][1] == intersections[jj][0]):
                                intss.append([intersections[ii][0], intersections[kk][0],
                                             intersections[kk][1], intersections[jj][1], ii, kk, jj])
                        if (intersections[jj][0] == el and intersections[ii][1] == sl):
                            if (intersections[jj][1] == intersections[kk][1]) and (intersections[kk][0] == intersections[ii][0]):
                                intss.append([intersections[jj][0], intersections[kk][1],
                                             intersections[kk][0], intersections[ii][1], jj, kk, ii])
    return intss


def route(s, e, city, get_in, get_out, change_line, station_time):
    lines = get_lines(city)
    s_lines = which_line(s, city)
    e_lines = which_line(e, city)

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
        if intss := get_ints(s, e, city):
            route = ''
            for j, i in enumerate(intss, 1):
                ss, ee, ints = i
                stations_count = abs(lines[ss].index(
                    s) - lines[ss].index(ints)) + abs(lines[ee].index(e) - lines[ee].index(ints))
                total = get_in + get_out + change_line + stations_count * station_time

                route += f'\nRoute {j}:'
                route += f'\n{s} >>>>>Toward {lines[ss][0] if lines[ss].index(s) - lines[ss].index(ints) > 0 else lines[ss][-1]}>>>>> {ints}'
                route += f'\n{ints} >>>>>Toward {lines[ee][0] if lines[ee].index(ints) - lines[ee].index(e) > 0 else lines[ee][-1]}>>>>> {e}'
                route += f'\nTotal Stations: {stations_count}'
                route += f'\nEstimatad time: {total} minutes\n'
            return route

        elif intss_2 := get_ints_lvl_2(s, e, city):
            route = ''
            for j, i in enumerate(intss_2, 1):
                try:
                    ss, mm, ee, ints_1, ints_2 = i
                    stations_count = abs(lines[ss].index(s) - lines[ss].index(ints_1)) + abs(lines[mm].index(
                        ints_1) - lines[mm].index(ints_2)) + abs(lines[ee].index(e) - lines[ee].index(ints_2))
                except:
                    ee, mm, ss, ints_2, ints_1 = i
                    stations_count = abs(lines[ss].index(s) - lines[ss].index(ints_1)) + abs(lines[mm].index(
                        ints_1) - lines[mm].index(ints_2)) + abs(lines[ee].index(e) - lines[ee].index(ints_2))
                total = get_in + get_out + change_line * 2 + stations_count * station_time
                route += f'\nRoute {j}:'
                route += f'\n{s} >>>>>Toward {lines[ss][0] if lines[ss].index(s) - lines[ss].index(ints_1) > 0 else lines[ss][-1]}>>>>> {ints_1}'
                route += f'\n{ints_1} >>>>>Toward {lines[mm][0] if lines[mm].index(ints_1) - lines[mm].index(ints_2) > 0 else lines[mm][-1]}>>>>> {ints_2}'
                route += f'\n{ints_2} >>>>>Toward {lines[ee][0] if lines[ee].index(ints_2) - lines[ee].index(e) > 0 else lines[ee][-1]}>>>>> {e}'
                route += f'\nTotal Stations: {stations_count}'
                route += f'\nEstimatad time: {total} minutes\n'
            return route

        elif intss_3 := get_ints_lvl_3(s, e, city):
            route = ''
            for j, i in enumerate(intss_3, 1):
                try:
                    ss, mm, nn, ee, ints_1, ints_2, ints_3 = i
                    stations_count = abs(lines[ss].index(s) - lines[ss].index(ints_1)) + abs(lines[mm].index(ints_1) - lines[mm].index(
                        ints_2)) + abs(lines[nn].index(ints_2) - lines[nn].index(ints_3)) + abs(lines[ee].index(ints_3) - lines[ee].index(e))
                except:
                    ee, nn, mm, ss, ints_3, ints_2, ints_1 = i
                    stations_count = abs(lines[ss].index(s) - lines[ss].index(ints_1)) + abs(lines[mm].index(ints_1) - lines[mm].index(
                        ints_2)) + abs(lines[nn].index(ints_2) - lines[nn].index(ints_3)) + abs(lines[ee].index(ints_3) - lines[ee].index(e))
                total = get_in + get_out + change_line * 2 + stations_count * station_time
                route += f'\nRoute {j}:'
                route += f'\n{s} >>>>>Toward {lines[ss][0] if lines[ss].index(s) - lines[ss].index(ints_1) > 0 else lines[ss][-1]}>>>>> {ints_1}'
                route += f'\n{ints_1} >>>>>Toward {lines[mm][0] if lines[mm].index(ints_1) - lines[mm].index(ints_2) > 0 else lines[mm][-1]}>>>>> {ints_2}'
                route += f'\n{ints_2} >>>>>Toward {lines[nn][0] if lines[nn].index(ints_2) - lines[nn].index(ints_3) > 0 else lines[nn][-1]}>>>>> {ints_3}'
                route += f'\n{ints_3} >>>>>Toward {lines[ee][0] if lines[ee].index(ints_3) - lines[ee].index(e) > 0 else lines[ee][-1]}>>>>> {e}'
                route += f'\nTotal Stations: {stations_count}'
                route += f'\nEstimatad time: {total} minutes\n'
            return route
