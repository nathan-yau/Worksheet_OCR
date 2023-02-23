import cv2
from supporting_functions import log_writer


def setup_cam(sol, username):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, sol[1])
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, sol[0])
    cam.set(cv2.CAP_PROP_FPS, 100)
    win_name = "Grading Math Worksheets"
    ret, frame = cam.read()
    print(frame.shape[0], frame.shape[1])
    if frame.shape[0] == 720 and frame.shape[1] == 1280:
        rotate = True
    else:
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, sol[1])
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, sol[0])
        win_name = "Grading Math Worksheets"
        ret, frame = cam.read()
        if frame.shape[0] == 1280 and frame.shape[1] == 720:
            rotate = False
        else:
            print("")
            print("Document scanner not supported. 1280 x 720 required. Current resolution: "+str(frame.shape[0])+" x "+str(frame.shape[1]))
            log_writer([username, "Resolution Error: "+str(frame.shape[0])+" x "+str(frame.shape[1]), " "])
            log_writer([username, "Logout", " "])
            exit()
    log_writer([username, "Scanner Initialized", " "])
    return cam, win_name, rotate
