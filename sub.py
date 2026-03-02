import requests
import os

G, R, Y, D = ('\033[1m\033[92m', '\033[1m\033[91m', '\033[1m\033[93m', '\033[0m')

try:
    with open('.name.txt', 'r') as f:
        name = f.read().strip()
except Exception:
    name = 'Anonymous'

# সতর্কতা: আপনার বট টোকেন এবং চ্যাট আইডি পাবলিক করা নিরাপদ নয়। কাজ শেষে টোকেন পরিবর্তন করে নিবেন।
BOT_TOKEN = '7079698461:AAG1N-qrB_IWHWOW5DOFzYhdFun4kBtSEQM'
CHAT_ID = '-1003275746200'
caption = f'MP-IDS Submitted by {name}'
url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'

# শুধুমাত্র .uids.txt সেন্ড করবে
files_to_send = ['.uids.txt']
success_count = 0

print(f'{Y}📤 Submitting files...{D}')

for filename in files_to_send:
    print(f'{Y}📄 Processing {filename}...{D}')
    try:
        with open(filename, 'rb') as f:
            files = {'document': (filename, f)}
            data = {'chat_id': CHAT_ID, 'caption': caption}
            
            # রিকোয়েস্ট পাঠানো হচ্ছে (কোনো লুপ বা রিট্রাই ছাড়া)
            resp = requests.post(url, data=data, files=files, timeout=10)
            
            if resp.status_code == 200 and resp.json().get('ok'):
                os.remove(filename) # সফল হলে ফাইল ডিলিট করে দিবে
                success_count += 1
                print(f'{G}✅ {filename} submitted successfully{D}')
            else:
                print(f'{R}❌ Failed to submit {filename}. Server responded with an error.{D}')
    except FileNotFoundError:
        print(f'{R}❌ File {filename} not found!{D}')
    except Exception as e:
        print(f'{R}❌ Network or connection error occurred while submitting {filename}.{D}')

# ফাইনাল মেসেজ
if success_count == len(files_to_send):
    print(f'\n{G}✅ Thank you! {name}, Your .uids file has been submitted to Admin.{D}\n')
else:
    print(f'\n{R}⚠️ Submission failed or incomplete. Please check your connection and try again later.{D}\n')
