#下载b站视频
#先使用cmd安装you-get：  pip/pip3 install you-get 
import os
BVnum='BV号'    
Bpath='https://www.bilibili.com/video/'+BVnum  #BV号
#command='you-get -i ' + path #查看视频的信息
command='you-get -o D:/movie --format=flv ' + Bpath     #-o 后面填写视频保存地址
#--format表示下载的格式，由上一步输出的信息，不同清晰度-format也不同 ，-format可以用于选择清晰度
os.system(command) #下载完还会有一个xml文件，里面存放的是视频的弹幕


#下载某人收藏夹中的内容：
#大多数时候下的挺慢的，不是很实用，不过可以挂在那里下。
#前提是要访问的收藏夹打开了隐私。
#类似的，下载某个up主的所有视频也可以这样下载，只是xpath定位的class要变一变了.
from selenium import webdriver
import time
import os
def PageNum():         #获取总的页数
    page=driver.find_element_by_class_name('be-pager-total').text
    pagenum=page[2:-3]
    return pagenum
def Page_Next():       #点击下一页
    page=driver.find_element_by_class_name('be-pager-next')
    page.click()
if __name__=='__main__':
    url="https://space.bilibili.com/UID/favlist"
    driver=webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    for i in range(0,int(PageNum())):
        favor=driver.find_elements_by_xpath('//ul[@class = "fav-video-list clearfix content"]/li')
        for ul in favor:
            url='https://www.bilibili.com/video/'+ul.get_attribute('data-aid')   #获取BV号
            command='you-get -o D:/movie --playlist --format=flv ' + url   #-format=flv下载的是1080p，如果某个视频没有1080p可能会报错
            os.system(command)
        Page_Next()
        time.sleep(3)  #等待加载
    driver.quit()


#监控B站视频的标题，播放量和弹幕数量
#不想打开浏览器可以使用无头模式，将数据取出来。无头模式会把console里的内容打印出来，所以这里暂时没采用。
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options   #无头模式
import time
import os
if __name__=='__main__':
    url="https://www.bilibili.com/video/BV1kK4y1v7sH"   #视频地址
    driver=webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    count=0 #控制次数
    while(True):
        driver.refresh()
        time.sleep(5)      #等待页面加载
        page=driver.find_elements_by_xpath('//div[@id = "app"]/div[@class="v-wrap"]/div[@class="l-con"]/div[@id="viewbox_report"]')
        #视频标题
        titles=page[0].find_elements_by_xpath('.//span[@class="tit"]')     
        if len(titles)==0:
            titles=page[0].find_elements_by_xpath('.//span[@class="tit tr-fix"]')      #标题的class好像有时候不一样，针对着改一下
        title=titles[0].text               
        #播放量
        plays=page[0].find_element_by_class_name("view")
        playnum=plays.text
        play=playnum[:-5]
        #弹幕数量
        barrages=page[0].find_element_by_class_name("dm")
        barrage=barrages.text
        barr=barrage[:-2]
        print('标题：' + title + '\n' + '播放量：' + play + '\n' + '弹幕数：'+barr)
        count=count+1
        if  count==10:     #终止条件
            break
