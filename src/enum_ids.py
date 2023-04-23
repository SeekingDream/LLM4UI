import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element_attr(element, attr_name="resourceId"):
    try:
        element_attr = element.get_attribute(attr_name)
        return element_attr
    except:
        return None


def enumerate_ids(desired_caps):
    server_url = "http://localhost:4723/wd/hub"
    # Connect to the app using Appium
    driver = webdriver.Remote(server_url, desired_caps)
    current_activity = driver.current_activity
    print(current_activity)

    time.sleep(5)
    root_element = driver.find_element(by='xpath', value='//*')

    son_elements = root_element.find_elements(by='xpath', value='//*')
    son_element_ids = []

    for son_element in son_elements:
        son_element_id = get_element_attr(son_element, 'resource-id')
        if son_element_id:
            son_element_ids.append(son_element_id)

    driver.quit()

    return son_element_ids


def get_elements_of_current_driver(driver):
    root_element = driver.find_element(by='xpath', value='//*')

    son_elements = root_element.find_elements(by='xpath', value='//*')
    son_element_ids = []

    for son_element in son_elements:
        son_element_id = get_element_attr(son_element, 'resource-id')
        if son_element_id:
            son_element_ids.append(son_element_id)

    driver.quit()
    return son_element_ids



def enumerate_all_activities(desired_caps):
    server_url = "http://localhost:4723/wd/hub"
    # Connect to the app using Appium
    driver = webdriver.Remote(server_url, desired_caps)

    time.sleep(5)
    app_activities = driver.execute_script('mobile: deepLinks', {'package': 'com.google.android.youtube'})
    for activity in app_activities:
        print(activity)

    driver.quit()


if __name__ == '__main__':
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "10",
        "deviceName": "38534a424c453098",
        "appPackage": "com.google.android.youtube",
        "appActivity": "com.google.android.youtube.HomeActivity",
        "noReset": True
    }

    tmp = enumerate_ids(desired_caps)
    for t in tmp:
        print(t)