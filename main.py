import sys
import time
from scripts import streamfare, streamfare_aljazeera, generic
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class RMCC:
    def __init__(self):
        self.useragentarr = []
        self.scripts = ['streamfare', 'err', 'twitch']
        for i in range(111, 81, -1):
            self.useragentarr.append("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                     " Chrome/{}/0.0 Safari/537.36".format(i))

    def driverConf(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument('--force-dark-mode')

        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(1920, 1200)

        return driver

    def findChromecast(self, driver):
        counter = 0
        sinks = []

        print("Looking for Chromecast device...")

        while len(sinks) < 1:
            sinks += driver.get_sinks()
            counter += 1
            time.sleep(1)

            if counter > 20:
                print('Failed to find device.')
                sys.exit(2)

        name = sinks[0]['name']
        print(f"Found Chromecast {name}")
        if 'session' in sinks[0]:
            print(f'Chromecast is busy with \'{sinks[0]["session"]}\'. Killing it.')
            driver.stop_casting(name)
            return name
        else:
            return name

    def findScript(self, url):
        for site in self.scripts:
            if site in url:
                return site
            else:
                return 'generic'


    def main(self):
        # URL comes from Queue
        url = 'https://streamfare.com/sky-news-live-stream'

        driver = self.driverConf()
        name = self.findChromecast(driver)

        print(f"Starting mirroring to {name}")
        driver.start_tab_mirroring(name)
        time.sleep(5)

        match self.findScript(url):
            case 'al-jazeera':
                user_script = Thread(target=lambda: streamfare_aljazeera.run(driver, url))
            case 'streamfare':
                user_script = Thread(target=lambda: streamfare.run(driver, url))
            case _:
                user_script = Thread(target=lambda: generic.run(driver, url))

        user_script.daemon = True  # terminates when main thread terminates
        user_script.start()



        # main thread will make sure we're still casting
        healthy = True

        # failure modes:
        #  - chromecast missing
        #  - chromecast casting someone else
        while healthy:
            time.sleep(10)

            sinks = driver.get_sinks()
            print(sinks)
            healthy = False
            for sink in driver.get_sinks():
                if (sink['name'] == name) and ('session' in sink) and (sink['session'] == 'Casting tab'):
                    print('Healthy for now')
                    healthy = True

            # if not user_script.is_alive():
            #     print("User script seems to have crashed")
            #     healthy = False

        print('Casting session no longer healthy')
        sys.exit(1)


if __name__ == '__main__':
    init = RMCC()
    init.main()
