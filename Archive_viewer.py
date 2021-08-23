import tkinter as tk
from tkinter import filedialog, Menu, ttk
import csv
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

file_name = ''
header_row = []
kks_code ='Время'


def file_converter():

    file_name = filedialog.askopenfilename()

    with open(file_name, 'r', encoding = 'windows-1251') as f:
        lines = f.readlines()

    del lines[:4]
    file_name = file_name.replace('.txt','.csv')

    with open(file_name,'w+') as f:
        for line in lines:
            line = line.replace('|',',')
            f.write(line)

    save_ex = tk.messagebox.askyesno('Сообщение', 'Требуется ли дополнительно сохранить файл в Excel?')

    if save_ex:
        read_file = pd.read_csv(file_name, encoding = 'windows-1251')
        read_file.to_excel(file_name.replace('.csv','.xlsx'), index = None, header = True)

    tk.messagebox.showinfo('Сообщение', 'Файл ' + file_name + ' успешно конвертирован!')


def file_opener():

    global header_row, file_name

    file_name = filedialog.askopenfilename()

    with open(file_name) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        dates = []

        for row in reader:
            current_date = datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S.%f ')
            dates.append(current_date)

    name = tk.Label(window, anchor ='nw' ,text = f"Открыт файл: {file_name}" )
    name.grid(column = 0, row = 0, sticky = 'nw')

    cont = tk.Label(window, anchor = 'nw', text = f"Число параметров: {len(header_row) - 2}" )
    cont.grid(column = 0, row = 1, sticky = 'nw')

    time_period = tk.Label(window, anchor = 'nw', text = f"Период времени: с {dates[0].strftime('%d.%m.%Y %H:%M:%S')} по {dates[-1].strftime('%d.%m.%Y %H:%M:%S')}" )
    time_period.grid(column = 0, row = 2, sticky = 'nw')

    time_step = tk.Label(window, anchor = 'nw', text = f"Шаг по времени: {dates[1] - dates[0]}" )
    time_step.grid(column = 0, row = 3, sticky = 'nw')


def get_header():

    combo['values'] = header_row[1:-2]


def graph_builder(code):

   
    params, dates = [],[]
    with open(file_name) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        kks_ind = header_row.index(code)


        for row in reader:
            current_date = datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S.%f ')
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





window = tk.Tk()
window.title("Архивы")
window.geometry('600x150')

file_menu = Menu(window)
conv = Menu(file_menu, tearoff = 0)
conv.add_command(label = 'Конвертировать .txt файл в .csv', font = ('', 10), command = file_converter)
conv.add_separator()
conv.add_command(label = 'Открыть .csv файл', font = ('', 10), command = file_opener)
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

combo = ttk.Combobox(window, values = [], postcommand = get_header, state = "readonly")
combo.grid(column = 0, row = 4,sticky = 'nw')



graph_button = tk.Button(window, text = 'Постротить график', command = lambda: graph_builder(combo.get()))
graph_button.grid(column = 0, row = 5,sticky = 'nw')


window.mainloop()

