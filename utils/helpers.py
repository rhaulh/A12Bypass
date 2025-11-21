# utils/helpers.py
import subprocess
import os
import sys
import ctypes

def run_subprocess_no_console(cmd, timeout=30, capture_output=True):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0
    creationflags = subprocess.CREATE_NO_WINDOW

    result = subprocess.run(
        cmd,
        startupinfo=startupinfo,
        creationflags=creationflags,
        stdout=subprocess.PIPE if capture_output else subprocess.DEVNULL,
        stderr=subprocess.PIPE if capture_output else subprocess.DEVNULL,
        stdin=subprocess.PIPE,
        timeout=timeout,
        text=capture_output
    )
    return result

def get_lib_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, 'libs', filename)

def hide_console():
    if sys.platform == "win32":
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
            ctypes.windll.kernel32.CloseHandle(whnd)