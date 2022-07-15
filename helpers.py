
# Tajrish Gheytariyeh Shahid_Sadr Gholhak Doctor_Shari'ati Mirdamad Shahid_Haghani Shahid_Hemmat Mosalla-ye_Emam_Khomeini Shahid_Beheshti Shahid_Mofatteh Shohada-ye_Haftom-e_Tir Taleghani Darvazeh_Dowlat Sa'di Emam_Khomeini Panzdah-e_Khordad Khayyam Meydan-e_Mohammadiyeh Shoush Payaneh_Jonoub Shahid_Bokharaei Ali_Abad Javanmard-e_Ghassab Shahr-e_Rey Palayeshgah Shahed-Bagher_Shahr Haram-e_Motahhar-e_Emam_Khomeini Kahrizak
# Farhangsara Tehranpars Shahid_Bagheri Daneshgah-e_Elm-o_San'at Sarsabz Janbazan Fadak Sabalan Shahid_Madani Emam_Hossein Darvazeh_Shemiran Baharestan Mellat Emam_Khomeini Hasan_Abad Daneshgah-e_Emam_Ali Meydan-e_Hor Shahid_Navab-e_Safavi Shademan Daneshgah-e_Sharif Tarasht Tehran_Sadeghiyeh
# Gha'em Shahid_Mahallati Aghdasiyeh Nobonyad Hossein_Abad Meydan-e_Heravi Shahid_Zeynoddin Khajeh_Abdollah-e_Ansari Shahid_sayyad-e_Shirazi Shahid_Ghodousi Sohrevardi Shahid_Beheshti Mirza-ye_Shirazi Meydan-e_Jahad Meydan-e_Hazrat-e_Vali_Asr Teatr-e_Shahr Moniriyeh Mahdiyeh Rahahan Javadiyeh Zamzam Shahrak-e_Shari'ati Abdol_Abad Ne'mat_Abad Azadegan
# Shahid_Kolahdouz Nirou_Havaei Nabard Pirouzi Ebn-e_Sina Meydan-e_Shohada Darvazeh_Shemiran Darvazeh_Dowlat Ferdowsi Teatr-e_Shahr Meydan-e_Enghelab-e_Eslami Towhid Shademan Doctor_Habibollah Ostad_Mo'in Meydan-e_Azadi Bimeh Shahrk-e_Ekbatan Eram-e_Sabz
# Shahid_Sepahbod_Qasem_Soleimani Golshahr Mohammad_Shahr Karaj Atmosfer Garmdarreh Vardavard Iran_Khodro Chitgar Varzeshgah-e_Azadi Eram-e_Sabz Tehran_Sadeghiyeh
# Shahid_Sattari Shahid_Ashrafi_Esfahani Yadegar-e_Emam Marzdaran Shahrak-e_Azmayesh Daneshgah-e_Tarbiat_Modarres Meydan-e_Hazrat-e_Vali_Asr Shohada-ye_Haftom-e_Tir Emam_Hossein Meydan-e_Shohada Amir_Kabir Shahid_Rezaei Be'sat Kiyan_Shahr Dowlat_Abad
# Meydan-e_San'at Borj-e_Milad-e_Tehran Boostan-e_Goftegou Daneshgah-e_Tarbiat_Modarres Modafean-e_Salamat Towhid Shahid_Navab-e_Safavi Roudaki Komeyl Beryanak Helal_Ahmar Mahdiyeh Meydan-e_Mohammadiyeh Mowlavi Meydan-e_Ghiyam Chehel_Tan-e_Doulab Ahang Basij

# default estimation times
get_in = 17
get_out = 12
change_line = 10
station_time = 2
city = 'mashhad'

def get_lines(c='mashhad'):
    lines = []
    with open(f'{c}.txt','r') as f:
        for line in f:
            lines.append(line.strip().split())
    return lines

lines = get_lines(city)

def which_line(s):
    in_lines = list()
    for i,l in enumerate(lines):
        if s in l:
            in_lines.append(i)
    return in_lines

intersections = dict()
for line in lines:
    for station in line:
        if len(which_line(station)) > 1:
            intersections[station] = which_line(station)

def get_ints(s,e):
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

