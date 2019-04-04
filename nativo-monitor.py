#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import json
import subprocess
import logging

#Globals
urls = []
driver = []

#_extension_path = ('%s/chrome_extension.crx' % (os.path.dirname(os.path.realpath(__file__))))
_json_path = (r'%s/bookmarks_kibana.json' % (os.path.dirname(os.path.realpath(__file__))))
_executable_path = '/usr/local/bin/chromedriver'
_embed = '&embed=true'

#logging
logger = logging.getLogger()

#Google Chrome settings
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--app=http://google.com")
#chrome_options.add_extension(_extension_path)

#function for elastic 5 URL
def elastic_stack_5(i, checked=None):
    time.sleep(15)
    remove_element_kibana_filter = driver[i].find_element_by_class_name('filter-bar')
    driver[i].execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", remove_element_kibana_filter)
    remove_element_kibana_panel = driver[i].find_element_by_class_name('panel-heading')
    driver[i].execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", remove_element_kibana_panel)
    time.sleep(2)

#function for Elastic 6 URL
def elastic_stack_6(i, checked=None):
    remove_element_fullscreen_button = driver[i].find_element_by_class_name('dshExitFullScreenButton__logo')
    remove_element_fullscreen_text = driver[i].find_element_by_class_name('dshExitFullScreenButton__text')
    driver[i].execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", remove_element_fullscreen_button)
    driver[i].execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", remove_element_fullscreen_text)

#function for Elastic Canvas URL
def elastic_stack_canvas(i, checked=None):
    time.sleep(30)
    driver[i].find_elements_by_class_name('euiButtonEmpty__text')[0].click()
    time.sleep(3)
    driver[i].find_elements_by_class_name('euiFlexItem')[25].click()
    time.sleep(5)
    remove_element_kibana_filter = driver[i].find_element_by_class_name('coreSystemRootDomElement')
    driver[i].execute_script("arguments[0].setAttribute('class','coreSystemRootDomElement canvas-isFullscreen')", remove_element_kibana_filter)
    time.sleep(15)

# Parse URL from JSON file
def chrome_bookmarks(path, checked=None):

    if not checked:
        checked = []

    checked.append(path)
    if path['type'] == 'folder':
        for n in path['children']:
            if n['type'] == 'url' and n['url'] !='':
                checked.append(n['url'])
                urls.append(n['url'])

            elif n['type'] == 'folder':
                for child in n['children']:
                    chrome_bookmarks(child, checked)
    elif path['type'] == 'url':
        urls.append(path['url'])

# Create multiple Selenium instances
def create_instances(self, checked=None):
    i = 0
    for i in range(0,len(urls)):
        if ("prod" in urls[i]):
            driver.append(webdriver.Chrome(executable_path=_executable_path, options=chrome_options))
            time.sleep(5)
        else:
            continue

# Load URL into Instances
def load_instances(self,checked=None):
    i=0
    for i in range(0,len(urls)):
        print(urls[i])
        if "URL NAME HERE" in urls[i]:
            driver[i].get(urls[i])
            time.sleep(10)
            driver[i].find_elements_by_class_name('kuiLocalMenuItem')[0].click()
            elastic_stack_6(i=i)
        if "URL NAME HERE" in urls[i]:
            driver[i].get(urls[i] + _embed)
            elastic_stack_5(i=i)
        if "URL NAME HERE" in urls[i]:
            driver[i].get(urls[i])
            elastic_stack_canvas(i=i)
        else:
            continue
        i += 1
    time.sleep(10)

# Rotate Instances
def rotate_instances(self, checked=None):
    refresh_timer = 0
    while True:
        for i in range(0, len(driver)):
            driver[i].switch_to.window(driver[i].window_handles[0])
            time.sleep(30)
            refresh_timer = refresh_timer + 1
            if refresh_timer == 30:

                # Refreshing instances
                for i in range(0, len(driver)):
                    driver[i].switch_to.window(driver[i].window_handles[0])
                    i -= 1
                    time.sleep(2)
                    driver[i].refresh()
                    if "URL NAME HERE" in urls[i]:
                        time.sleep(10)
                        elastic_stack_6(i=i)
                    if "URL NAME HERE" in urls[i]:
                        elastic_stack_5(i=i)
                    if "URL NAME HERE" in urls[i]:
                        elastic_stack_canvas(i=i)
                    else:
                        continue
                    time.sleep(15)
                refresh_timer = 0

#Main Function
def main():
    with open(_json_path, 'r') as data:
        result = json.load(data)
    root = result['roots']['bookmark_bar']

    chrome_bookmarks(root)
    create_instances(urls)
    load_instances(urls)
    rotate_instances(driver)

if __name__ == "__main__":
    main()
