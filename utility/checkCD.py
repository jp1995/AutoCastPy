import os
from utility.logging_setup import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def checkCD():
    if os.name == 'posix':
        executable = 'chromedriver'
    else:
        executable = 'chromedriver.exe'

    if executable not in os.listdir():
        log.error('Chromedriver is missing. Download it and put in the AutoCastPy directory.')
        return False

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = webdriver.ChromeService(executable_path=f'./{executable}')
    driver = webdriver.Chrome(service=service, options=options)

    bVersion = driver.capabilities['browserVersion'].split('.')[0]
    dVersion = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0].split('.')[0]
    driver.quit()

    if bVersion != dVersion:
        log.info(f'Major version mismatch\n'
                 f'Chromedriver version {dVersion}\n'
                 f'Chrome version {bVersion}\n')
        return False
    else:
        log.info('Driver version matches Chrome version, continuing\n')
        return executable
