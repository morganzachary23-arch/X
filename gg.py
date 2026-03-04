import cloudscraper
import random
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from fake_useragent import UserAgent
import threading

# রঙ সেটআপ
BOLD = '\033[1m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
D = '\033[0m'
C = '\033[96m'

# থ্রেড লক ফাইল রাইটিং এর জন্য
file_lock = threading.Lock()

# সেশন পুল
session_pool = []
session_lock = threading.Lock()

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-4.0 (403 Fixed)\n {D}')

def create_session():
    """নতুন সেশন তৈরি করে"""
    try:
        # Fake UserAgent তৈরি
        ua = UserAgent()
        
        # শুধুমাত্র সঠিক ব্রাউজার নাম ব্যবহার করুন
        browser_options = [
            {'browser': 'chrome', 'platform': 'windows', 'mobile': False, 'desktop': True},
            {'browser': 'firefox', 'platform': 'windows', 'mobile': False, 'desktop': True},
            {'browser': 'chrome', 'platform': 'linux', 'mobile': False, 'desktop': True}
        ]
        
        selected_browser = random.choice(browser_options)
        
        # Cloudscraper সেশন তৈরি
        scraper = cloudscraper.create_scraper(
            browser=selected_browser,
            delay=10
        )
        
        # স্ট্যান্ডার্ড headers সেট
        scraper.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'User-Agent': ua.random
        })
        
        return scraper
    except Exception as e:
        print(f'{Y} [!] Session তৈরি করতে সমস্যা: {e}{D}')
        return None

def init_session_pool(size=2):
    """সেশন পুল তৈরি করে"""
    global session_pool
    session_pool = []  # আগের সেশনগুলো ক্লিয়ার করুন
    
    print(f'{C} [*] সেশন পুল তৈরি হচ্ছে...{D}')
    
    for i in range(size):
        print(f'{Y} [*] সেশন {i+1} তৈরি হচ্ছে...{D}')
        session = create_session()
        if session:
            session_pool.append(session)
            print(f'{G} [✓] সেশন {i+1} তৈরি হয়েছে{D}')
        else:
            print(f'{R} [✗] সেশন {i+1} তৈরি ব্যর্থ{D}')
        time.sleep(1)
    
    return len(session_pool)

def get_session():
    """পুল থেকে সেশন নেয়"""
    global session_pool
    with session_lock:
        if session_pool:
            return random.choice(session_pool)
        else:
            return create_session()

def username_gen(names, start, end):
    """ইউজারনেম জেনারেট করে"""
    usernames = []
    name_list = [name.strip() for name in names.split(',') if name.strip()]
    
    for name in name_list:
        for num in range(start, end + 1):
            # সঠিক ফরম্যাটে ইউজারনেম তৈরি
            username = f'{name.lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    
    random.shuffle(usernames)
    return usernames

def checker(uname):
    """ইউজারনেম চেক করার মূল ফাংশন"""
    session = get_session()
    if not session:
        print(f'{R} [!] সেশন পাওয়া যায়নি{D}')
        return False
    
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # র‍্যান্ডম ফোন নম্বর
    phone = f"1347{random.randint(100000, 999999)}"
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://baji999.net',
        'Referer': 'https://baji999.net/bd/en/register',
        'X-Requested-With': 'XMLHttpRequest'
    }

    json_data = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'userId': uname,
        'phone': phone,
        'friendReferrerCode': '',
        'captcha': '',
        'callingCode': '880',
        'registerTypeId': 0,
        'random': str(random.randint(1000, 9999))
    }

    retry_count = 0
    max_retries = 2
    
    while retry_count < max_retries:
        try:
            response = session.post(url, json=json_data, headers=headers, timeout=20)
            
            if response.status_code == 403:
                print(f'{R} [!] Cloudflare Blocked. Retry {retry_count + 1}/{max_retries}{D}')
                retry_count += 1
                time.sleep(10 * retry_count)
                continue
                
            elif response.status_code == 200:
                try:
                    data = response.json()
                    
                    if data.get('status') == 'F0003':
                        return True
                    elif data.get('status') == 'S0001':
                        print(f'{Y} [!] Rate Limit{D}')
                        time.sleep(20)
                        continue
                    else:
                        return False
                        
                except:
                    return False
            else:
                return False
                
        except Exception as e:
            print(f'{Y} [!] Error: {str(e)[:50]}{D}')
            retry_count += 1
            time.sleep(5)
            continue
    
    return False

def check_username(username):
    """ইউজারনেম চেক এবং সেভ করে"""
    try:
        uname = username.split('|')[0].strip() if '|' in username else username.strip()
        
        print(f'{C} [*] Checking: {uname}{D}')
        
        if checker(uname):
            print(f'{BOLD}{G} [✓] VALID: {uname}{D}')
            with file_lock:
                with open('valid_usernames.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{username}\n')
            
            time.sleep(random.uniform(3, 6))
        else:
            print(f'{R} [✗] Invalid: {uname}{D}')
    except Exception as e:
        print(f'{Y} [!] Error in check_username: {e}{D}')

def main():
    logo()
    
    # সেশন পুল initialize (শুধু ২ টি সেশন)
    pool_size = init_session_pool(2)
    
    if pool_size == 0:
        print(f'{R} [!] কোন সেশন তৈরি হয়নি। প্রোগ্রাম বন্ধ হচ্ছে...{D}')
        return
    
    # ইনপুট নেওয়া
    names = input(f'{BOLD}{G} নাম লিখুন (যেমন: Sadek,Tanvir,Rahim) : {D}')
    start = int(input(f'{BOLD}{Y} শুরু নাম্বার : '))
    end = int(input(f'{BOLD}{Y} শেষ নাম্বার : '))
    
    print(f'\n{G} [1] স্লো (নিরাপদ)\n{Y} [2] মিডিয়াম\n{R} [3] ফাস্ট{D}')
    print(f'{C} [4] আল্ট্রা স্লো (403 ফিক্স){D}')
    
    speed = int(input(f'\n{C} স্পিড নির্বাচন করুন : {D}'))
    
    # স্পিড সেটিংস
    if speed == 1:
        max_workers = 1
        base_delay = 5
    elif speed == 2:
        max_workers = 2
        base_delay = 3
    elif speed == 3:
        max_workers = 3
        base_delay = 2
    else:
        max_workers = 1
        base_delay = 8

    # ইউজারনেম জেনারেট
    usernames = username_gen(names, start, end)
    
    print(f'\n{BOLD}{G} {"="*50}')
    print(f'মোট ইউজারনেম: {len(usernames)}')
    print(f'থ্রেড সংখ্যা: {max_workers}')
    print(f'বিরতি: {base_delay} সেকেন্ড')
    print(f'{"="*50}{D}\n')
    
    time.sleep(2)
    
    # চেকিং শুরু
    valid_count = 0
    total_checked = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for username in usernames:
            # বিরতি দিয়ে রিকোয়েস্ট পাঠান
            time.sleep(base_delay)
            future = executor.submit(check_username, username)
            futures.append(future)
        
        # রেজাল্ট সংগ্রহ
        for future in as_completed(futures):
            total_checked += 1
            if total_checked % 10 == 0:
                print(f'{C} [*] {total_checked}/{len(usernames)} চেক করা হয়েছে{D}')
    
    print(f'\n{BOLD}{G} {"="*50}')
    print(f'চেকিং সম্পূর্ণ!')
    print(f'ভ্যালিড ইউজারনেম "valid_usernames.txt" ফাইলে সেভ হয়েছে')
    print(f'{"="*50}{D}')

if __name__ == '__main__':
    try:
        # প্রয়োজনীয় প্যাকেজ ইন্সটল করা আছে কিনা চেক করুন
        required_packages = ['cloudscraper', 'fake-useragent', 'requests']
        
        # valid_usernames.txt ফাইল তৈরি করুন
        if not os.path.exists('valid_usernames.txt'):
            with open('valid_usernames.txt', 'w') as f:
                pass
        
        main()
    except KeyboardInterrupt:
        print(f'\n{Y} [!] প্রোগ্রাম বন্ধ করা হচ্ছে...{D}')
    except Exception as e:
        print(f'{R} [!] Error: {e}{D}')
        print(f'{Y} টিপস: নিচের কমান্ড রান করুন:{D}')
        print(f'{C} pip install cloudscraper fake-useragent requests{D}')
