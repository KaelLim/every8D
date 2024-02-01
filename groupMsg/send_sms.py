import os
import csv
import requests
from dotenv import load_dotenv

# 加载 account.env 和 msg.env 文件
load_dotenv(dotenv_path='../account.env')
load_dotenv(dotenv_path='../msg.env')

# 从环境变量读取数据
uid = os.getenv('UID')
pwd = os.getenv('PWD')
token = os.getenv('Msg')
site_url = os.getenv('SITE_URL')

# API 端点
send_sms_url = f"{site_url}/API21/HTTP/SendSMS.ashx"

# 从 phone.csv 读取电话号码
phone_numbers = []
with open('phone.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        phone_numbers.append(row['phone'])

# 将电话号码转换为逗号分隔的字符串
dest_numbers = ','.join(phone_numbers)

# 准备请求参数
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Bearer {token}'  # 使用 token 验证
}
body = {
    'UID': uid,  # 如果你选择使用 UID 和 PWD 验证，取消此行注释
    'PWD': pwd,  # 如果你选择使用 UID 和 PWD 验证，取消此行注释
    'SB': '重要訊息！',
    'MSG': '慈濟不就好棒棒喔',
    'DEST': dest_numbers
}

# 发送 POST 请求
response = requests.post(send_sms_url, headers=headers, data=body)

# 检查请求是否成功
if response.status_code == 200:
    print("短信发送成功。")
    print(response.text)  # 打印响应内容
else:
    print(f"发送失败，状态码：{response.status_code}")
