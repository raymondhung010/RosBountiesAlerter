# helper\CustomHelper.py

class CustomHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_windows_app_origin_file_name(f_name):
        import win32api
        lang, codepage = win32api.GetFileVersionInfo(f_name, '\\VarFileInfo\\Translation')[0]
        str_info_path = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, 'OriginalFilename')
        return str(win32api.GetFileVersionInfo(f_name, str_info_path))
