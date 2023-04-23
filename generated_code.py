import uiautomator2 as u2

# Connect to device
d = u2.connect('38534a424c453098')

# Open YouTube app
d.app_start('com.google.android.youtube', 'com.google.android.youtube.HomeActivity')

# Tap on profile picture
d(resourceId="com.google.android.youtube:id/avatar").click()

# Select "Settings" from dropdown menu
d(text="Settings").click()

# Scroll down to "Autoplay" and toggle switch to turn it on
d(scrollable=True).scroll.to(text="Autoplay")
d(text="Autoplay").right(className="android.widget.Switch").click()

# Choose to play on both Wi-Fi and mobile data
d(text="On Wi-Fi only").click()
d(text="On Wi-Fi and mobile data").click()