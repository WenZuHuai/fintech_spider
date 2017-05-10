import traceback
import time
import uuid
import math
import random
from io import BytesIO
from io import StringIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

def calculate_slider_offset(img0, img1):
    """
    
    :param img0: 
    :param img1: 
    :return: return (True,left) or (False,None)
    """
    img0 = Image.open(img0).convert("L")#灰度值
    img1 = Image.open(img1).convert("L")
    # img0 = Image.open(img0).convert("1")#二值图
    # img1 = Image.open(img1).convert("1")
    # img0 = Image.open(img0)
    # img1 = Image.open(img1)
    w0, h0 = img0.size
    w1, h1 = img1.size
    if w0 != w1 and h0 != h1:
        return False, None
    pix0_list = []
    pix1_list = []
    for x in range(w0):
        pix_value = 0
        for y in range(h0):
            pix_value += img0.load()[x, y]
            # pix_value += ((img0.load()[x,y][0]+img0.load()[x,y][1]+img0.load()[x,y][2]) / 3)
            # r = img0.load()[x,y][0]
            # g = img0.load()[x,y][1]
            # b = img0.load()[x,y][2]
            # pix_value += (1-3*min(r,g,b)/(r+g+b))
        pix0_list.append(pix_value)
    for x in range(w0):
        pix_value = 0
        for y in range(h0):
            pix_value += img1.load()[x, y]
            # pix_value += ((img1.load()[x, y][0] + img1.load()[x, y][1] + img1.load()[x, y][2]) / 3)
            # r = img1.load()[x,y][0]
            # g = img1.load()[x,y][1]
            # b = img1.load()[x,y][2]
            # pix_value += (1-3*min(r,g,b)/(r+g+b))
            # pix_value += ((max(r,g,b)+min(r,g,b))/2)
        pix1_list.append(pix_value)
    pix_list = [abs(pix0_list[index] - pix1_list[index]) for index in range(len(pix0_list))]
    count = 0
    for index in range(50,len(pix_list)):
        if pix_list[index] > 1500:
            count += 1
            if count >35:
                break
        else:
            count =0
    left = index - 35
    print(pix_list)
    print("需要滑动像素点：", left)
    return  True, left

def get_search_page(search_text):
    url = "http://www.gsxt.gov.cn/index.html"
    driver = webdriver.Chrome("/home/hee/driver/chromedriver")
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.ID, "keyword")))
    element.clear()
    element.send_keys(search_text)

    # element.send_keys(Keys.ENTER)
    time.sleep(random.uniform(1.0,2.0))
    element = driver.find_element_by_id("btn_query")
    element.click()
    wait = WebDriverWait(driver, 30)
    element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "gt_box")))
    time.sleep(random.uniform(2.0, 3.0))
    return driver

def crop_captcha_image(driver, gt_element_class_name="gt_box"):

    captcha_el = driver.find_element_by_class_name(
        gt_element_class_name)
    location = captcha_el.location
    size = captcha_el.size
    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x'] + size['width'])
    bottom = int(location['y'] + size['height'])
    screenshot = driver.get_screenshot_as_png()
    print(left, top, right, bottom)
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((left, top, right, bottom))
    captcha.save("%s.png" % uuid.uuid1())
    return captcha

def drag_drop_test(driver,
                   x_offset=0,
                   y_offset=0,
                   element_class="gt_slider_knob"):
    """拖拽滑块
    
    :param x_offset:相对滑块x坐标偏移 
    :param y_offset: 相对滑块y坐标偏移
    :param element_class: 滑块网页元素的css类名
    :return: 
    """
    dragger = driver.find_element_by_class_name(element_class)
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(dragger, x_offset, y_offset).perform()
    time.sleep(2.8)

def click_refresh(driver):
    element = driver.find_element_by_class_name('gt_refresh_button')
    element.click()
def crack():
    driver = get_search_page("中国移动")
    for index in range(5):
        img1 = crop_captcha_image(driver)
        drag_drop_test(driver, x_offset=5)
        img2 = crop_captcha_image(driver)
        tag, left = calculate_slider_offset(img1, img2)
        if not tag:
            click_refresh(driver)
        else:
            break

    print(left)
if __name__ == "__main__":
    crack()

    # calculate_slider_offset("3.png","4.png")