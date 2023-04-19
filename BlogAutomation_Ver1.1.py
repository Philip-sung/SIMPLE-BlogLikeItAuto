import SeleniumModules as sm
import time
import random

##########사용자 설정 변수##########
# ID & Passwords
id :str = "Put ID Here"
pw :str = "Put Password Here"

# Maximum Posts Number to visit
postNum = 50

# Maximum link clicks of Related Bloggers
blogerNum = 10

# ExcludeURL
excludeURLS = [
"cjddn2009",
"wlsdbsqkd",
"jative",
]
###################################

sm.login(id,pw)


urls = sm.searchBlog(postNum)
for url in urls:
    sm.openBlog(url, 1)

    exceptionflag = False
    for Xurl in excludeURLS: 
        if Xurl in url:
            time.sleep(2)
            sm.closeExcludedBlog()
            exceptionflag = True
            continue
    if(exceptionflag):
        continue

    if sm.availableLike() :
        sm.clickLike()

    relatedBlogers = sm.clickRelatedBloggers(blogerNum)

    for relatedurl in relatedBlogers:
        sm.openBlog(relatedurl, 2)
        sm.moveToRecentPost()
        if sm.availableLike() :
            sm.clickLike()
        sm.closeBlog()

    sm.closeBlog()

sm.driver.quit()