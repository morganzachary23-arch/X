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
        
        # র‍্যান্ডম ব্রাউজার সেটিংস
        browser_options = [
            {'browser': 'chrome', 'platform': 'windows', 'mobile': False, 'desktop': True},
            {'browser': 'firefox', 'platform': 'windows', 'mobile': False, 'desktop': True},
            {'browser': 'chrome', 'platform': 'linux', 'mobile': False, 'desktop': True},
            {'browser': 'safari', 'platform': 'macos', 'mobile': False, 'desktop': True}
        ]
        
        selected_browser = random.choice(browser_options)
        
        # Cloudscraper সেশন তৈরি
        scraper = cloudscraper.create_scraper(
            browser=selected_browser,
            interpreter='js2py',
            delay=15,
            allow_brotli=True
        )
        
        # স্ট্যান্ডার্ড headers সেট
        scraper.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': ua.random,
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
        })
        
        return scraper
    except Exception as e:
        print(f'{Y} [!] Session তৈরি করতে সমস্যা: {e}{D}')
        return None

def init_session_pool(size=5):
    """সেশন পool তৈরি করে"""
    global session_pool
    for _ in range(size):
        session = create_session()
        if session:
            session_pool.append(session)
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
        # বিভিন্ন প্যাটার্নে ইউজারনেম তৈরি
        patterns = [
            f'{name.lower()}{num} | {name.capitalize()}',  # sadek1 | Sadek
            f'{name.lower()}{num:03d} | {name.capitalize()}',  # sadek001 | Sadek
            f'{name.lower()}_{num} | {name.capitalize()}',  # sadek_1 | Sadek
            f'{name.lower()}.{num} | {name.capitalize()}',  # sadek.1 | Sadek
        ]
        
        for num in range(start, end + 1):
            pattern = random.choice(patterns)
            username = pattern.format(num=num)
            usernames.append(username)
    
    random.shuffle(usernames)
    return usernames

def checker(uname):
    """ইউজারনেম চেক করার মূল ফাংশন"""
    session = get_session()
    if not session:
        return False
    
    # বিভিন্ন API endpoint try করবে
    endpoints = [
        'https://baji999.net/api/wv/v1/user/registerPreCheck',
        'https://baji999.live/api/wv/v1/user/registerPreCheck',
        'https://baji999.cc/api/wv/v1/user/registerPreCheck'
    ]
    
    url = random.choice(endpoints)
    
    # র‍্যান্ডম ফোন নম্বর জেনারেট
    phone_prefixes = ['17', '18', '19', '13', '14', '15', '16']
    phone = f"{random.choice(phone_prefixes)}{random.randint(10000000, 99999999)}"
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
        'Content-Type': 'application/json',
        'Origin': 'https://baji999.net',
        'Referer': 'https://baji999.net/bd/en/register',
        'X-Requested-With': 'XMLHttpRequest',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
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
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            # র‍্যান্ডম বিরতি (Anti-Detection)
            time.sleep(random.uniform(3, 7))
            
            response = session.post(url, json=json_data, headers=headers, timeout=25, allow_redirects=False)
            
            if response.status_code == 403:
                print(f'{R} [!] Cloudflare Blocked. Retry {retry_count + 1}/{max_retries}{D}')
                retry_count += 1
                
                # নতুন সেশন তৈরি
                session = create_session()
                if not session:
                    time.sleep(30)
                    continue
                    
                time.sleep(15 * retry_count)  # এক্সপোনেনশিয়াল ব্যাকঅফ
                continue
                
            elif response.status_code == 200:
                try:
                    data = response.json()
                    
                    if data.get('status') == 'F0003':
                        return True
                    elif data.get('status') == 'S0001':
                        print(f'{Y} [!] Rate Limit. Waiting...{D}')
                        time.sleep(45)
                        continue
                    else:
                        return False
                        
                except json.JSONDecodeError:
                    return False
            else:
                print(f'{Y} [!] Status Code: {response.status_code}{D}')
                return False
                
        except requests.exceptions.ConnectionError:
            print(f'{Y} [!] Connection Error. Retrying...{D}')
            time.sleep(10)
            retry_count += 1
            continue
            
        except requests.exceptions.Timeout:
            print(f'{Y} [!] Timeout. Retrying...{D}')
            time.sleep(8)
            retry_count += 1
            continue
            
        except Exception as e:
            print(f'{R} [!] Error: {str(e)[:50]}{D}')
            return False
    
    return False

def check_username(username):
    """ইউজারনেম চেক এবং সেভ করে"""
    uname = username.split('|')[0].strip() if '|' in username else username.strip()
    
    print(f'{C} [*] Checking: {uname}{D}')
    
    if checker(uname):
        print(f'{BOLD}{G} [✓] VALID: {uname}{D}')
        with file_lock:
            with open('valid_usernames.txt', 'a', encoding='utf-8') as f:
                f.write(f'{username}\n')
        
        # প্রতি ভ্যালিড ইউজারের পর বিরতি
        time.sleep(random.uniform(5, 10))
    else:
        print(f'{R} [✗] Invalid: {uname}{D}')

def main():
    logo()
    
    # সেশন পool initialize
    print(f'{C} [*] সেশন পool তৈরি হচ্ছে...{D}')
    pool_size = init_session_pool(3)
    print(f'{G} [✓] {pool_size} টি সেশন তৈরি হয়েছে{D}')
    
    # ইনপুট নেওয়া
    names = input(f'{BOLD}{G} নাম লিখুন (যেমন: Sadek,Tanvir,Rahim) : {D}')
    start = int(input(f'{BOLD}{Y} শুরু নাম্বার : '))
    end = int(input(f'{BOLD}{Y} শেষ নাম্বার : '))
    
    print(f'\n{G} [1] স্লো (সবচেয়ে নিরাপদ)\n{Y} [2] মিডিয়াম\n{R} [3] ফাস্ট (ঝুঁকিপূর্ণ){D}')
    print(f'{C} [4] আল্ট্রা স্লো (403 ফিক্স){D}')
    
    speed = int(input(f'\n{C} স্পিড নির্বাচন করুন : {D}'))
    
    # স্পিড সেটিংস
    speed_config = {
        1: {'workers': 1, 'delay': 5},
        2: {'workers': 2, 'delay': 3},
        3: {'workers': 3, 'delay': 2},
        4: {'workers': 1, 'delay': 8}
    }
    
    config = speed_config.get(speed, speed_config[4])
    max_workers = config['workers']
    base_delay = config['delay']

    # ইউজারনেম জেনারেট
    usernames = username_gen(names, start, end)
    
    print(f'\n{BOLD}{G} {"="*50}')
    print(f'মোট ইউজারনেম: {len(usernames)}')
    print(f'থ্রেড সংখ্যা: {max_workers}')
    print(f'বিরতি: {base_delay} সেকেন্ড')
    print(f'{"="*50}{D}\n')
    
    time.sleep(3)
    
    # চেকিং শুরু
    valid_count = 0
    total_checked = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for username in usernames:
            # প্রতিটি রিকোয়েস্টের আগে বিরতি
            delay = base_delay + random.uniform(1, 3)
            time.sleep(delay)
            
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
        # প্রয়োজনীয় প্যাকেজ ইন্সটল চেক
        required_packages = ['cloudscraper', 'fake-useragent']
        main()
    except KeyboardInterrupt:
        print(f'\n{Y} [!] প্রোগ্রাম বন্ধ করা হচ্ছে...{D}')
    except Exception as e:
        print(f'{R} [!] Error: {e}{D}')
        print(f'{Y} টিপস: "pip install cloudscraper fake-useragent" রান করুন{D}')
