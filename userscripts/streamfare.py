import time
from selenium.webdriver.common.action_chains import ActionChains


def run(driver, url):
    driver.get(url)
    time.sleep(5)
    action = ActionChains(driver)

    # Agree to cookies
    action.move_by_offset(1120, 678)
    action.click()
    action.perform()
    action.move_by_offset(-1120, -678)

    # Start the player
    time.sleep(2)
    action.move_by_offset(926,458)
    action.click()
    action.perform()
    action.move_by_offset(-926, -458)

    # Fullscreen the player
    time.sleep(2)
    action.move_by_offset(1263, 566)
    time.sleep(2)
    action.click()
    action.perform()
    action.move_by_offset(-1263, -566)