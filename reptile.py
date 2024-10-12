import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def update_ul_content(url, local_file_path):
    # 检查当前时间是否为 00:01
    current_time = datetime.now()
    if current_time.hour == 0 and current_time.minute == 1:

        # 1. 从网页端获取 <ul class="slot-list slot-list-1"> 的内容
        response = requests.get(url)
        web_soup = BeautifulSoup(response.text, 'html.parser')
        web_ul_element = web_soup.find('ul', class_=['slot-list slot-list-1', 'slot-list slot-list-2'])

        # 检查是否成功找到元素
        if not web_ul_element:
            print("未找到网页中的 <ul class='slot-list slot-list-1'> 元素")
            return
        
        # 2. 读取本地 HTML 文件
        with open(local_file_path, "r", encoding="utf-8") as file:
            local_soup = BeautifulSoup(file, 'html.parser')
        
        # 3. 替换本地文件中的 <ul class="slot-list slot-list-1"> 的内容
        local_ul_element = local_soup.find('ul', class_=['slot-list slot-list-1', 'slot-list slot-list-2'])
        
        if local_ul_element:
            # 用网页端的内容替换本地的 <ul> 元素内容
            local_ul_element.replace_with(web_ul_element)
            
            # 4. 将修改后的 HTML 保存回本地文件
            with open(local_file_path, "w", encoding="utf-8") as file:
                file.write(str(local_soup))

# 持续监控时间，每 60 秒检查一次是否为 00:01
while True:
    update_ul_content("https://cgyy.xmu.edu.cn/room/1", "templates/room/1.html")
    update_ul_content("https://cgyy.xmu.edu.cn/room/2", "templates/room/2.html")
    time.sleep(60)
