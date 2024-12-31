import re


class StaticFuncs:
    @staticmethod
    def process_ser(ser, pattern):
        return ser.apply(lambda x: re.sub(r"-", "", re.search(pattern, str(x)).group(0)) if re.search(pattern, str(x)) else None).dropna()
    
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