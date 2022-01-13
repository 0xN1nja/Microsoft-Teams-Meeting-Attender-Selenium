# Microsoft Teams Meeting Attender
A Bot To Attend Meetings On Microsoft Teams (Modified Version Of https://github.com/teja156/microsoft-teams-class-attender)
# Installation
### Clone Repository
```bash
git clone https://github.com/0xN1nja/Microsoft-Teams-Meeting-Attender-Selenium.git
```
### Install Required Modules
```bash
pip install -r requirements.txt
```
# Usage
# Step 1 (Install And Add Chrome Driver Path)
#### Install Chrome Driver (https://chromedriver.chromium.org/) According To Your Chrome Version
## How To Add Chrome Driver Path?
#### Open `main.py` (Line 42)
```python
CHROME_DRIVER_PATH=r"" # Add Chome Driver Path (Download From https://chromedriver.chromium.org/ According To Your Chrome Version)
```
### For Example (Line 42)
```python
CHROME_DRIVER_PATH=r"C:\Users\Abhimanyu\chrome_driver.exe" # Add Chome Driver Path (Download From https://chromedriver.chromium.org/ According To Your Chrome Version)
```
# Step 2 (Add Your Credentials)
#### Go To Line 46 And Add Your Credentials
```python
USER_CREDS={"email":"","password":""} # Add Your Credentials
```
### For Example (Line 46)
```python
USER_CREDS={"email":"xyz@xyz.com","password":"xyz"} # Add Your Credentials
```
# Step 3 (Add Your Time Table)
## How To Add Your Time Table?
#### Add Start Time (string)

#### Add Class Name (string)

#### Add Class Start Time (string)

#### Add Leaving Time (string)
```python
schedule.every().monday.at("start time").do(join_class,"class name","start time","leaving time")
```
### For Example (Line 148)
```python
schedule.every().monday.at("10:00").do(join_class,"IT","10:05","11:00")
```
## How To Duplicate Tasks?

### For Example
```python
schedule.every().monday.at("10:00").do(join_class,"IT","10:05","11:00")
schedule.every().monday.at("11:05").do(join_class,"Maths","11:10","12:00")
```
## How To Schedule Class On Other Days?

#### You Can Add Days Like This 
```python
schedule.every().dayname.at("start time").do(join_class,"class name","start time","leaving time")
```
### For Example 
```python
schedule.every().thursday.at("start time").do(join_class,"class name","start time","leaving time")
```
# Step 4 (Add Webhook URL)
## How To Notify On Discord?
#### Go To Line 43 And Add Webhook URL
```python
WEBHOOK_URL="" # Add Your Webhook URL
```
### For Example (Line 43)
```python
WEBHOOK_URL="https://discord.com/api/webhooks/xyz" # Add Your Webhook URL
```
# Step 5 (Run)
#### Start The Bot
```bash
python main.py
```
# Configure
## How To Join Class Muted?
### For Example (Line 31)
```python
opt.add_argument("--mute-audio") # Mute Audio While Joining Class
```
## How To Run Browser In An Invisible Window?
### For Example (Line 32)
```python
opt.add_argument("--headless") # Uncomment This To Run Browser In An Invisible Window
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
