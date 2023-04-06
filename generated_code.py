import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

desired_caps = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "appPackage": "com.google.android.youtube",
    "appActivity": "com.google.android.apps.youtube.app.WatchWhileActivity",
    "noReset": True
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

time.sleep(5)

search_button = driver.find_element(MobileBy.ID, "com.google.android.youtube:id/menu_search")
search_button.click()

time.sleep(2)

search_box = driver.find_element(MobileBy.ID, "com.google.android.youtube:id/search_edit_text")
search_box.send_keys("dota2")

time.sleep(2)

search_box.send_keys(u'\ue007')

time.sleep(5)

driver.quit()
