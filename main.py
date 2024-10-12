from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request, redirect, url_for, session

import requests
from bs4 import BeautifulSoup

def fetch_and_modify_html(url, output_file):
    # 读取网页内容
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.text
        
        # 解析 HTML 内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找所有包含 `time-slot fulled`、`time-slot booked` 或 `time-slot closed` 类的 `span` 标签
        for span in soup.find_all('span', class_=['time-slot fulled', 'time-slot booked']):
            span['onclick'] = "toggleSlot(this)"
        
        # 添加 JavaScript 代码
        script = soup.new_tag('script')
        script.string = '''
        function toggleSlot(span) {
            // 获取日期和时间段文本，作为唯一标识符
            const dateInfo = span.closest('.slot').querySelector('.date-info').textContent.trim();
            const slotTime = span.textContent.trim();
            const slotId = `${dateInfo}_${slotTime}`; // 生成唯一标识符

            // 切换状态并存储
            if (span.classList.contains('fulled')) {
                span.classList.remove('fulled');
                span.classList.add('booked');
                localStorage.setItem(slotId, 'booked');
            } else if (span.classList.contains('booked')) {
                span.classList.remove('booked');
                span.classList.add('fulled');
                localStorage.setItem(slotId, 'fulled');
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            const slots = document.querySelectorAll('.time-slot');
            slots.forEach(slot => {
                const dateInfo = slot.closest('.slot').querySelector('.date-info').textContent.trim();
                const slotTime = slot.textContent.trim();
                const slotId = `${dateInfo}_${slotTime}`; // 生成唯一标识符

                // 从 localStorage 中恢复状态
                const savedStatus = localStorage.getItem(slotId);
                if (savedStatus) {
                    slot.classList.remove('fulled', 'booked', 'closed');
                    slot.classList.add(savedStatus);
                }

                slot.addEventListener('click', () => {
                    toggleSlot(slot);
                });
            });
        });
        '''
        soup.body.append(script)  # 将脚本添加到 `body` 的末尾

        # 手动替换 &nbsp; 只在指定元素中
        for green_slot in soup.find_all('span', class_='green_slot'):
            if green_slot.string:
                green_slot.string.replace_with(green_slot.string.replace(" ", "\xa0"))

        # 保存修改后的 HTML 文件
        with open(f'templates/{output_file}', 'w', encoding='utf-8') as file:
            file.write(str(soup))

app = Flask(__name__)
app.secret_key = 'a_very_secret_key_12345'

@app.route('/')
def home():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('front_page.html', username=usnername, student_id=student_id)

@app.route('/my_reservations')
def my_reservations():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('my_reservations.html', username=usnername, student_id=student_id)

@app.route('/room_reservations')
def room_reservations():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('room_reservations.html', username=usnername, student_id=student_id)

@app.route('/room/1')
def room1():
    return render_template('room/1.html')

@app.route('/room/2')
def room2():
    return render_template('room/2.html')

@app.route('/misd_query')
def misd_query():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('misd_query.html', username=usnername, student_id=student_id)

@app.route('/my_reservations/slot')
def slot():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('my_reservations/slot.html', username=usnername, student_id=student_id)

@app.route('/my_reservations/slot2')
def slot2():
    usnername = session.get('username')
    student_id = session.get('student_id')
    return render_template('my_reservations/slot2.html', username=usnername, student_id=student_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['student_id'] = request.form['student_id']
        return redirect(url_for('room1'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
   
