import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


class Data(object):
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y



def chk_idx(idx):
    try:
        idx[0].split(',')[13]
        return True
    except IndexError:
        return False


input_dir = 'C:\\Users\\320047209\\OneDrive - Philips\\Desktop\\Test Wafers\\05272021\\Data'

files = []
target_dir = os.listdir(input_dir)
for item in target_dir:
    if item[-3:] == 'csv':
        files.append(item)

points = []
for file in files:
    #y_data = []
    #x_data = []

    csv_file = open(input_dir + '\\' + file, 'r', newline='')
    reader = csv.reader(csv_file, delimiter='\n')
    for idx, row in enumerate(reader):
        if chk_idx(row) is True:
            points[idx] = Data()
            y_val = row[0].split(',')[13]
            if y_val != '<Data>':
                #y_data.append(y_val)
                points[idx].set_x(x_val)
            x_val = row[0].split(',')[0]
            if x_val != '<File Timestamp>':
                x_val = datetime.datetime.strptime(x_val, '%d-%B-%Y %H:%M:%S')
                #x_data.append(x_val)
                points[idx].set_y(y_val)

    print(points)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%B-%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.plot()
    plt.gcf().autofmt_xdate()
    plt.show()