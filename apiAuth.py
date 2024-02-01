import os
from dotenv import load_dotenv
import requests

# 加載 account.env 檔案
load_dotenv(dotenv_path='account.env')

# 從 account.env 檔案中讀取 UID、API_PWD 和 SITE_URL
uid = os.getenv('UID')
api_pwd = os.getenv('API_PWD')
site_url = os.getenv('SITE_URL')

# 檢查是否成功讀取所需的環境變量
if not uid or not api_pwd or not site_url:
    print("account.env 檔案中必須包含 UID、API_PWD 和 SITE_URL。")
else:
    # 設定 API 端點
    url = f"{site_url}/API21/HTTP/ConnectionHandler.ashx"

    # 準備請求主體
    payload = {
        "HandlerType": 3,
        "VerifyType": 1,
        "UID": uid,
        "PWD": api_pwd
    }

    # 設定請求標頭
    headers = {
        'Content-Type': 'application/json'
    }

    # 發送 POST 請求以獲取連線憑證
    response = requests.post(url, json=payload, headers=headers)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        
        # 檢查操作是否成功
        if data['Result']:
            # 獲取 Msg (token)
            token = data['Msg']
            print("成功獲取連線憑證。")

            # 使用 token 檢查連線狀態
            check_url = f"{site_url}/API21/HTTP/ConnectionHandler.ashx"
            check_payload = {
                "HandlerType": 3,
                "VerifyType": 2
            }
            check_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            check_response = requests.post(check_url, json=check_payload, headers=check_headers)

            if check_response.status_code == 200 and check_response.json().get('Result'):
                print("連線狀態正常。")

                # 將 token 寫入 msg.env 檔案，使用覆蓋模式
                with open('msg.env', 'w') as f:
                    f.write(f"Msg={token}\n")
                print("Msg (token) 已寫入 msg.env 檔案。")
            else:
                print("連線狀態異常。")
            
        else:
            print(f"獲取連線憑證失敗。訊息：{data['Msg']}")
    else:
        print(f"HTTP POST 請求失敗，狀態碼為 {response.status_code}。")
