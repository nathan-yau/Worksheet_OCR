import cv2
from supporting_functions import log_writer
from supporting_functions import quit_program
from datetime import datetime
import tkinter as tk


def setup_cam(handler):
    resolution = [1138, 640]
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cam.set(cv2.CAP_PROP_FPS, 100)
    win_name = "Grading Math Worksheets"
    ret, frame = cam.read()
    if frame is None:
        tk.messagebox.showinfo(title="Camera Error", message="Please check if the document scanner is attached!")
        quit_program(True)
    if frame.shape[0] == 720 and frame.shape[1] == 1280:
        rotate = True
    else:
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        win_name = "Grading Math Worksheets"
        ret, frame = cam.read()
        if frame.shape[0] == 1280 and frame.shape[1] == 720:
            rotate = False
        else:
            tk.messagebox.showinfo(title="Resolution Error",
                                   message="Document scanner not supported. 1280 x 720 required. "
                                           "Current resolution: "+str(frame.shape[0])+" x "+str(frame.shape[1]))
            log_writer([handler, "Resolution Error: "+str(frame.shape[0])+" x "+str(frame.shape[1]), " "])
            log_writer([handler, "Logout", " "])
            exit()
    log_writer([handler, "Scanner Initialized", " "])
    return cam, win_name, rotate


def capturing_image(cam, win_name, rotate, handler, dummy_image):
    while True:
        ret, frame = cam.read()
        if rotate is True:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        try:
            frame_copy = frame.copy()
        except AttributeError:
            print("\n" + "*" * 50 + "\nCamera ejected from computer! Please check!\n" + "*" * 50)
            quit_program(True)
        cv2.imwrite('./log_files/{}'.format('target.png'), dummy_image)
        if not ret:
            print("Please check if the document scanner is attached.")
            break
        cv2.imshow(win_name, frame)
        cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Closing the Document Scanner...")
            log_writer([handler, "Scanner Closed", " "])
            img_name = ""
            cam.release()
            cv2.destroyAllWindows()
            print(img_name)
            break
        elif k % 256 == 32:
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            img_name = "{}.png".format(ts)
            log_writer([handler, "Image Capture", img_name])
            cv2.imwrite('./log_files/image_backup/{}'.format(img_name), frame)
            break
    dummy_image = frame.copy()
    cv2.destroyAllWindows()
    return dummy_image, frame_copy, img_name

