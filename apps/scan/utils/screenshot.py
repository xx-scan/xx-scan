import subprocess
from subprocess import Popen


## https://github.com/sethsec/celerystalk/blob/7ac6c1e663cd4ae9b43cec4d2ce78d26f35c8a13/lib/utils.py

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from pyvirtualdisplay import Display
import os
import re
import time
from timeit import default_timer as timer


def take_screenshot(urls_to_screenshot,task_id,ip,scan_output_base_file_dir, workspace,command_name,populated_command):
    path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(lib.scan.__file__)), ".."))
    audit_log = path + "/log/cmdExecutionAudit.log"
    f = open(audit_log, 'a')
    start_time = time.time()
    start_time_int = int(start_time)
    start_ctime = time.ctime(start_time)
    start = timer()

    display = Display(visible=0, size=(800, 600))
    display.start()
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(firefox_options=options)
    pid = driver.service.process.pid
    print(pid)
    # db.update_task_status_started("STARTED", task_id, pid, start_time_int)

    for url,output in urls_to_screenshot:
        try:
            #driver = webdriver.Firefox(firefox_options=options)
            # capture the screen
            driver.get(url)
            print("Taking screenshot of [{0}]".format(url))
            screenshot = driver.save_screenshot(output)
        except WebDriverException as  e:
            #print('exception: {0}'.format(e))
            print("Error taking screenshot of [{0}]".format(url))
        except Exception as  e:
            print('exception: {0}'.format(e))
            #print(type(e).__name__)
        # finally:
        #     driver.quit()
    driver.quit()
    display.stop()
    end = timer()
    end_ctime = time.ctime(end)
    run_time = end - start
    # db.update_task_status_completed("COMPLETED", task_id, run_time)
    # f.write("\n[-] CMD COMPLETED in " + str(run_time) + " - " + populated_command + "\n")
    f.write("\n" + str(start_ctime) + "\t" + str(end_ctime) + "\t" + str(
        "{:.2f}".format(run_time)) + "\t" + command_name + "\t" + populated_command)
    f.close()
