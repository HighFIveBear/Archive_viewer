import tkinter as tk
from tkinter import filedialog, Menu, ttk
import csv
import openpyxl
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# file_name = ''
header_row = []
kks_code ='Время'


def file_converter():

    files = filedialog.askopenfilenames(filetypes = [('text files','.txt')])

    if len(files) == 0:

        return None

    save_csv = tk.messagebox.askyesno('Сообщение', 
                        'Сохранить файлы в формате .csv?')

    if save_csv:
        for file in files:
            csv_converter(file)


    save_ex = tk.messagebox.askyesno('Сообщение', 
                        'Cохранить файлы в формате .xlsx?')

    if save_ex:
        for file in files:
            xlsx_converter(file)

    if (not save_csv) & (not save_ex):

        tk.messagebox.showinfo('Вопрос', 'Зачем было сюда жать?')

    else:

        tk.messagebox.showinfo('Сообщение', 'Файлы успешно конвертированы!')


def csv_converter(file_name):

    try:

        with open(file_name, 'r', encoding = 'windows-1251') as f:
            lines = f.readlines()

            del lines[:4]
            file_name = file_name.replace('.txt','.csv')

            with open(file_name,'w+') as f:
                for line in lines:
                    line = line.replace('|',',')
                    f.write(line)
                
    except UnicodeDecodeError:

        with open(file_name, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
            last_line = lines[-1]

            garbage = 1 + len(last_line.split('\t'))

            del lines[:garbage]
            file_name = file_name.replace('.txt','.csv')

            with open(file_name,'w+') as f:
                for line in lines:
                    line = line.replace('\t',',')
                    f.write(line)


def xlsx_converter(file_name):

    wb = openpyxl.Workbook()
    ws = wb.active

    try:

        with open(file_name, 'r', encoding = 'windows-1251') as f:
            lines = f.readlines()

            del lines[:4]
            file_name = file_name.replace('.txt','.csv')

            with open(file_name,'w+') as f:
                for line in lines:
                    line = line.replace('|',',')
                    f.write(line)
                
    except UnicodeDecodeError:

        with open(file_name, 'r', encoding = 'utf-8') as f:
            lines = f.readlines()
            last_line = lines[-1]

            garbage = 1 + len(last_line.split('\t'))

            del lines[:garbage]
            file_name = file_name.replace('.txt','.csv')

            with open(file_name,'w+') as f:
                for line in lines:
                    line = line.replace('\t',',')
                    f.write(line)

    with open(file_name) as f:
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
            ws.append(row)

    wb.save(file_name.replace('.csv','.xlsx'))


def file_opener():

    global header_row, file_name

    file_name = filedialog.askopenfilename(filetypes = [('CSV files','.csv')])

    with open(file_name) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        dates = []

        for row in reader:
            try:
                current_date = datetime.strptime(row[0], 
                                '%d.%m.%Y %H:%M:%S.%f ')
            except ValueError:
                current_date = datetime.strptime(row[0], '%d.%m.%y %H:%M:%S')
            dates.append(current_date)

    name = tk.Label(window, anchor ='nw' ,text = f'Открыт файл: {file_name}')
    name.grid(column = 0, row = 0, sticky = 'nw')

    cont = tk.Label(window, anchor = 'nw', 
                        text = f'Число параметров: {len(header_row) - 2}')
    cont.grid(column = 0, row = 1, sticky = 'nw')

    time_period = tk.Label(window, anchor = 'nw', text = 'Период времени: с '
                    f'{dates[0].strftime("%d.%m.%Y %H:%M:%S")} по ' 
                    f'{dates[-1].strftime("%d.%m.%Y %H:%M:%S")}')

    time_period.grid(column = 0, row = 2, sticky = 'nw')

    time_step = tk.Label(window, anchor = 'nw', 
                        text = f'Шаг по времени: {dates[1] - dates[0]}')
    time_step.grid(column = 0, row = 3, sticky = 'nw')


def get_header():

    combo['values'] = header_row[1:-1]


def graph_builder(code):

   
    params, dates = [],[]
    with open(file_name) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        kks_ind = header_row.index(code)

        for row in reader:
            try:
                current_date = datetime.strptime(row[0], 
                                        '%d.%m.%Y %H:%M:%S.%f ')
            except ValueError:
                current_date = datetime.strptime(row[0], '%d.%m.%y %H:%M:%S')
            dates.append(current_date)
            param = float(row[kks_ind])
            params.append(param)

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(dates, params, c='red')

    plt.title("", fontsize = 24)
    plt.xlabel(header_row[0], fontsize = 16)
    fig.autofmt_xdate()
    plt.ylabel(header_row[kks_ind], fontsize = 16)
    plt.tick_params(axis = 'both', which = 'major', labelsize = 16)

    plt.show()


def cascade_graph_builder():

    path_name = filedialog.askdirectory()

    f = open(file_name)

    for ind in range(1,len(header_row) - 1):

        reader = csv.reader(f)
        next(reader)

        params, dates = [],[]

        for row in reader:
            try:
                current_date = datetime.strptime(row[0], 
                                        '%d.%m.%Y %H:%M:%S.%f ')
            except ValueError:
                current_date = datetime.strptime(row[0], '%d.%m.%y %H:%M:%S')
            dates.append(current_date)
            param = float(row[ind])
            params.append(param)

        f.seek(0)

        plt.style.use('seaborn')
        fig, ax = plt.subplots()
        ax.plot(dates, params, c='red')

        plt.title("", fontsize = 24)
        plt.xlabel(header_row[0], fontsize = 16)
        fig.autofmt_xdate()
        plt.ylabel(header_row[ind], fontsize = 16)
        plt.tick_params(axis = 'both', which = 'major', labelsize = 16)


        plt.savefig(path_name +  '/' + header_row[ind] + '.png', 
                                            dpi = 200, bbox_inches ='tight')

    tk.messagebox.showinfo('Сообщение', 'Все графики построены!')
    f.close()



window = tk.Tk()
window.title("Архивы")
window.geometry('600x200')

file_menu = Menu(window)
conv = Menu(file_menu, tearoff = 0)
conv.add_command(label = 'Конвертировать файлы архивов СВРК(СВБУ)', 
                    font = ('', 10), command = file_converter)
conv.add_separator()
conv.add_command(label = 'Открыть .csv файл', font = ('', 10), 
                    command = file_opener)
file_menu.add_cascade(label = 'Файл', menu = conv)
window.config(menu = file_menu)

name = tk.Label(window, anchor ='nw' ,text = "Открыт файл:" )
name.grid(column = 0, row = 0, sticky = 'nw')

cont = tk.Label(window, anchor = 'nw', text = "Число параметров:" )
cont.grid(column = 0, row = 1, sticky = 'nw')

time_period = tk.Label(window, anchor = 'nw', text = "Период времени:" )
time_period.grid(column = 0, row = 2, sticky = 'nw')

time_step = tk.Label(window, anchor = 'nw', text = "Шаг по времени:" )
time_step.grid(column = 0, row = 3, sticky = 'nw')

combo = ttk.Combobox(window, values = [], postcommand = get_header, 
                            state = "readonly")
combo.grid(column = 0, row = 4,sticky = 'nw')



graph_button = tk.Button(window, text = 'Постротить график', 
                            command = lambda: graph_builder(combo.get()))
graph_button.grid(column = 0, row = 5,sticky = 'nw')

cascade_button = tk.Button(window, text = 'Построить графики всех параметров', 
                            command = cascade_graph_builder)
cascade_button.grid(column = 0, row = 6,sticky = 'nw')


window.mainloop()

