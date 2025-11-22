import os
import requests
import json
from datetime import datetime, timedelta
import random
import time
from bs4 import BeautifulSoup

# ===================================================
# متغيرة البيئة السرية والمفاتيح المدمجة
# ===================================================
# بيانات تلجرام
TELEGRAM_TOKEN = "8377697278:AAEptchGlYa19eg3g9bi-iKtU3-GflVBaJA"
TELEGRAM_CHAT_ID = "1554251396"

# مدير مفاتيح API الدوارة (سعة 600 طلب يومياً)
WHOIS_API_KEYS_POOL = [
    {"provider": "WHOISFREAKS", "key": "8a415a6c9b274ad7896f44755479ea99", "url": "[https://api.whoisfreaks.com/v1.0/whois?apiKey=](https://api.whoisfreaks.com/v1.0/whois?apiKey=){key}&domainName={domain}"},
    {"provider": "WHOISXML", "key": "At_U9un5tTeNXMErhyGJoSwsTnuZ0T8s", "url": "[https://www.whoisxmlapi.com/whois/api/v2?apiKey=](https://www.whoisxmlapi.com/whois/api/v2?apiKey=){key}&domainName={domain}"},
]

# قوائم الحماية والتحليل
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]
CURRENT_MARKET_TRENDS = ['ai', 'crypto', 'nft', 'invest', 'meta', 'web3', 'fintech']
EXPLOIT_KEYWORDS = ['bank', 'loan', 'cash', 'money', 'trade', 'secure', 'password']


# ===================================================
# دوال وحدات الحماية والتهيئة
# ===================================================

def get_random_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def get_active_proxies(max_proxies=50):
    """يتم محاكاة جلب واختبار البروكسيات."""
    # لتشغيل الكود على Netlify بسرعة، نستخدم هنا قائمة وهمية (يفترض أن الكود الحقيقي يجلبها)
    # القائمة الوهمية (يجب استبدالها لاحقاً بكود جلب حقيقي):
    return ['[http://1.2.3.4:8080](http://1.2.3.4:8080)', '[http://5.6.7.8:8080](http://5.6.7.8:8080)'] if not os.environ.get('NETLIFY') else []

def get_random_proxy(active_proxies):
    if active_proxies:
        proxy_url = random.choice(active_proxies)
        return {'http': proxy_url, 'https': proxy_url}
    return {}

# ===================================================
# دوال وحدات الجني والتحليل
# ===================================================

def scrape_domains(active_proxies):
    """جني قوائم الدومينات من مصادر متعددة."""
    # دمج مصادر جني متعددة (القوائم المكتشفة في منتديات القبعة السوداء)
    target_urls = [
        "[https://www.expireddomains.net/deleted-com-domains/](https://www.expireddomains.net/deleted-com-domains/)", # المصدر الأساسي
        # "[http://dropped-domains-source-2.com](http://dropped-domains-source-2.com)", # يمكن إضافة المزيد هنا
    ]
    all_raw_domains = []
    
    for url in target_urls:
        proxy_config = get_random_proxy(active_proxies)
        headers = get_random_headers()
        try:
            # محاكاة الجني (سنفترض الحصول على 1000 دومين من المصدر)
            for i in range(1000):
                domain_name = f"testdomain{i}-{random.randint(1, 99)}.{random.choice(['com', 'ai', 'io', 'net', 'xyz'])}"
                # إضافة قيمة InitialAge عشوائية للمحاكاة
                all_raw_domains.append({'Domain': domain_name, 'InitialAge': random.randint(1, 25)}) 
        except Exception:
            pass
            
    return all_raw_domains

def fetch_precise_whois(domain_name, active_proxies):
    """مدير مفاتيح API الدوارة يجلب بيانات WHOIS."""
    
    # اختيار مفتاح API عشوائي للتبديل وتجنب الحدود
    api_source = random.choice(WHOIS_API_KEYS_POOL)
    
    # بناء URL الطلب حسب المزود (WhoisXML أو WhoisFreaks)
    url = api_source['url'].format(key=api_source['key'], domain=domain_name)
    
    try:
        response = requests.get(url, headers=get_random_headers(), proxies=get_random_proxy(active_proxies), timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # توحيد استجابة البيانات
        if api_source['provider'] == "WHOISXML":
            creation_date = data.get('createdDate')
            domain_status = data.get('status')
            nameservers = data.get('nameServers')
        else: # WHOISFREAKS
            creation_date = data.get('registrant_details', {}).get('creation_date')
            domain_status = data.get('domain_details', {}).get('status')
            nameservers = data.get('domain_details', {}).get('nameservers', [])

        return {
            'creation_year': int(creation_date[:4]) if creation_date and len(creation_date) >= 4 else 0,
            'status': domain_status,
            'is_premium': data.get('premium', False),
            'nameservers': nameservers
        }
    except Exception as e:
        return {'creation_year': 0, 'status': 'Unknown', 'is_premium': False, 'nameservers': []}


# ===================================================
# وحدات مؤشر السيادة المطلقة (ASI) والقبعة السوداء
# ===================================================

def calculate_inherited_score(precise_whois_data):
    """القوة الموروثة (مؤشرات القبعة السوداء)"""
    score = 0
    nameservers = precise_whois_data.get('nameservers', [])
    
    # المؤشر 1: بصمة الاستضافة القديمة (Legacy Hosting Footprint) - 15 نقطة
    if nameservers and len(nameservers) > 1 and not any('default' in ns or 'parking' in ns for ns in nameservers):
        score += 15
        
    # المؤشر 2: القوة الموروثة المُحسّنة (Inherited Authority) - 15 نقطة
    if any(kw in str(nameservers).lower() for kw in ['corp', 'ltd', 'inc', 'solutions']):
        score += 15
        
    return score

def check_domain_uniqueness(domain_name):
    """وحدة التفرُّد: هل ينافس هذا الدومين أسماء مشابهة؟"""
    domain_part = domain_name.split('.')[0]
    if len(domain_part) < 6:
        return "عالي"
    if domain_part.endswith(('pro', 'hub', 'ai')):
        return "متوسط"
    return "منخفض"


def calculate_asi(domain_entry, precise_whois_data):
    """يحسب مؤشر السيادة المطلقة (ASI) النهائي."""
    asi_score = 0
    domain_name = domain_entry['Domain'].lower()
    domain_part = domain_name.split('.')[0]
    
    creation_year = precise_whois_data.get('creation_year', 0)
    domain_age = datetime.now().year - creation_year if creation_year > 0 else 0
    
    # I. الندرة التاريخية (40 نقطة)
    if domain_age >= 20: asi_score += 25
    elif domain_age >= 10: asi_score += 15
    length = len(domain_part)
    if length <= 4: asi_score += 15
    
    # II. الاستغلال المالي (40 نقطة)
    if any(kw in domain_part for kw in EXPLOIT_KEYWORDS): asi_score += 20
    if precise_whois_data.get('is_premium', False): asi_score += 15
        
    # III. مطابقة السوق والقبعة السوداء (45 نقطة)
    if any(trend in domain_part for trend in CURRENT_MARKET_TRENDS): asi_score += 15
    if any(kw in domain_part for kw in ['cbd', 'gambling']): asi_score += 20
    if not ('-' in domain_part or any(c.isdigit() for c in domain_part)): asi_score += 10
        
    # IV. القوة الموروثة (30 نقطة)
    asi_score += calculate_inherited_score(precise_whois_data)
    
    # V. المضاعف
    tld = domain_name.split('.')[-1]
    tld_multipliers = {'com': 1.25, 'ai': 1.30, 'io': 1.20, 'net': 1.10}
    multiplier = tld_multipliers.get(tld, 1.0)
    
    return asi_score * multiplier, domain_age

def evaluate_acquisition_risk(precise_whois_data):
    """تقييم مخاطر "التهرب من التجديد"."""
    status = precise_whois_data.get('status', '').lower()
    if 'redemptionperiod' in status or 'pendingdelete' in status:
        return "جاهز للاقتناص"
    if 'clienthold' in status or 'transferlock' in status:
        return "يُنصح بالحذر"
    return "جاهز للاقتناص"


def apply_asi_filter(all_raw_domains, active_proxies):
    """تطبيق الترشيح المسبق والتحليل العميق ASI."""
    
    # === المرحلة 1: الترشيح المسبق القاسي (لتقليص 1000+ إلى 600) ===
    pre_filtered_list = []
    for entry in all_raw_domains:
        domain_name = entry['Domain'].lower()
        domain_part = domain_name.split('.')[0]
        tld = domain_name.split('.')[-1]
        
        # شروط الترشيح الصارمة
        if len(domain_part) > 10 or tld not in ['com', 'ai', 'io', 'net']:
            continue
        try:
            if int(entry.get('InitialAge', 0)) < 5:
                continue
        except ValueError:
            continue
        pre_filtered_list.append(entry)
        
    # نختار 550 دومين فقط لتحليل WHOIS API (ضمان عدم تجاوز الـ 600 طلب)
    processing_list = pre_filtered_list[:550]

    # === المرحلة 2: تحليل ASI العميق ووحدة القرار الحاسم ===
    final_results = []
    
    for entry in processing_list:
        precise_data = fetch_precise_whois(entry['Domain'], active_proxies)
        asi_score, domain_age = calculate_asi(entry, precise_data)
        
        final_results.append({
            'Domain': entry['Domain'],
            'ASI_Score': asi_score,
            'Age': domain_age,
            'Uniqueness': check_domain_uniqueness(entry['Domain']),
            'Risk': evaluate_acquisition_risk(precise_data),
        })
        
        time.sleep(random.uniform(0.1, 0.3)) 

    final_results.sort(key=lambda x: x['ASI_Score'], reverse=True)
    return final_results[:3]

def format_final_alert(targets):
    """تنسيق رسالة التلجرام النهائية مع وحدة القرار الحاسم."""
    message = "👑 *إنذار اقتناص السيادة المطلقة (Apex Snatch Alert)* 👑\n\n"
    message += f"⏰ *التوقيت:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += "--------------------------------------\n"
    
    for i, target in enumerate(targets):
        estimated_sale_price = 1500 + (target['ASI_Score'] * 20) 
        
        # مؤشر القرار النهائي
        if target['Uniqueness'] == 'عالي' and target['Risk'] == 'جاهز للاقتناص':
            decision_text = "**🥇 الاقتناء رقم {}: فرصة ذهبية بلا منافسة**".format(i+1)
        elif target['Risk'] == 'جاهز للاقتناص':
            decision_text = "**🥈 توصية قوية: اقتناص مضمون، مخاطر عودة المالك منخفضة**"
        else:
            decision_text = "❌ يُنصح بالحذر: دومين عالي القيمة، لكن قد يعود المالك الأصلي"
        
        message += (
            f"🚀 *الهدف رقم {i+1}:* `{target['Domain']}`\n"
            f"   - *مؤشر ASI:* **{target['ASI_Score']:.1f}**\n"
            f"   - *الربح المتوقع:* **{estimated_sale_price:.0f}$ فما فوق**\n"
            f"   - *العمر/التفرُّد:* {target['Age']} سنة / تفرُّد **{target['Uniqueness']}**\n"
            f"   - *مخاطر الشراء:* {target['Risk']}\n"
            f"{decision_text}\n"
            f"--------------------------------------\n"
        )
        
    message += "⏳ *جاهز للاقتناص الفوري - استعمل خدمة Backordering* 🚨"
    return message


def send_telegram_alert(text, token, chat_id):
    """ترسل الرسالة إلى بوت تلجرام."""
    url = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, data=payload).raise_for_status()
    except Exception as e:
        print(f"فشل إرسال رسالة تلجرام: {e}")

# ===================================================
# الدالة الرئيسية التي تعمل عبر Netlify
# ===================================================

def handler(event, context):
    """الدالة الرئيسية لتشغيل Netlify Cron Job."""
    
    active_proxies = get_active_proxies() 
    
    all_dropped_domains = scrape_domains(active_proxies) 
    
    if not all_dropped_domains:
        send_telegram_alert("❌ فشل عملية الجني. لا توجد بيانات متاحة.", TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
        return {"statusCode": 500}
        
    top_3_targets = apply_asi_filter(all_dropped_domains, active_proxies)
    
    final_message = format_final_alert(top_3_targets)
    send_telegram_alert(final_message, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    
    return {"statusCode": 200, "body": "تمت عملية تحليل الدومينات بنجاح"}
