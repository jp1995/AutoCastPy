import os
import time
import json
import importlib
from threading import Thread
from selenium import webdriver
from web.app import run_webserver
from multiprocessing import Process, Queue
from utility.checkCD import checkCD
from utility.logging_setup import log, logWipe


class RMCC:
    def __init__(self):
        self.scripts = self.loadScripts()
        self.q = Queue()
        self.webserver = Process(target=run_webserver, args=(self.q,))
        self.driver = self.driverConf()
        self.user_script = Thread
        self.status = True
        self.castID = ''
        self.mappings = {}
        self.mappings_path = 'userscripts/mapping.json'
        self.URL = ''
        self.ccName = ''

    """
    The configuration of the selenium webdriver.
    """
    @staticmethod
    def driverConf():
        opts = webdriver.ChromeOptions()
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument('--force-dark-mode')
        opts.add_argument('--headless=new')

        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(1920, 1200)

        return driver

    """
    The first Chromecast it finds is selected. If you have more Chromecasts, deal with it.
    Don't ask me why you need to run driver.get_sinks() in a loop for a while.
    """
    def findChromecast(self) -> bool:
        counter = 0
        sinks = []
        log.info("Looking for Chromecast device...")

        while len(sinks) < 1:
            sinks += self.driver.get_sinks()
            counter += 1
            time.sleep(1)
            if counter > 20:
                log.error('Failed to find device. Ensure the device is online and try again.')
                return False

        self.ccName = sinks[0]['name']
        log.info(f"Found Chromecast {self.ccName}")
        if 'session' in sinks[0]:
            log.info(f'Chromecast is busy with \'{sinks[0]["session"]}\'. Killing it.')
            self.driver.stop_casting(self.ccName)

        return True

    """
    The url-segment-to-userscript mappings are imported from the file.
    """
    def loadMappings(self):
        with open(self.mappings_path, 'r') as file:
            self.mappings = json.load(file)

    """
    Dynamically imports all the user scripts using importlib.
    """
    @staticmethod
    def loadScripts() -> dict:
        scriptsdict = {}
        for filename in os.listdir('userscripts'):
            if filename.endswith('.py'):
                script_name = filename[:-3]
                module = importlib.import_module(f'userscripts.{script_name}')
                scriptsdict[script_name] = module
        return scriptsdict

    """
    Looks at the given URL and attempts to find a matching userscript from the mappings
    """
    def findScript(self, url) -> str:
        for pattern, script_name in self.mappings.items():
            if pattern in url:
                return script_name
        return 'generic'

    """
    Starts the casting.
    """
    def beginCast(self):
        log.info(f"Starting mirroring to {self.ccName}")
        self.driver.start_tab_mirroring(self.ccName)
        self.status = True

    """
    Dynamically runs the appropriate userscript.
    Thread is used here instead of a multiprocessing Process because mom's pickle spaghetti.
    """
    def runScript(self, url):
        script = self.findScript(url)
        module = self.scripts.get(script)

        if module:
            log.info(f'Running script {script}')
            self.user_script = Thread(target=lambda: module.run(self.driver, url))
            self.user_script.daemon = True
            self.user_script.start()
        else:
            log.info(f'No script found for {url}')

    """
    The Queue is used by the webserver to communicate with the main program.
    """
    def handleQueue(self) -> bool:
        if self.q.empty():
            return False
        data = self.q.get()
        log.info(f'Received: {data}')
        self.URL = data
        return True

    """
    Checks if the program is still casting, otherwise the driver is closed as threads cannot be killed trivially.
    Unfortunately each cast does not have a unique ID, however, the selenium implementation gives
    'session' = 'Casting tab', manually casting a tab from chrome gives session = 'Mirroring Chrome' and casting an app
    from a phone gives session = 'Ready to cast', so it works.
    """
    def healthCheck(self) -> bool:
        sinks = self.driver.get_sinks()
        for sink in sinks:
            if (sink['name'] == self.ccName) and ('session' in sink) and (sink['session'] == 'Casting tab'):
                return True

        log.info('We appear to not be casting at the moment. Closing the driver.')
        self.driver.close()
        self.status = False
        return False

    """
    This is the main program loop.
    """
    def main(self):
        logWipe()
        if not checkCD():
            quit()
        self.webserver.start()
        self.loadMappings()
        minute = 0

        while True:
            time.sleep(1)
            minute += 1
            if self.handleQueue():
                self.driver = self.driverConf()
                if self.findChromecast():
                    self.beginCast()
                    self.runScript(self.URL)

            if minute == 60 and self.status:
                self.healthCheck()
                minute = 0


if __name__ == '__main__':
    init = RMCC()
    init.main()
