import re


class StaticFuncs:
    @staticmethod
    def process_df(df, pattern):
        df['휴대폰 (연락처)'] = df['휴대폰 (연락처)'].apply(
            lambda x: re.sub(r"-", "", re.search(pattern, str(x)).group(0)) if re.search(pattern, str(x)) else None
        )
        return df.dropna(subset=['성함', '휴대폰 (연락처)'])
    
    def getSMSData(APIKEY, num, msg : str, title : str):
        return {
            'key': APIKEY,
            'userid': 'owencho01',
            'sender': '01030048959',
            'receiver': str(num),
            'msg': msg,
            'msg_type': 'mms', 
            'title': title,
            'destination': str(num)
        }