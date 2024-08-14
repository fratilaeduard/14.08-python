import capture, filter
import threading
import time

print("Starting MAC capture in 3 seconds...")
time.sleep(3)

#start airmon and capture in a csv
capture.external_capture()

capture_file = filter.get_last_capture()

filter.generate_xlsx(capture_file)
filter.filter_teams()
# filter.reset_xlsx()

print("Done obtaining team informations.")