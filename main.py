import argparse
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm
from src import StaticFuncs

def main():
    # Load environment variables
    load_dotenv()
    APIKEY = os.getenv('SMARTSMS_API_KEY')
    PATTERN = r"^\d{3}-\d{4}-\d{4}$"
    SEND_URL = 'https://apis.aligo.in/send/'

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Send SMS via Aligo API.")
    parser.add_argument("--excel", required=True, help="Path to the E-wool adress file")
    parser.add_argument("--image", required=True, help="Path to the image file for MMS.")
    parser.add_argument("--msg", required=True, help="Message to send.")
    parser.add_argument("--title", required=True, help="Title of the MMS.")
    args = parser.parse_args()

    # Read Excel file
    sheet_dict = {sheet_name: pd.read_excel(args.excel, sheet_name=sheet_name)['휴대폰 (연락처)'] 
                  for sheet_name in pd.ExcelFile(args.excel).sheet_names}

    # Process each sheet
    errors = 0
    for sheet_name, ser in sheet_dict.items():
        print(f'{sheet_name} : 전체 명단 {len(ser)}명, 올바른 전화번호 형식 {len(StaticFuncs.process_ser(ser, PATTERN))}명')
        loop = tqdm(ser, desc=f'{sheet_name} 전송 진행중', total=len(ser))
        for num in loop:
            sms_data = StaticFuncs.getSMSData(APIKEY, num, args.msg, args.title)
            files = {'image': open(args.image, 'rb')}
            send_response = requests.post(SEND_URL, data=sms_data, files=files)
            if send_response.json()['error_cnt'] == 1:
                errors += 1
                loop.set_description(f'Error: {errors}')

if __name__ == "__main__":
    main()