# helper\WindowCapture.py
import numpy as np
import win32con
import win32gui
import win32ui
import win32process

from helper.CustomHelper import CustomHelper


class WindowCapture:
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # ==============================================================================
    def __init__(self, window_name=None):
        # ==========================================================================

        self.hwnd = win32gui.FindWindow(None, window_name)

        if not self.hwnd:
            print('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    # ==============================================================================
    def get_screenshot(self):
        # ==============================================================================

        # get the window image data
        w_dc = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(w_dc)
        c_dc = dcObj.CreateCompatibleDC()
        data_bitmap = win32ui.CreateBitmap()
        data_bitmap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        c_dc.SelectObject(data_bitmap)
        c_dc.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signed_ints_array = data_bitmap.GetBitmapBits(True)
        img = np.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        c_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, w_dc)
        win32gui.DeleteObject(data_bitmap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)

        return img

    @staticmethod
    def find_ros_window_names():
        import psutil
        rb_window_text_list = []

        def enum_windows_proc(hwnd, lparam):
            temp_window_text = win32gui.GetWindowText(hwnd)
            if len(temp_window_text) > 0 and win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                origin_file_name = CustomHelper.get_windows_app_origin_file_name(psutil.Process(pid).exe())
                if origin_file_name == "RoS-BoT.exe":
                    rb_window_text_list.append(str(temp_window_text))
                    print(str(temp_window_text))

        win32gui.EnumWindows(enum_windows_proc, 0)
        return rb_window_text_list;
