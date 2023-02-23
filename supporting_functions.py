from datetime import datetime
from csv import writer


def log_writer(row):
    try:
        dt = datetime.now()
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        epoch_time = datetime(2022, 12, 1)
        row = [ts, (dt - epoch_time).total_seconds()] + row
        with open('./log_files/logfile.csv', 'a', newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(row)
            f_object.close()
    except PermissionError:
        print("Permission Error. Close the Logfile before running this program.")
        input("Press ENTER to exit the program.")
        exit()


def page_break():
    for i in range(20):
        print(" ")


def quit_program(escape_flag):
    if escape_flag is True:
        exit()
