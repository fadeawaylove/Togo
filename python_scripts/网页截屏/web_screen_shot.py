import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

content_height_js = """
function getScrollHeight(){  
    return Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);  
}
return getScrollHeight()
"""

content_width_js = """
function getScrollWidth(){  
    return Math.max(document.body.scrollWidth,document.documentElement.scrollWidth);  
}
return getScrollWidth()
"""

def get_screenshot(url, pic_name):

    driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)
    print("开始获取页面内容...")
    driver.get(url)
    time.sleep(1)
    driver.maximize_window()

    width, height = driver.execute_script(content_width_js), driver.execute_script(content_height_js)
    print("内容大小为：{}x{}".format(width, height))
    driver.set_window_size(width, height)
    driver.get_screenshot_as_file(pic_name)

    driver.quit()


if __name__ == "__main__":
    url = "https://www.runoob.com/linux/linux-comm-crontab.html"
    get_screenshot(url, pic_name="c.png")