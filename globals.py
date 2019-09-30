import datetime

time_start = datetime.datetime.now()
target_website = "https://www.india.gov.in/"
gecko_path = "./geckodriver"
test_log = "logs/test_log_" + time_start.strftime("%s") + ".xlsx"
time_wait = 30
