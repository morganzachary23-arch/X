import cloudscraper
import random
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# রঙ সেটআপ
BOLD = '\033[1m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
D = '\033[0m'
C = '\033[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-3.0 (Anti-403)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    # প্রতিবার নতুন একটি স্ক্র্যাপার অবজেক্ট তৈরি করা যা ভিন্ন ব্রাউজার নকল করবে
    browser_options = [
        {'browser': 'chrome', 'platform': 'windows', 'mobile': False},
        {'browser': 'firefox', 'platform': 'windows', 'mobile': False},
        {'browser': 'chrome', 'platform': 'android', 'mobile': True},
        {'browser': 'safari', 'platform': 'ios', 'mobile': True}
    ]
    
    selected_browser = random.choice(browser_options)
    scraper = cloudscraper.create_scraper(browser=selected_browser)

    while True:
        try:
            # হিউম্যান বিহেভিয়ার নকল করতে র‍্যান্ডম বিরতি
            time.sleep(random.uniform(2, 5)) 
            
            url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
            
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Origin': 'https://baji999.net',
                'Referer': random.choice(['https://baji999.net/bd/en/register', 'https://baji999.net/']),
                'X-Requested-With': 'XMLHttpRequest'
            }

            json_data = {
                'languageTypeId': 1,
                'currencyTypeId': 8,
                'userId': uname,
                'phone': f'1347{random.randint(100000, 999999)}', # র‍্যান্ডম ফোন নাম্বার
                'friendReferrerCode': '',
                'captcha': '',
                'callingCode': '880',
                'registerTypeId': 0,
                'random': str(random.randint(1000, 9999))
            }

            response = scraper.post(url, json=json_data, headers=headers, timeout=20)
            
            if response.status_code == 403:
                print(f'{R} [!] Cloudflare Blocked IP. Wait 10s or Change IP...{D}')
                time.sleep(10)
                return False

            data = response.json()
            
            if data.get('status') == 'F0003':
                return True
            elif data.get('status') == 'S0001':
                print(f'{Y} [!] Rate Limit. Slowing down...{D}')
                time.sleep(30)
                continue
            else:
                return False

        except Exception:
            return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [VALID] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{G} ENTER NAMES (e.g. Sadek,Tanvir) : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : '))
    end = int(input(f'{BOLD}{Y} END NUMBER : '))
    
    print(f'\n{G} [1] LOW (Best for Anti-Block)\n{Y} [2] MEDIUM\n{R} [3] HIGH{D}')
    speed = int(input(f'\n{C} CHOOSE SPEED : {D}'))
    
    # ৪MD৩ এড়াতে স্পিড খুব বেশি না রাখাই ভালো
    spd = {1: 1, 2: 3, 3: 5}.get(speed, 1)

    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    print(f'\n{BOLD}{G} CHECKING FINISHED! {D}')

if __name__ == '__main__':
    if not os.path.exists('.uids.txt'):
        open('.uids.txt', 'w').close()
    main()
