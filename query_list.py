
# dumpsys window displays | grep -E mCurrentFocus

QUERY_LIST = [
    # {
    #     'app_name': 'youtube',
    #     'init_prompt': 'what do I need to do to turn on the Autoplay on Youtube app'
    # },

    {
        'appPackage': 'com.neumorphic.calculator',
        'appActivity': 'com.neumorphic.calculator.MainActivity',
        'init_prompt': 'I have installed calculator on my Android devices. '
                       'what do I need to do to use the calculator App to compute '
                       '10 + 10 * 20'
    },

    {
        'appPackage': 'com.github.axet.bookreader',
        'appActivity': 'com.github.axet.bookreader.activities.MainActivity',
        'init_prompt': 'I have installed Book Reader App on my Android devices. '
                       'what do I need to do to search the "i-20.pdf" file on my phone'
                       'and open it'
    },

    {
        'appPackage': 'livio.rssreader',
        'appActivity': 'livio.rssreader.RSSReader',
        'init_prompt': 'I have installed News Reader App on my Android devices. '
                       'what do I need to do to open the third news'
    },

    {
        'appPackage': 'com.vimeo.android.videoapp',
        'appActivity': 'com.vimeo.android.videoapp.MainActivity',
        'init_prompt': 'I have installed Vimeo App on my Android devices. '
                       'what do I need to do to search the video "dota" '
                       'and open the first searched results'
    },

    {
        'appPackage': 'com.hulu.plus',
        'appActivity': 'com.hulu.features.welcome.WelcomeActivity',
        'init_prompt': 'I have installed HuLu App on my Android devices. '
                        'what do I need to do to login HULU App with the'
                        'email sxc180080@utdallas.edu and the password 123456789'
    },

    {
        'appPackage': 'com.github.characterdog.bmicalculator',
        'appActivity': 'com.github.characterdog.bmicalculator.MainActivity',
        'init_prompt': 'I have installed BMI calculator on my Android devices. '
                       'What do I need to do to use the BMI calculator App to compute the '
                       'BMI with 10 inch height and 10 pounds weight'
    },


    {
        'appPackage': 'com.musictube.streammusic',
        'appActivity': 'com.musictube.streammusic.ui.MainActivity',
        'init_prompt': 'I have installed MusicTube App on my Android devices. '
                       'what do I need to do to search the "Someone like you" on MusicTube App'
    },



    # {
    #     'app_name': 'chrome',
    #     'init_prompt': 'write a python script for me to load chrome and search dota2 on Android simulator using appuim'
    # },


]