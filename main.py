"""Runs FIFA's config/launcher, presses enter, then closes the launcher. Run from same dir as FIFA's executable"""

from os import path, listdir
import re
import wmi
import win32gui
import win32process
import win32com.client


def main():
    # Init
    c = wmi.WMI()
    shell = win32com.client.Dispatch("WScript.Shell")

    # Detecting fifa executable
    print "Looking for FIFA executable..."
    fifa_file = ""
    found_fifa = False
    for file in listdir('.'):
        if re.match('fifa[0-9]+.exe', file):
            found_fifa = True
            fifa_file = path.join(path.dirname(__file__), file)

    if not found_fifa:
        print "Unable to find FIFA executable, please run from the same directory as fifa*.exe"
        return 1

    # Run FIFA config/launcher
    print("Running FIFA config/launcher...")
    shell.run(fifa_file)

    # Get the HWND and PID of FIFA config/launcher
    config_hwnds = []
    config_process = None
    print("Waiting for config/launcher to load...")
    while len(config_hwnds) != 1:
        for process in c.Win32_Process(name="fifaconfig.exe"):
            config_hwnds = get_hwnds_for_pid(process.ProcessID)
            config_process = process

    # Give FIFA config/launcher focus
    win32gui.SetForegroundWindow(config_hwnds[0])

    print("Running FIFA...")
    # Send an 'Enter' keypress
    shell.SendKeys('{ENTER}', 0)

    print("Waiting for FIFA to load...")
    # Wait for FIFA proper to load, then kill the config/launcher
    while True:
        if len(c.Win32_Process(name=fifa_file)) > 0:
            print "Killing config/launcher..."
            config_process.Terminate()

            print "All done. Cheers Jeff!"
            return 0


# Credit: Tim Golden - http://timgolden.me.uk/python/win32_how_do_i/find-the-window-for-my-subprocess.html
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

if __name__ == "__main__":
    main()
