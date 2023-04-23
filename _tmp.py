
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Set desired capabilities
desired_caps = {
    "deviceName": "38534a424c453098",
    "platformName": "Android",
    "platformVersion": "10",
    "appPackage": "com.google.android.youtube",
    "appActivity": "com.google.android.apps.youtube.app.WatchWhileActivity",
    "noReset": True
}

# Initialize driver
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# Wait for app to load
wait = WebDriverWait(driver, 10)

try:
    profile_pic = wait.until(EC.presence_of_element_located((By.ID, "com.google.android.youtube:id/avatar")))
except TimeoutException:
    print("Profile picture element not found")
    driver.quit()
    exit()

# Tap on profile picture
TouchAction(driver).tap(profile_pic).perform()

# Tap on settings
try:
    settings_btn = wait.until(EC.presence_of_element_located((By.ID, "com.google.android.youtube:id/menu_item_settings")))
except TimeoutException:
    print("Settings button element not found")
    driver.quit()
    exit()

settings_btn.click()

# Scroll down to Autoplay and toggle switch
try:
    autoplay_switch = wait.until(EC.presence_of_element_located((By.ID, "com.google.android.youtube:id/autoplay_switch")))
except TimeoutException:
    print("Autoplay switch element not found")
    driver.quit()
    exit()

autoplay_switch_location = autoplay_switch.location
autoplay_switch_size = autoplay_switch.size
autoplay_switch_center_x = autoplay_switch_location['x'] + autoplay_switch_size['width'] / 2
autoplay_switch_center_y = autoplay_switch_location['y'] + autoplay_switch_size['height'] / 2
TouchAction(driver).long_press(x=autoplay_switch_center_x, y=autoplay_switch_center_y).wait(1000).release().perform()

# Choose Wi-Fi and mobile data option
try:
    wifi_and_mobile_data_option = driver.find_element_by_xpath("//android.widget.CheckedTextView[@text='On Wi-Fi and mobile data']")
except NoSuchElementException:
    print("Wi-Fi and mobile data option element not found")
    driver.quit()
    exit()

wifi_and_mobile_data_option.click()

# Quit driver
driver.quit()
