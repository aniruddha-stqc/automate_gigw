import datetime
import os
import platform

time_start = datetime.datetime.now()
target_website = "https://www.w3schools.com/python/ref_string_split.asp"
is_linux = "Linux" in platform.platform()
if is_linux:
    gecko_path = "./geckodriver"
else:
    gecko_path = "./geckodriver.exe"
test_log = ""
# test_log = "logs/test_log_" + time_start.strftime("%S") + ".xlsx"
time_wait = 60
