"""
Modified Version Of Microsoft Teams Class Attender (https://github.com/teja156/microsoft-teams-class-attender/)
Author : Abhimanyu Sharma
GitHub : https://github.com/N1nja0p
"""
"""
Events :
no-join-button : Join Button Not Found
joined-successfully : Joined Class Successfully
left-class : Left Class Successfully
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from discord_webhooks import DiscordWebhooks
import time
import schedule
import datetime
import logging
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_argument("--mute-audio") # Mute Audio While Joining Class
# opt.add_argument("--headless") # Uncomment This To Run Browser In Invisible Window
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })
DEBUG=True
driver=webdriver.Chrome(executable_path=r"chromedriver.exe",options=opt)
# Fill Your Credentials :
USER_CREDS={"email":"","password":""}
def login(email,password):
    driver.get("https://teams.microsoft.com")
    WebDriverWait(driver,1000000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="i0116"]')))
    email_field=driver.find_element_by_xpath('//*[@id="i0116"]').send_keys(email)
    email_submit=driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    WebDriverWait(driver,10000000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="i0118"]')))
    password_field=driver.find_element_by_xpath('//*[@id="i0118"]').send_keys(password)
    sign_in=driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    WebDriverWait(driver,10000000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="idSIButton9"]')))
    stay_signed_in=driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    print("Login Success")
def join_class(class_name,start_time,end_time):
    WebDriverWait(driver,100000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="personDropdown"]')))
    try_time = int(start_time.split(":")[1]) + 15
    try_time = start_time.split(":")[0] + ":" + str(try_time)
    class_list_in_grid_span=driver.find_elements_by_class_name("name-channel-type")
    for i in class_list_in_grid_span:
        if class_name.lower() in i.get_attribute("innerHTML").lower():
            i.click()
        else:
            print("Invalid Class Name.")
    time.sleep(5)
    # If Class Name In Span, Find Join Button
    try:
        join_button=driver.find_element_by_class_name("ts-calling-join-button")
        join_button.click()
    except:
        i=0
        MAX_SEARCHING_TIME=15
        while i<MAX_SEARCHING_TIME:
            print("Join Button Not Found, Refreshing.")
            driver.refresh()
            join_class(class_name,"","")
            i+=1
        print(f"Join Button Not Found After Searching {MAX_SEARCHING_TIME} Minutes.")
        notify("no-join-button",class_name,start_time,end_time)
    # Clicked On Join Button, Now Click On Disable Microphone And Disable Video
    print(f"Joining {class_name} Class!")
    time.sleep(5)
    video=driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
    video_title=video.get_attribute("title").lower()
    if video_title == "turn camera off":
        video.click()
    time.sleep(4)
    microphone=driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
    microphone_title=microphone.get_attribute("title").lower()
    if microphone_title == "mute microphone":
        microphone.click()
    time.sleep(4)
    join_now_button=driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
    time.sleep(2)
    join_now_button.click()
    print(f"Successfully Joined {class_name.title()} Class!")
    notify("joined-successfully",class_name,start_time,end_time)
    class_time=datetime.strptime(end_time,"%H:%M") - datetime.strptime(start_time,"%H:%M")
    time.sleep(class_time.seconds)
    driver.find_element_by_class_name("ts-calling-screen").click()
    driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
    print(f"Left {class_name} Class!")
    notify("left-class",class_name,start_time,end_time)
def notify(event,class_name,join_time,leaving_time):
    # Add Your Webhook URL :
    WEBHOOK_URL=""
    webhook=DiscordWebhooks(WEBHOOK_URL)
    webhook.set_footer(text="--Abhimanyu Sharma")
    if event=="joined-successfully":
        webhook.set_content(title="Class Joined Successfully!")
        webhook.add_field(name="Class Name",value=class_name.title())
        webhook.add_field(name="Status",value="Joined Class")
        webhook.add_field(name="Join Time",value=join_time)
        webhook.add_field(name="Leaving Time",value=leaving_time)
    if event=="left-class":
        webhook.set_content(title="Class Left Successfully!")
        webhook.add_field(name="Class Name",value=class_name.title())
        webhook.add_field(name="Status",value="Left Class")
        webhook.add_field(name="Join Time",value=join_time)
        webhook.add_field(name="Leaving Time",value=leaving_time)
    if event=="no-join-button":
        webhook.set_content(title="No Join Button Found!",description=f"Seems Like There Is No {class_name.title()} Today.")
        webhook.add_field(name="Class Name",value=class_name.title())
        webhook.add_field(name="Status",value="No Join Button Found")
        webhook.add_field(name="Join Time",value=join_time)
        webhook.add_field(name="Leaving Time",value=leaving_time)
    webhook.send()
    print("Information Sent To Discord!")
if __name__ == "__main__":
    login(USER_CREDS["email"],USER_CREDS["password"])
    # Add Your Own Timetable (Duplicate Tasks) :
    # Format : 24h // 00:00
    # Schedule For Monday
    schedule.every().monday.at("start time").do(join_class,"class name","start time","leaving time")
    # Schedule For Tuesday
    schedule.every().tuesday.at("start time").do(join_class,"class name","start time","leaving time")
    # Schedule For Wednesday
    schedule.every().wednesday.at("start time").do(join_class,"class name","start time","leaving time")
    # Schedule For Thursday
    schedule.every().thursday.at("start time").do(join_class,"class name","start time","leaving time")
    # Schedule For Friday
    schedule.every().friday.at("start time").do(join_class,"class name","start time","leaving time")
    # Schedule For Saturday
    schedule.every().saturday.at("start time").do(join_class,"class name","start time","leaving time")
    # Run Pending Tasks
    while True:
        schedule.run_pending()
        time.sleep(1)