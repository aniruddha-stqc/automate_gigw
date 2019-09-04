import datetime
import os
import threading

import globals
import webscrap_contrast
import webscrap_css
import webscrap_html
import webscrap_spell


def execute():
    script_name = os.path.basename(__file__)
    print(script_name + " : " + "Launching GIGW Test Suite in Selenium Gecko Browser headlessly")

    # creating thread
    thread_spell = threading.Thread(target=webscrap_spell.execute)
    thread_html = threading.Thread(target=webscrap_html.execute)
    thread_css = threading.Thread(target=webscrap_css.execute)
    thread_contrast = threading.Thread(target=webscrap_contrast.execute)

    thread_spell.start()
    thread_html.start()
    thread_css.start()
    thread_contrast.start()

    thread_spell.join()
    thread_html.join()
    thread_css.join()
    thread_contrast.join()


if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    execute()
    print(script_name + " : " + "Finished in " + str(
        (datetime.datetime.now() - globals.time_start).total_seconds()) + " seconds")
