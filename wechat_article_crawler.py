import requests
import datetime
from time import sleep
from bs4 import BeautifulSoup
import json

# 自动化思路：建立号码池和数据库，启动时遍历数据库所有公众号（耗费【150+50x天数】个爬取次数），
# 每次访问都随机选择一个号码（每个号码需要爬取至少【200/号码数】个页面），
# 每个页面至少需要花费时间【120/号码数】秒，遍历一遍需要时间【13/号码数的平方】小时
# 最后更新数据库数据，定期抽取数据编码上传

import random

class NumberPool:
    def __init__(self, numbers):
        self.numbers = numbers
        self.last_call = None
        
    def validate(self):
        valid_numbers = []
        for number in self.numbers:
            if self.is_valid(number):
                valid_numbers.append(number)
        print(f"{len(valid_numbers)} valid numbers")
        self.numbers = valid_numbers
        
    def is_valid(self, number):
        # Implement validation logic
        return True 
    
    def count_numbers(self):
        return len(self.numbers)
    
    def get_number(self):
        if self.last_call and time.time() - self.last_call < 120/self.count_numbers():
            print("Too soon to call again")
            return None
        
        self.last_call = time.time()
        return random.choice(self.numbers)

def main():
    result = []
    for i in range(start - 1, 10000):
        print('crawling {}th page'.format(i + 1))
        try:
            i *= 5
            url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={}&count=5&fakeid={}&type=9&query=&token={}&lang=zh_CN&f=json&ajax=1'.format(
                i, fakeid, token)
            headers = {
                'authority': 'mp.weixin.qq.com',
                'cookie': cookie,
                'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
            res = requests.get(url=url, headers=headers).json()
            for k in res['app_msg_list']:
                title = k['title']
                timeStamp = k['update_time']
                dateArray = datetime.datetime.fromtimestamp(timeStamp)
                time = dateArray.strftime('%Y-%m-%d %H:%M:%S')
                href = k['link']
                cover = k['cover']


                # 解析文章内容
                r = requests.get(url=href, headers=headers).content.decode('utf-8')
                soup = BeautifulSoup(r, 'html.parser')
                images = soup.select('div#js_content img')
                if not images:
                    print('No images in content')
                    images = []
                else:
                    images = [img.get('data-src') for img in images] 
                content = '\n'.join([p.text for p in soup.select('div#js_content p')])

                dic = {
                    'title': title,
                    'time': time,
                    'href': href,
                    'cover': cover,
                    'content': content,
                    'images': images
                }

                result.append(dic)
                
        except Exception as e:
            print('Error occurred when crawling:', e)
            break

    with open('wechat_article.json', 'a') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    start = 1
    fakeid = 'MzIzNTQ3NjY2MA=='
    # token = '1247220242'
    # cookie = 'appmsglist_action_3882612755=card; ua_id=wslDscT23uIeY8QKAAAAANEOsRhHdkiiAHhLajGUo4s=; wxuin=76175969279960; uuid=f084033a871aeb84e4733dd1ed7dce25; rand_info=CAESINzefkKaQZR2vQlNt/2m4caquUFPVMWr3mgjcS+T/kSc; slave_bizuin=3882612755; data_bizuin=3882612755; bizuin=3882612755; data_ticket=5P9Ee1ApWewNEtVLHAPc6UCuwgInfzvTv36SjZR293BQkaj/JNeZolh33VVepuRN; slave_sid=Njl0eFgySDJJRlkxY3VfSWJIRFZUYl9ucno0U2tjUGlCaG1FVVkxWHJyS3VhUkF3MTBtNExwWk1OX2xRTFlma1dPb2RkSmxlNjZqXzlWcVBBX0NNWEpPRk5DT28wQ1oyRFdUS3BkSzN2clNoQ0s1SVVwS2VoMDE1eHp4alRWa0FFNXV2UlhMb0FkWklmTHc1; slave_user=gh_b6f700d5c3fd; xid=a6f6174babcd315e2e15d828638aef2c; mm_lang=zh_CN'
    token = '666753265'
    cookie = 'rewardsn=; ua_id=8UQSlIu51QqrzmtKAAAAAEygHDGWzcF7_hgcKc1XD6o=; _clck=14bt622|1|fex|0; wxuin=94396564744996; uuid=77fddd0771efbfa2a8b2d71a92662419; rand_info=CAESIIVhTDj59d3yiMtkIoUFHZOdDbmvUrJkO8/aa1TPcW+R; slave_bizuin=3930571524; data_bizuin=3930571524; bizuin=3930571524; data_ticket=ZGtzxXMSB0Tbk7hrbGhBYHIcJrPfbwuV9q2s1uGZGrExgsr3zXXLv1CKb+/FafUS; slave_sid=aTVZRnBhWG5Tb09sR2g4T3BPVThoY3hzNGoweEtCMHphMl9TWU5xZ1ZYcnNXV1hLRlE1QTNsWERzQWdQVFJuUDEzcXdDbDY2XzBjSU11YTl4SHFnX1k4QW01d29nU25USWp3c2h1SE0wU2lmSUcyQnM2Sk5nckFYQ0N5T2NnSEtCV1BNNHp6UHlTcFBXSUNt; slave_user=gh_f0acd9eb9c1b; xid=7d29cee4ffbeda73f25ace52adea3f37; mm_lang=zh_CN; wxtokenkey=777; _clsk=1lsuhmd|1694414990143|14|1|mp.weixin.qq.com/weheat-agent/payload/record'
    main()
