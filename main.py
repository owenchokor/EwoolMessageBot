import argparse
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm
from src import StaticFuncs
import datetime

def main():
    load_dotenv()
    APIKEY = os.getenv('SMARTSMS_API_KEY')
    PATTERN = r"^\d{3}-\d{4}-\d{4}$"
    SEND_URL = 'https://apis.aligo.in/send/'
    LOG_PATH = './logs/' + datetime.datetime.now().strftime("%Y%m%d%h%m") + '.txt'


    parser = argparse.ArgumentParser(description="Send SMS via Aligo API.")
    parser.add_argument("--excel", required=True, help="Path to the E-wool adress file")
    parser.add_argument("--image", required=True, help="Path to the image file for MMS.")
    #parser.add_argument("--msg", required=True, help="Message to send.")
    #parser.add_argument("--title", required=True, help="Title of the MMS.")
    args = parser.parse_args()


    sheet_dict = {sheet_name: pd.read_excel(args.excel, sheet_name=sheet_name)[['성함', '휴대폰 (연락처)']] 
                for sheet_name in pd.ExcelFile(args.excel).sheet_names}
    
    logs = ''

    errors = 0
    for sheet_name, df in sheet_dict.items():
        valid_df = StaticFuncs.process_df(df, PATTERN).to_dict('records')
        print(f'{sheet_name} : 전체 명단 {len(df)}명, 올바른 전화번호 형식 {len(valid_df)}명')
        loop = tqdm(valid_df, desc=f'{sheet_name} 전송 진행중', total=len(valid_df))
        for person in loop:
            title = '이울 60주년 행사 및 발전기금 모금 안내'
            msg = f"{person['성함']} 선생님, 이울진료회 60주년 행사 및 발전기금 모금 안내드립니다."
            sms_data = StaticFuncs.getSMSData(APIKEY, person, msg, title)
            files = {'image': open(args.image, 'rb')}
            send_response = requests.post(SEND_URL, data=sms_data, files=files)
            logs += f'{person["성함"]} : {send_response.json()}\n'
            if send_response.json()['error_cnt'] == 1:
                errors += 1
                loop.set_postfix_str(f'Error: {errors}')
    
    with open(LOG_PATH, 'w') as f:
        f.write(logs)
if __name__ == "__main__":
    main()