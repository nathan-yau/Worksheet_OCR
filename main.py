import numpy as np
import pandas as pd
import cv2
import supporting_functions


def default_files_setup():
    blank_image = (np.zeros((1280, 920, 3), np.uint8))
    cv2.imwrite('./Source/{}'.format('target.png'), blank_image)
    df = pd.read_csv("./LogFile/table.csv", dtype=str)
    supporting_functions.log_writer(["", "Default Loaded", " "])
    return df


def login_session():
    handler = str(input("Input your full name: ")).title()
    print("")
    supporting_functions.log_writer([handler, "Login", " "])
    return handler


def main():
    default_parameters = default_files_setup()
    username = login_session()
    # escape = False
    # counter = 0


if __name__ == "__main__":
    main()
