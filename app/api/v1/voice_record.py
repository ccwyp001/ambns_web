# -*- coding: utf-8 -*-

from app.api.aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '15722953'
API_KEY = 'ANXzzUyWMy3Tws6GUZP6U8dU'
SECRET_KEY = 'BD6fE5m1VjldZOXgGzScidT1mRkuABub'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
if __name__ == '__main__':

    _ = client.asr(get_file_content('C:/Users/wuyongpeng/Desktop/12316k.wav'), 'wav', 16000, {
        'dev_pid': 1536,
    })
    print(_)