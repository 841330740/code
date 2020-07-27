from selenium import webdriver
import time

def Search_Product(key):     #向搜索框输入内容
    driver.find_element_by_id('key').send_keys(key)

def Click_Search():        #搜索按钮
    driver.find_element_by_class_name('button').click()

def PageNum():         #获取总的页数
    pagenum=driver.find_element_by_class_name('p-skip').text
    return pagenum[1:-10]

def Page_Next():      #下一页
    page=driver.find_element_by_class_name('pn-next')
    page.click()
    
if __name__=='__main__':
    products=[]
    count=0
    url="http://www.jingdong.com/"
    driver=webdriver.Chrome()
    driver.get(url)
    Search_Product('switch')
    driver.maximize_window()
    Click_Search()
    time.sleep(3)      #进程挂起5秒，等待窗口加载完成
    driver.execute_script("window.scrollBy(0, 8000)")    #下拉滚动条以使网页中的全部商品信息加载
    time.sleep(1)
    while(count<int(PageNum())):
        products_info=driver.find_elements_by_xpath('//div[@class = "gl-i-wrap"]')
        for div in products_info:
            name=div.find_element_by_xpath('.//div[@class="p-name p-name-type-2"]')     #商品名称
            price=div.find_element_by_xpath('.//div[@class="p-price"]//i')           #价格
            shop=div.find_element_by_xpath('.//div[@class="p-shop"]')  #店铺名称
            commit=div.find_element_by_xpath('.//div[@class="p-commit"]//a')       #评价
            products.append((name.text,price.text+'元',shop.text,commit.text+'评论'))
        pagenum=count+1
        print('第'+str(pagenum)+'页已提取，共'+PageNum()+'页')
        Page_Next()
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 8000)")    
        time.sleep(1)
        count+=1
    driver.quit()
    print(products)
