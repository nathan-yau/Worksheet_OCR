from paddleocr import PaddleOCR
import cv2
from supporting_functions import log_writer


def arrange_size(cnts_each):
    x, y, w, h = cv2.boundingRect(cnts_each)
    return w * h


def detect_edge(handler, image_tag, frame):
    edged = cv2.Canny(frame, 75, 200)
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=lambda x: arrange_size(x), reverse=True)
    x, y, w, h = cv2.boundingRect(cnts[0])
    log_writer([handler, "image_edge_detect", image_tag])
    return [x, x+w, y, h+y]


def detect_sheet_number(handler, image_tag, df, project_image, frame, edge_coordinates):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    pxs, pys = edge_coordinates[0], edge_coordinates[2]
    roi = frame[pys+10:pys+200, pxs+30:pxs+300]
    cv2.imwrite('./log_files/{}'.format('target2.png'), roi)
    result = ocr.ocr(roi, cls=True)[0]
    if len(result) > 0:
        for r in result:
            if str(r[1][0][-1]).upper() == "A" or str(r[1][0][-1]).upper() == "B" and len(
                    str(r[1][0][-1]).upper()) <= 6:
                break
        crs = str(r[1][0]).upper().strip()
        sheet_number = crs[0] + crs[1:].replace("I", "1").replace("|", "1").replace(
                "O", "0").replace("L", "1").replace("!", "1").replace(" ", "").replace(
                "J", "1").replace("H", "B").replace(".", "1").replace("'", "")
        log_writer([handler, sheet_number + "_ocr_detected", image_tag])
        validity = (sheet_number in df.shnum.values)
        if validity is False:
            log_writer([handler, "failed_sheet_number_detection", image_tag])
            sheet_number = sheet_number_exception(handler, image_tag, df)
        else:
            cv2.putText(img=project_image, text=sheet_number, org=(pxs, pys),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(255, 255, 255), thickness=3)
    else:
        sheet_number = sheet_number_exception(handler, image_tag, df)
    return sheet_number


def sheet_number_exception(handler, image_tag, df):
    while True:
        print("Failed to recognize the sheet number.")
        manuel_input = str(input("Please manually input the Sheet Number: "))
        sheet_number = manuel_input.upper()
        validity = (sheet_number in df.shnum.values)
        if validity is True:
            log_writer([handler, sheet_number + "_manual_input", image_tag])
            break
        log_writer([handler, sheet_number + "_manual_input", image_tag])
    return sheet_number
