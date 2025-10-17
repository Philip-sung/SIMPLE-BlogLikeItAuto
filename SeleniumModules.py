from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # ★ 추가
import pyperclip as pp
import time
import random
import os
from datetime import datetime


# Path for Chrome Driver
driverFolder : str= os.getcwd()+'/selenium/chromedriver.exe'
service = Service(driverFolder)

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

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

def login(yourid, yourpassword):
    # 최신 PC 로그인 페이지로 변경
    driver.get("https://nid.naver.com/nidlogin.login")
    time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))

    # 아이디와 비밀번호 입력
    inputkeys(yourid, "아이디")
    inputkeys(yourpassword, "비밀번호")

    # 로그인 실행 (Enter 키 전송)
    time.sleep(random.uniform(keyInputDelayMin, keyInputDelayMax))
    driver.find_element(By.ID, "pw").send_keys(Keys.ENTER)
    time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))


def inputkeys(value, field):
    pp.copy(value)

    # 입력 대상 선택
    if field == "아이디":
        input_element = driver.find_element(By.ID, "id")
    elif field == "비밀번호":
        input_element = driver.find_element(By.ID, "pw")
    else:
        raise ValueError("잘못된 입력 구분입니다. (아이디/비밀번호 중 하나만 허용)")

    # 값 입력
    input_element.click()
    time.sleep(random.uniform(keyInputDelayMin, keyInputDelayMax))
    input_element.send_keys(Keys.CONTROL, 'v')


def searchBlog(postNum : int):
    adress = "https://m.blog.naver.com/Recommendation.naver"
    driver.get(adress)
    time.sleep(random.uniform(defaultDelayMin,defaultDelayMax))

    articles = driver.find_elements(By.XPATH, "//div[@class='postlist__qxOgF']/a")
    numOfArticles = len(articles)
    while numOfArticles < postNum :
        articles = driver.find_elements(By.XPATH, "//div[@class='postlist__qxOgF']/a")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(ScrollDelayMin,ScrollDelayMax))
        numOfArticles = len(driver.find_elements(By.XPATH, "//div[@class='postlist__qxOgF']/a"))
    
    articles = driver.find_elements(By.XPATH, "//div[@class='postlist__qxOgF']/a")
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
        confirmlike = driver.find_element(By.CSS_SELECTOR,"a.u_likeit_button._face").get_attribute("class").split(" ")
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
    global clickedLikeNum
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = "like_logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{today_str}_likecount.txt")

    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.startswith(f"{today_str} : "):
                    prev_count = int(content.split(":")[1].strip())
                else:
                    prev_count = 0
        except Exception:
            prev_count = 0
    else:
        prev_count = 0

    document_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(likeminPauseTime, likemaxPauseTime))
        now_scroll_height = driver.execute_script("return window.scrollY+window.innerHeight")
        if now_scroll_height >= document_height:
            break
        document_height = driver.execute_script("return document.body.scrollHeight")

    like_btn = driver.find_element(By.CSS_SELECTOR, "a.u_likeit_button._face.off")
    time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
    driver.execute_script("arguments[0].scrollIntoView({block : 'center'});", like_btn)
    time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
    like_btn.click()
    time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))

    clickedLikeNum += 1
    total_count = prev_count + 1

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"{today_str} : {total_count}")

    print(f"LikeIT Clicked for {clickedLikeNum} Posts. (Total today: {total_count})")

def clickRelatedBloggers(blogerNum : int):
    try:
        morebloger = driver.find_element(By.CLASS_NAME, "other_reaction")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", morebloger)
        time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
        driver.execute_script("arguments[0].click();", morebloger)
        time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
        print("Clicked 'other_reaction' button successfully.")
    except Exception as e:
        print("No 'other_reaction' button found — skipping.", e)
        return []

    # 관련 블로거 수집 (특정 닉네임 제외)
    try:
        blogers = driver.find_elements(By.XPATH, "//div[@class='profile_area__BcjSN']/a")
        blogerurls = []
        for b in blogers:
            try:
                # 닉네임 텍스트 추출
                nickname_elem = b.find_element(By.XPATH, ".//span[@class='nickname__MrPCf']")
                nickname = nickname_elem.text.strip()
                if nickname == "마법상점판":
                    print(f"Skipped blogger '{nickname}'.")
                    continue  # 해당 블로거는 무시
            except:
                # 닉네임 span이 없으면 그냥 통과
                pass

            # URL 추출
            url = b.get_attribute("href")
            if url:
                blogerurls.append(url)

            # 최대 blogerNum 제한
            if len(blogerurls) >= blogerNum:
                break

        print(f"Collected {len(blogerurls)} related blogger URLs (excluding blocked nicknames).")
        return blogerurls
    except Exception as e:
        print("Failed to collect related blogger URLs:", e)
        return []

def moveToRecentPost():
    time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
    try:
        # 버튼 탐색 (없을 수 있음)
        listView = driver.find_element(By.XPATH, "//button[@data-click-area='pls.text']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", listView)
        time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
        listView.click()
        time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
        
        # 포스트 목록에서 첫 번째 포스트 열기
        posts = driver.find_elements(By.XPATH, "//div[@class='postlist__qxOgF']/a")
        if len(posts) == 0:
            print("No posts found — skipping.")
            return
        url = str(posts[0].get_attribute("href"))
        driver.get(url)
        time.sleep(random.uniform(defaultDelayMin, defaultDelayMax))
        print("Moved to most recent post.")
        
    except Exception as e:
        # 버튼이 없거나 클릭 불가능할 경우 건너뜀
        print("No 'list view' button found or not clickable — skipping this blogger.")
        return