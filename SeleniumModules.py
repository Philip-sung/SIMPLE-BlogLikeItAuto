from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip as pp
import time
import random
import os


# Path for Chrome Driver
driverFolder : str= os.getcwd()+'/selenium/chromedriver.exe'

# Number of Liked Post & Ceased Posts
clickedLikeNum : int = 0
stopTagNum = 0

# Delay
## Default Delay
defaultDelayMin : float = 1.0
defaultDelayMax : float = 2.0
## Delay for Scroll while searching posts
ScrollDelayMin : float = 0.5
ScrollDelayMax : float = 1.0
## Delay for Key Input
keyInputDelayMin : float = 0.5
keyInputDelayMax : float = 1.0
## Delay for Scroll while READING Post
likeminPauseTime : float = 0.5
likemaxPauseTime : float = 1.0
## Long Term Delay for Test
longDelayforTest : float = 5.0


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--no-sandbox')
options.add_argument("disable-gpu")

options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome(driverFolder, options=options)

def login(yourid,yourpassword):
    driver.get("https://nid.naver.com/nidlogin.login?svctype=262144&url=http://m.naver.com/aside/")
    inputkeys(yourid, "아이디")
    inputkeys(yourpassword, "비밀번호")
    time.sleep(random.uniform(keyInputDelayMin, keyInputDelayMax))
    driver.find_element(By.XPATH, f"//input[@placeholder='비밀번호']").send_keys(Keys.ENTER)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))

def inputkeys(myId, placeholder):
    pp.copy(myId)
    idInput = driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
    idInput.click()
    pp.copy(myId)
    time.sleep(random.uniform(keyInputDelayMin, keyInputDelayMax))
    idInput.send_keys(Keys.CONTROL, 'v')


def searchBlog(postNum : int):
    adress = "https://m.blog.naver.com/Recommendation.naver"
    driver.get(adress)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))

    articles = driver.find_elements(By.XPATH, "//div[@class='postlist__LXY3R']/a")
    numOfArticles = len(articles)
    while numOfArticles < postNum :
        articles = driver.find_elements(By.XPATH, "//div[@class='postlist__LXY3R']/a")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(ScrollDelayMin,ScrollDelayMax))
        numOfArticles = len(driver.find_elements(By.XPATH, "//div[@class='postlist__LXY3R']/a"))
    
    articles = driver.find_elements(By.XPATH, "//div[@class='postlist__LXY3R']/a")
    numOfArticles = len(articles)
    urls = []
    for i in range(numOfArticles):
        url = str(articles[i].get_attribute("href"))
        urls.append(url)
    return urls

def openBlog(url, i : int):
    driver.execute_script(f"window.open('{url}');")
    driver.switch_to.window(driver.window_handles[i])
    print("Visit : " + url)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))

def closeBlog():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def closeExcludedBlog():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("!EXIT! : Manually Excluded URL")

def availableLike():
    global stopTagNum
    try : 
        confirmlike = driver.find_element(By.XPATH, "//*[@id='body']/div[10]/div/div[1]/div/div/a").get_attribute("class").split(" ")
        if "on" in confirmlike :
            stopTagNum += 1
            print(f'Already Proceeded : {stopTagNum}')
            return False
        elif "off" in confirmlike : 
            return True
    except Exception as e: 
        print(e)
        print('No available button for LikeIT')
        return False

def clickLike():
    document_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(likeminPauseTime,likemaxPauseTime))
        now_scroll_height = driver.execute_script("return window.scrollY+window.innerHeight")
        if now_scroll_height >= document_height:
            break
        document_height = driver.execute_script("return document.body.scrollHeight")
        
    like_btn = driver.find_element(By.XPATH, "//div[@class='btn_like']/div")
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    driver.execute_script("arguments[0].scrollIntoView({block : 'center'});", like_btn)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    like_btn.click()
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    global clickedLikeNum
    clickedLikeNum += 1
    print(f"LikeIT Clicked for {clickedLikeNum} Posts.")

def clickRelatedBloggers(blogerNum : int):
    morebloger = driver.find_element(By.XPATH, "//a[@class='btn_like_more']")
    driver.execute_script("arguments[0].scrollIntoView({block : 'center'});", morebloger)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    morebloger.send_keys(Keys.ENTER)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    blogers = driver.find_elements(By.XPATH, "//div[@class='bloger_area___eCA_']/a")
    numOfBlogers = len(blogers)
    blogerurls = []
    if (blogerNum < numOfBlogers):
        numOfBlogers = blogerNum
    for i in range(numOfBlogers):
        url = str(blogers[i].get_attribute("href"))
        blogerurls.append(url)
    return blogerurls

def moveToRecentPost():
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    listView = driver.find_element(By.XPATH, "//button[@data-clickcode='pls.text']")
    listView.click()
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))
    posts = driver.find_elements(By.XPATH, "//div[@class='postlist__LXY3R']/a")
    url = str(posts[0].get_attribute("href"))
    driver.get(url)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))

    