import uiautomator2 as u2

from src.dump_ui import dump_ui_with_connection, extract_meta

# Connect to device
d = u2.connect('38534a424c453098')

# Open YouTube app
d.app_start('com.google.android.youtube', 'com.google.android.youtube.HomeActivity')

# Tap on profile picture
ui_res = dump_ui_with_connection(d)
ui_res = extract_meta(ui_res)
ui_res = [str(i + 1) + ':' + str(d) for i, d in enumerate(ui_res)]
template = 'I want to design a element to represent ' \
           '"profile picture"' \
           'for my Youtube application. ' \
           'I have following UI element candidates. ' \
           'Suggest top three most related elements. ' \
           'Only return the candidate index' \
           'Candidate Elements:\n' \
            + ';\n'.join(ui_res)
print(template + '\n\n\n')
# tell the APP name; filter out unrelated
d(resourceId="com.google.android.youtube:id/mobile_topbar_avatar").click()


# Select "Settings" from dropdown menu
ori_ui_res = dump_ui_with_connection(d)
ui_res = extract_meta(ori_ui_res)
ui_res = [str(d) for d in ui_res]
template = 'I want to design a element to represent ' \
           '"Settings" element' \
           'for my Android application. ' \
           'I have following UI element candidates. ' \
           'Suggest one most suitable. ' \
           'Candidate Elements:\n' \
            + '\n'.join(ui_res)
print(template + '\n\n\n')
d(text="Settings").click()

# Scroll down to "Autoplay" and toggle switch to turn it on
d(scrollable=True).scroll.to(text="Autoplay")
d(text="Autoplay").click()

# Choose to play on both Wi-Fi and mobile data
d(text="On Wi-Fi only").click()
d(text="On Wi-Fi and mobile data").click()