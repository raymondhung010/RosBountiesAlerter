# main.py
from helper import WindowCapture
import cv2 as cv

# ==============================================================================
if __name__ == '__main__':
    # =============================================================================
    """
        main method 
    """
    rbWindowText = WindowCapture.find_ros_window_names()
    # debug mode will be in the first position
    # debug mode window text always be 10 random string
    if len(rbWindowText) != 0 and len(rbWindowText[0]) == 10:
        w = WindowCapture(rbWindowText[0])
        screenshot = w.get_screenshot()
        pre_crop_h, pre_crop_w = screenshot.shape[:2]
        crop_screenshot = screenshot[60:round(pre_crop_h / 2), 0:round(pre_crop_w / 3)]
        (cropped_h, cropped_w) = crop_screenshot.shape[:2]
        img = cv.resize(crop_screenshot, (cropped_w * 2, cropped_h * 2))
        cv.imshow("resize", img)
        cv.imwrite("test2.png", img)
        cv.waitKey(0)

