import os
import csv
from datetime import datetime


def timestamp(date):
    date_obj = str(datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p'))
    dt_tuple = tuple([int(x) for x in date_obj[:10].split('-')]) + tuple([int(x) for x in date_obj[11:].split(':')])
    dtime = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
    dtimestamp = dtime.timestamp()
    return float(dtimestamp)

root = 'C:/Users/320047209/Downloads/Costa Rica CAPA Data/CSV/'
for report in os.listdir(root):
    try:
        new_list = [['', '', '']]
        with open(root + report) as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(',')
                unit = line[1]
                station = line[2]
                result = line[5]
                data = float(line[9])
                date = timestamp(line[12][:-1])
                append_flag = False
                if date >= 1642136400 or 'Q' in report:         # If date range is correct
                    if station == station:
                        if result.lower() == 'pass':                        # and the unit passes
                            for idx, item in enumerate(new_list):          # check all units so far.
                                if unit == item[0]:                          # if a unit has already been recorded,
                                    append_flag = True
                                    if date > float(item[2]):                     # and its from a later date,
                                        del new_list[idx]
                                        new_list.append([unit, str(data), date])
                            if append_flag is False:
                                new_list.append([unit, str(data), date])

        del new_list[0]

        new_list.sort(key=lambda x: x[2])
        for date_correction in new_list:
            date_correction[2] = datetime.fromtimestamp(int(date_correction[2])).strftime('%m/%d/%Y %I:%M:%S %p')

        with open(root + 'Truncated/' + report[:-4] + ' TRUNCATED.csv', 'w', newline='') as trunc:
            write = csv.writer(trunc)
            write.writerows(new_list)

    except PermissionError:
        continue
