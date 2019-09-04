import threading

import globals
import webscrap_contrast
import webscrap_css
import webscrap_html
import webscrap_spell


def execute():
    # creating thread
    thread_spell = threading.Thread(target=webscrap_spell.execute)
    thread_html = threading.Thread(target=webscrap_html.execute)
    thread_css = threading.Thread(target=webscrap_css.execute)
    thread_contrast = threading.Thread(target=webscrap_contrast.execute)

    # starting thread 1
    thread_spell.start()
    thread_html.start()
    thread_css.start()
    thread_contrast.start()

    thread_spell.join()
    thread_html.join()
    thread_css.join()
    thread_contrast.join()

    print("Done")

if __name__ == '__main__':
    execute()
