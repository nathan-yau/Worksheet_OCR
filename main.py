import numpy as np
import pandas as pd
import cv2
import supporting_functions
import camera_control
import worksheet_ocr
import answer_projection


def default_files_setup():
    empty_image = (np.zeros((1280, 920, 3), np.uint8))
    cv2.imwrite('./log_files/{}'.format('target.png'), empty_image)
    df = pd.read_csv("./log_files/table.csv", dtype=str)
    supporting_functions.log_writer(["", "Default Loaded", " "])
    return df, empty_image


def login_session():
    handler = str(input("Input your full name: ")).title()
    print("")
    supporting_functions.log_writer([handler, "Login", " "])
    return handler


def main():
    """
    Drive the program. 
    """
    escape = False
    counter = 0
    default_parameters, blank_image = default_files_setup()
    username = login_session()
    print("*"*50+"\nPlease select from the options below\n"+"*"*50)
    print("1. Grading Math Worksheets")
    print("2. Quit\n")
    menu = input("Enter selection and then press the ENTER key: ")
    while True:
        if menu == "1":
            supporting_functions.page_break()
            break
        elif menu == "2":
            print(username, "logged out.")
            supporting_functions.log_writer([username, "Logout", " "])
            escape = True
            break
        else:
            menu = input("That's not a valid option. Please enter again: ")
    supporting_functions.quit_program(escape)
    if menu == "1":
        supporting_functions.log_writer([username, "Started Grading", " "])
    #########################################################################################
    print("Initializing the Document Scanner. . .", end=" ")
    cam, win_name, rotate = camera_control.setup_cam(username)
    print("Done")
    while True:
        project_image, frame, status, counter, img_name = camera_control.capturing_image(cam, win_name, rotate, counter, username, blank_image)
        if status is False:
            break
        elif status is True:
            edge_coordinates = worksheet_ocr.detect_edge(username, img_name, frame)
            sheet_number = worksheet_ocr.detect_sheet_number(username, img_name, default_parameters, project_image, frame, edge_coordinates)
            project_image = answer_projection.define_range(default_parameters, sheet_number, edge_coordinates, project_image)
            cv2.imwrite('./log_files/{}'.format('target.png'), project_image)
            supporting_functions.log_writer([username, sheet_number + "_shown_with_answer", img_name])
            print("Answers have been projected. Please select the below options to continue.")
            print("1. Manual amend the sheet number")
            print("2. Hide the answers")
            print("3. Process to the next page")
            print("4. Quit")
            selection = input("Enter selection and then press the ENTER key: ")
            while True:
                if selection == "1":
                    sheet_number = worksheet_ocr.sheet_number_exception()
                    project_image = blank_image.copy()  # frame.copy()
                    project_image = answer_projection.define_range(default_parameters, sheet_number, edge_coordinates, project_image)
                    cv2.imwrite('./log_files/{}'.format('target.png'), project_image)
                    dummy = input("Answers have been projected. Please press the ENTER key once finished.")
                    break
                elif selection == "2":
                    cv2.imwrite('./log_files/{}'.format('target.png'), blank_image)
                    input("Press the ENTER key to switch back.")
                    cv2.imwrite('./log_files/{}'.format('target.png'), project_image)
                    dummy = input("Enter '1' to process to the next page.")
                    if dummy == "1":
                        break
                elif selection == "3":
                    break
                elif selection == "4":
                    supporting_functions.log_writer([username, "Ended Grading", " "])
                    print(username, "logged out.")
                    supporting_functions.log_writer([username, "Logout", " "])
                    escape = True
                    break
                else:
                    selection = input("That's not a valid option. Please enter again: ")
            supporting_functions.log_writer([username, sheet_number + "_closed", img_name])
            supporting_functions.quit_program(escape)
    cam.release()
    supporting_functions.log_writer([username, "Ended Grading", " "])
    supporting_functions.log_writer([username, "Logout", " "])
    exit()


if __name__ == "__main__":
    main()
