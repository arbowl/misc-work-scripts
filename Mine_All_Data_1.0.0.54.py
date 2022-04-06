import os
import csv
import os.path

# Testing
######################
import cProfile
import pstats
import multiprocessing
from timeit import default_timer as timer
######################

# See EOF for explanation
try:
    import numpy as np
    is_numpy = True
except ImportError:
    is_numpy = False

import tkinter as tk
from tkinter import *
from datetime import datetime
from tkinter import filedialog
import xml.etree.ElementTree as et
from os.path import exists as file_exists


class Window(object):
    # This def creates the app box
    def __init__(self, app):
        background = 'white smoke'
        cur_year = datetime.today().year
        self.root = app
        self.body = Frame(app, width=520, height=180, bg=background)
        self.body.pack(fill='both', expand=True)

        self.input_dir = ''
        self.output_dir = ''

        self.top_label = Label(app, text='FOR ENGINEERING USE ONLY', font=('Helvetica', '22'), fg='red')
        self.top_label.pack(padx=2, pady=2)

        self.input_label = Label(self.body, text='Input folder:', bg=background)
        self.input_label.grid(column=0, row=1)
        self.output_label = Label(self.body, text='Output folder:', bg=background)
        self.output_label.grid(column=0, row=2)

        self.input_button = Button(self.body, text='Browse', command=self.__input__)
        self.input_button.grid(column=7, row=1, padx=5, pady=10)
        self.output_button = Button(self.body, text='Browse', command=self.__output__)
        self.output_button.grid(column=7, row=2, padx=5, pady=2)

        self.input_var = StringVar()
        self.input_entry = Entry(self.body, textvariable=self.input_var, width=50)
        self.input_entry.insert(END, '')  # DEFAULT INPUT
        self.input_entry.grid(column=1, columnspan=6, row=1, padx=5, pady=2)

        self.output_var = StringVar()
        self.output_entry = Entry(self.body, textvariable=self.output_var, width=50)
        self.output_entry.insert(END, '')  # DEFAULT OUTPUT
        self.output_entry.grid(column=1, columnspan=6, row=2, padx=5, pady=2)

        self.product_var = StringVar()
        self.product_label = Label(self.body, text='Product:', background=background)
        self.product_label.grid(column=0, row=3)
        try:
            self.product_clicked = StringVar()
            self.product_options = ['Any Product'] + next(os.walk('//usdrdsech1vwa06/TestData'))[1]
            self.product_clicked.set('Any Product')
            self.product_dropdown = OptionMenu(self.body, self.product_clicked, *self.product_options)
            self.product_dropdown.grid(column=1, row=3, pady=2)
        except FileNotFoundError:
            self.product_entry = Entry(self.body, textvariable=self.product_var, width=10)
            self.product_entry.grid(column=1, row=3, padx=5)

        self.serial_var = StringVar()
        self.serial_label = Label(self.body, text='Serial #:', background=background)
        self.serial_label.grid(column=2, row=3)
        self.serial_entry = Entry(self.body, textvariable=self.serial_var, width=9)
        self.serial_entry.grid(column=3, row=3)

        self.quarter_clicked = StringVar()
        self.quarter_label = Label(self.body, text='Quarter:', background=background)
        self.quarter_label.grid(column=6, row=3)
        self.quarter_options = ['--', 'Q1', 'Q2', 'Q3', 'Q4']
        self.quarter_clicked.set('--')
        self.quarter_dropdown = OptionMenu(self.body, self.quarter_clicked, *self.quarter_options)
        self.quarter_dropdown.grid(column=7, row=3, pady=2)

        self.year_clicked = StringVar()
        self.year_label = Label(self.body, text='Year:', background=background)
        self.year_label.grid(column=4, row=3)
        self.year_options = ['----'] + list(range(cur_year - 10, cur_year + 1, 1))
        self.year_clicked.set('----')
        self.year_dropdown = OptionMenu(self.body, self.year_clicked, *self.year_options)
        self.year_dropdown.grid(column=5, row=3, pady=2)

        self.run_button = Button(self.body, text='Run', command=self.__run__, height=4, width=6)
        self.run_button.grid(column=8, row=0, rowspan=4, padx=5)

    def __input__(self):
        self.input_dir = filedialog.askdirectory(parent=root, initialdir='/', title='Input Directory')
        if len(self.input_dir) > 0:
            self.input_var.set(self.input_dir)
        return

    def __output__(self):
        self.output_dir = filedialog.askdirectory(parent=root, initialdir='/', title='Output Directory')
        if len(self.output_dir) > 0:
            self.output_var.set(self.output_dir)
        return

    def __run__(self):
        with cProfile.Profile() as pr:
            in_dir = self.input_var.get()
            out_dir = self.output_var.get()
            if in_dir == '':
                try:
                    year = self.year_clicked.get()
                    product = self.product_clicked.get()
                    quarter = self.quarter_clicked.get()
                    in_dir = '//usdrdsech1vwa06/TestData/' + product + '/' + year + '-' + quarter
                except FileNotFoundError:
                    return

            try:
                os.mkdir(out_dir)
            except OSError:
                pass

            files = []
            if is_numpy is True:
                test_database = np.array([['', '']], dtype='object')
            else:
                test_database = [['', '']]
            Q1 = ['jan', 'january', 'feb', 'february', 'mar', 'march']
            Q2 = ['apr', 'april', 'may', 'jun', 'june']
            Q3 = ['jul', 'july', 'aug', 'august', 'sep', 'september']
            Q4 = ['oct', 'october', 'nov', 'november', 'dec', 'december']

            target_directory = os.listdir(in_dir)
            for item in target_directory:
                if 'aborted' not in item.lower():
                    if item[-3:] == 'xml':
                        files.append(item)

            for file in files:
                # Resets the check to what it was when the button was clicked
                product_selected = self.product_var.get().lower()
                quarter_selected = self.quarter_clicked.get()
                year_selected    = self.year_clicked.get()
                serial_num       = self.serial_var.get()

                if serial_num == '':
                    serial_num = file
                if serial_num not in file:
                    continue

                try:
                    date = file.split('-')[-1].split(' ')[1]

                    year = date[4:]
                    if year != year_selected and year_selected != '':
                        continue
                    else:
                        pre_check = True

                    if date[:1] == '0':
                        date = date[1:]
                        leading_zero = True
                    else:
                        leading_zero = False

                    if leading_zero is True:
                        month = date[:1]
                    else:
                        month = date[:2]

                    if int(month) <= 3:
                        quarter = 'Q1'
                    elif 3 < int(month) <= 6:
                        quarter = 'Q2'
                    elif 6 < int(month) <= 9:
                        quarter = 'Q3'
                    elif 9 < int(month) <= 12:
                        quarter = 'Q4'
                    else:
                        quarter = 'Q0'

                    if quarter != quarter_selected and quarter_selected != 'Q*':
                        continue
                    else:
                        pre_check = True

                except IndexError:
                    pass

                xml_tree = et.parse(in_dir + '\\' + file)
                xml_root = xml_tree.getroot()

                # Extracts and sorts the header info
                rl = len(xml_root[0])  # Root length
                OverallResult  = xml_root[2][0].text
                Equipment      = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'Equipment'])[2:-2]
                LotNumber      = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'LotNumber'])[2:-2]
                Operator       = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'Operator'])[2:-2]
                PlatformTestSW = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'PlatformTestSW'])[2:-2]
                ProcessStep    = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'ProcessStep'])[2:-2]
                Product        = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'Product'])[2:-2]
                ProductSN      = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'ProductSN'])[2:-2]
                ProductTestSW  = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'ProductTestSW'])[2:-2]
                ReportRevision = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'ReportRevision'])[2:-2]
                Timestamp      = str([xml_root[0][x].text for x in range(0, rl) if xml_root[0][x].tag == 'Timestamp'])[2:-2]
                header = Timestamp + ',' + datetime.today().strftime('%m/%d/%Y %I:%M') + ',' + ReportRevision + ',' + \
                    Operator + ',' + Equipment + ',' + PlatformTestSW + ',' + ProductTestSW + ',' + Product + ',' + \
                    ProcessStep + ',' + LotNumber + ',' + ProductSN + ',' + OverallResult

                # Skips if this info is in the title
                if pre_check is not True:
                    day, month, year = Timestamp.split('-')
                    year = year[:4]
                    if month.lower() in Q1:
                        quarter = 'Q1'
                    elif month.lower() in Q2:
                        quarter = 'Q2'
                    elif month.lower() in Q3:
                        quarter = 'Q3'
                    elif month.lower() in Q4:
                        quarter = 'Q4'
                    else:
                        quarter = 'Q0'

                # If the respective field was left blank, allow all entries
                if year_selected == '----':
                    year = year_selected
                if quarter_selected == '--':
                    quarter_selected = quarter
                if product_selected == '':
                    product_selected = Product.lower()

                # Parses and sorts data by test
                if year == year_selected and quarter == quarter_selected and Product.lower() == product_selected:
                    for test in range(0, test_child_size(xml_root, 0) + 1):
                        for subtest in range(3, len(xml_root[1][test])):
                            if xml_root[1][test][subtest][5][2].attrib:
                                test_title = xml_root[1][test][subtest][5][2].attrib
                                test_value = xml_root[1][test][subtest][5][2].text
                                for subgroup in range(6, len(xml_root[1][test][subtest]) - 4):
                                    if is_float(xml_root[1][test][subtest][subgroup][2].text) is True:
                                        test_value = test_value + ',' + xml_root[1][test][subtest][subgroup][2].text

                                test_pass_fail = xml_root[1][test][subtest][5][1].text

                            ###########################################################################################
                            # Sorts the data into a list to be written into a *.CSV
                            # Format:       [ [ "test name 1", "report1 test1\n report2 test1\n ... reportn test1\n"]
                            #                 [ ... ]
                            #                 [ "test name n", "report1 testn\n report2 testn\n ... reportn testn\n"] ]

                                # Conversion example:
                                # 'Test="Rx Element Peak-Peak" Measurement="Pk-Pk" Record="Rx Element[0]'
                                # becomes:
                                # 'Rx Element Peak-Peak Measurement_Pk-Pk Record_Rx Element.csv'
                                test_name = test_to_filename(test_title)

                                # Creates a list of the values of the first column in the test_database 2D array
                                test_list = [i[0] for i in test_database]

                                # If the test name hasn't been added yet, add it to the first column of the 2D array
                                if test_name not in test_list:
                                    if is_numpy is True:
                                        new_row = [[test_name, '']]
                                        test_database = np.concatenate([test_database, new_row])
                                    else:
                                        test_database.append([test_name, ''])

                                # Searches the first column of the 2D array for the index containing the test name
                                if is_numpy is True:
                                    idx = int(np.where(test_database == test_name)[0])
                                else:
                                    idx = [idx for idx in test_database if test_name in idx][0]
                                    idx = test_database.index(idx)

                                # Adds data to the second column where the test index was located
                                test_database[idx][1] = test_database[idx][1] + header + ',' + test_pass_fail + ',' + \
                                    test_value + '\n'

            # This takes the database created above in test_database and makes a report for each test_database[i][1]
            # where each "i" is a new *.CSV and each [i][1] contains every row to be written, terminated by \n
            for report in range(1, len(test_database)):
                if not file_exists(self.output_dir + '\\' + test_database[report][0]):
                    csv_file = open(self.output_dir + '\\' + test_database[report][0], 'a', newline='')
                    filewriter = csv.writer(csv_file, delimiter=',', quotechar='|')
                    filewriter.writerow(['FOR ENGINEERING USE ONLY'])
                    filewriter.writerow(['<File Timestamp>', '<Timestamp>', '<ReportRevision>', '<Operator>', '<Equipment>',
                                         '<PlatformTestSW>', '<ProductTestSW>', '<Product>', '<ProcessStep>', '<LotNumber>',
                                         '<ProductSN>', '<OverallResult>', '<TestResult>', '<Data>'])
                else:
                    csv_file = open(self.output_dir + '\\' + test_database[report][0], 'a', newline='')

                database_parse = test_database[report][1].split('\n')
                filewriter = csv.writer(csv_file, delimiter='\n', quotechar='|')
                filewriter.writerows([database_parse[:-1]])

                csv_file.close()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

# Names the output file based on the test name following Tom Greene's convention
def test_to_filename(test_name):
    test_name = str(test_name)[1:][:-1]
    test_name = test_name.replace(':', '')
    test_name = test_name.replace(',', '')
    test_name = test_name.replace('(', '')
    test_name = test_name.replace(')', '')
    test_name = test_name.split('\'')[1::2]
    test_name = str(
        test_name[1] + ' ' + test_name[2] + '_' + test_name[3] + ' ' + test_name[4] + '_' + test_name[5])
    if test_name[-1:] == ']':
        test_name = test_name[:-3]
    return test_name + '.csv'


# Recursively checks child size
def test_child_size(test_root, size):
    try:
        if test_root[1][size][3][5][2].attrib:
            return test_child_size(test_root, size + 1)
    except IndexError:
        return size - 1


# Checks if a parsed value is a float
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# Creates the window and starts the loop
root = tk.Tk()
root.wm_title('Mine All Data 1.0.0.54')
root.geometry('570x180')
start = Window(root)
root.mainloop()

# A note on module choice:
# I created a sorting algorithm using numpy as well as regular lists. Numpy is faster, but Philips does not allow "pip"
# on company Wi-Fi, so midway through I decided to only use default packages. This is also why I used ElementTree
# instead of lxml. I kept the numpy algorithm since I already did the work, hence the numpy check.
