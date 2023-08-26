from datetime import datetime
from csv import writer
import tkinter as tk


def log_writer(row):
    dt = datetime.now()
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    epoch_time = datetime(2022, 12, 1)
    row = [ts, (dt - epoch_time).total_seconds()] + row
    try:
        with open('./log_files/logfile.csv', 'a', newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(row)
            f_object.close()
    except PermissionError:
        tk.messagebox.showinfo(title="Permission Error", message="Close the Logfile before running this program.")
        quit()


def quit_program(escape_flag):
    if escape_flag is True:
        exit()
