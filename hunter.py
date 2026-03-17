import os
import sys
import time
import requests
import urllib.parse
import re
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted 
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track

# تهيئة الواجهة
console = Console()

# تحميل المفتاح من ملف .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "حط_المفتاح_بتاعك_هنا":
    console.print("[bold red][!] Error: API Key is missing in .env file![/bold red]")
    exit()

# تهيئة موديل الذكاء الاصطناعي 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

def show_banner():
    banner = """
[bold red]
 ╔═══════════════════════════════════════════════════════╗
 ║  ███████╗███████╗██████╗  ██████╗                     ║
 ║  ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗                    ║
 ║    ███╔╝ █████╗  ██████╔╝██║   ██║                    ║
 ║   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║                    ║
 ║  ███████╗███████╗██║  ██║╚██████╔╝                    ║
 ║  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝                     ║
 ║   ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ ║
 ║   ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗║
 ║   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝║
 ║   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗║
 ║   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║║
 ║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝║
 ╚═══════════════════════════════════════════════════════╝
[/bold red]
[bold white]        "Logic is my only weapon." - Ayanokoji Kiyotaka[/bold white]
[bold cyan]                    Developed by: 0xHamid (Zero)[/bold cyan]
    """
    console.print(banner)

def js_hunter_module():
    console.print("\n[bold yellow][*] Module 1: Automated JS Secrets & Endpoint Hunter (Smart Regex & Resume)[/bold yellow]")
    
    try:
        target_url = Prompt.ask("[bold cyan][?] Enter the Target URL (e.g., https://target.com)[/bold cyan]")
    except UnicodeDecodeError:
        console.print("[bold red][!] Please switch your keyboard to English and try again![/bold red]")
        return
        
    if not target_url.startswith("http"):
        console.print("[bold red][!] Invalid URL. Must start with http or https.[/bold red]")
        Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold yellow]")
        return

    target_domain = urllib.parse.urlparse(target_url).netloc
    cache_file = f"cache_{target_domain.replace(':', '_')}.txt"
    juicy_data = ""

    # --- نظام الاستكمال (Resume Logic) ---
    if os.path.exists(cache_file):
        console.print(f"\n[bold green][+] Found previous saved data for {target_domain}![/bold green]")
        try:
            choice = Prompt.ask("[bold cyan][?] Do you want to resume using saved data? (y/n)[/bold cyan]", choices=["y", "n"])
        except UnicodeDecodeError:
            choice = "n"
            
        if choice == "y":
            with open(cache_file, "r", encoding="utf-8") as f:
                juicy_data = f.read()
            console.print("[bold green][+] Data loaded from cache successfully.[/bold green]")
            
    # لو مفيش كاش أو اليوزر اختار يمسح ويعيد
    if not juicy_data:
        try:
            with console.status(f"[bold green]Scanning {target_url} for JS files...[/bold green]", spinner="dots"):
                response = requests.get(target_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                js_links = []
                for script in soup.find_all('script'):
                    if script.get('src'):
                        full_url = urllib.parse.urljoin(target_url, script.get('src'))
                        js_links.append(full_url)
            
            if not js_links:
                console.print("[bold yellow][!] No external JS files found on this page.[/bold yellow]")
                Prompt.ask("\n[bold yellow]Press Enter to return...[/bold yellow]")
                return

            console.print(f"\n[bold green][+] Found {len(js_links)} JS files.[/bold green]")
            
            # فلتر سريع
            junk_libs = ['jquery', 'bootstrap', 'analytics', 'gtm', 'recaptcha', 'pixel', 'polyfill', 'adsystem', 'track', 'metrics', 'fontawesome', 'vendor', 'react-dom']
            filtered_links = [link for link in js_links if not any(junk in link.lower() for junk in junk_libs)]
            filtered_links = list(set(filtered_links))

            console.print(f"\n[bold green][+] Selected {len(filtered_links)} files for Smart Regex Scanning.[/bold green]")
            
            success_count = 0
            fail_count = 0
            
            for link in track(filtered_links, description="[bold pink]Hunting for secrets & paths...[/bold pink]"):
                try:
                    js_resp = requests.get(link, timeout=7)
                    if js_resp.status_code == 200:
                        success_count += 1
                        js_text = js_resp.text
                        file_findings = set()
                        
                        string_pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\'|`([^`\\]*(?:\\.[^`\\]*)*)`'
                        for match in re.findall(string_pattern, js_text):
                            s = match[0] or match[1] or match[2]
                            if s and 4 < len(s) < 500: 
                                junk_strings = ['<svg', '<?xml', 'data:image', 'base64,', 'rgb(', 'rgba(', 'font-family', 'border-radius', 'solid #', 'px', '100%', '<div', '<span', '<a href', 'text/javascript', 'application/json']
                                if not any(junk in s.lower() for junk in junk_strings):
                                    file_findings.add(s)

                        for comment in re.findall(r'//(.*?)[\r\n]|/\*(.*?)\*/', js_text, flags=re.DOTALL):
                            c = comment[0] or comment[1]
                            if c and 4 < len(c.strip()) < 300:
                                file_findings.add(f"[COMMENT] {c.strip()}")

                        if file_findings:
                            juicy_data += f"\n\n/* --- Target File: {link} --- */\n"
                            juicy_data += "\n".join(file_findings)
                    else:
                        fail_count += 1
                except:
                    fail_count += 1
            
            console.print(f"\n[bold yellow][=] Extraction Summary: Processed ({success_count}/{len(filtered_links)}) files | Failed/Timeout: {fail_count}[/bold yellow]")
            
            if juicy_data:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(juicy_data)
                console.print(f"[bold cyan][+] Extracted lines saved to cache: {cache_file}[/bold cyan]")
                
        except Exception as e:
            console.print(f"[bold red][!] Error during scraping: {str(e)}[/bold red]")
            return

    if not juicy_data:
        console.print("[bold yellow][!] No strings or comments found in the selected JS files.[/bold yellow]")
        Prompt.ask("\n[bold yellow]Press Enter to return...[/bold yellow]")
        return

    MAX_CHARS = 200000
    total_chars = len(juicy_data)
    
    if total_chars > MAX_CHARS:
        chunks = [juicy_data[i:i+MAX_CHARS] for i in range(0, total_chars, MAX_CHARS)]
        console.print(f"\n[bold yellow][!] The extracted data is HUGE: {total_chars} characters![/bold yellow]")
        console.print(f"[bold yellow][!] It has been split into {len(chunks)} chunks ({MAX_CHARS} chars each).[/bold yellow]")
        
        try:
            chunk_choice = Prompt.ask(f"[bold cyan][?] Which chunk do you want to analyze now? (1-{len(chunks)})[/bold cyan]", default="1")
            chunk_index = int(chunk_choice) - 1
            if chunk_index < 0 or chunk_index >= len(chunks):
                chunk_index = 0
        except (ValueError, UnicodeDecodeError):
            chunk_index = 0
            
        data_to_send = chunks[chunk_index]
        current_chunk_display = chunk_index + 1
        console.print(f"[bold green][+] Sending Chunk {current_chunk_display}/{len(chunks)} ({len(data_to_send)} chars) to AI...[/bold green]")
        report_suffix = f"_chunk_{current_chunk_display}"
    else:
        data_to_send = juicy_data
        console.print(f"\n[bold cyan][+] Payload ready! Sending {total_chars} chars to AI for deep analysis...[/bold cyan]")
        report_suffix = ""

    # === إضافة خيارات التخصيص للموديول الأول ===
    console.print("\n[bold cyan][?] What do you want the AI to extract from this JS data?[/bold cyan]")
    console.print("[1] 🕵️  Full Report (Secrets, Endpoints, Comments)")
    console.print("[2] 🔗 Endpoints Only (Clean list for Fuzzing)")
    console.print("[3] 🎯 Custom Sniper Mode (Type what you want, e.g., 'WeHex Hash codes')")
    
    try:
        ai_mode = Prompt.ask("[bold yellow]Select Analysis Mode[/bold yellow]", choices=["1", "2", "3"], default="1")
    except UnicodeDecodeError:
        ai_mode = "1"

    formatting_rules = """
    [تعليمات هامة للتنسيق]:
    - استخدم الـ Markdown باحترافية وتنسيق نظيف جداً.
    - أي مصطلح تقني بالإنجليزي، كود، مسار (Endpoint)، أو اسم متغير يجب أن يوضع بين علامات `backticks` أو داخل كتل برمجية (Code Blocks) ``` لعدم تداخل الكلام العربي مع الإنجليزي (RTL/LTR).
    - اجعل التقرير مرتباً باستخدام العناوين والنقاط لتسهيل القراءة.
    """

    if ai_mode == "2":
        prompt = f"""
        أنت خبير أمن سيبراني. البيانات التالية عبارة عن نصوص تم استخراجها من ملفات JavaScript.
        المطلوب: 
        استخراج جميع مسارات الـ API (Endpoints) والـ URLs والـ Routes فقط.
        لا تكتب أي مقدمات أو شروحات باللغة العربية. اطبع النتائج كقائمة نظيفة (كل مسار في سطر مستقل) لتسهيل استخدامها مباشرة في أدوات الفحص مثل Ffuf أو Burp Suite.
        ضع المسارات داخل Code Block.
        
        البيانات:
        {data_to_send}
        """
        report_title = "Clean Endpoints Extraction"
    
    elif ai_mode == "3":
        custom_query = Prompt.ask("[bold pink][?] What exactly are you looking for? (e.g., WeHex hash codes, AWS Keys, etc.)[/bold pink]")
        prompt = f"""
        أنت خبير أمن سيبراني. البيانات التالية مستخرجة من ملفات JavaScript للهدف.
        الباحث الأمني يطلب منك مهمة محددة جداً: ({custom_query}).
        
        المطلوب:
        ابحث حصراً وفقط عن طلب الباحث في البيانات المرفقة.
        تجاهل أي معلومات أخرى لا تتعلق بطلبه تماماً. اكتب الخلاصة والنتائج بشكل مباشر.
        
        {formatting_rules}
        
        البيانات:
        {data_to_send}
        """
        report_title = f"Custom Sniper: {custom_query}"
        
    else:
        prompt = f"""
        أنت خبير أمن سيبراني (Senior Bug Hunter). البيانات التالية عبارة عن نصوص وتعليقات تم استخراجها من ملفات JavaScript للهدف.
        
        مهمتك:
        1. فلترة النتائج وتجاهل الـ False Positives تماماً.
        2. استخراج أي API Keys, Tokens, أو Hardcoded Credentials حقيقية وواضحة.
        3. استخراج أهم مسارات الـ Endpoints والـ API Routes.
        4. استخراج أي معلومات حساسة في التعليقات.
        5. اكتب الخلاصة مباشرة.
        
        {formatting_rules}
        
        البيانات:
        {data_to_send} 
        """
        report_title = "JS Secrets Hunter (Full Report)"

    try:
        with console.status("[bold green]AI is finalizing the report...[/bold green]", spinner="aesthetic"):
            result = model.generate_content(prompt)
            full_report = result.text
            
        console.print(f"\n[bold red]🔥 [ {report_title.upper()} ] 🔥[/bold red]")
        console.print(Panel(full_report, border_style="red", title=f"[0xHamid] {report_title}"))
        
        report_filename = f"JS_Report_{target_domain.replace(':', '_')}{report_suffix}.md"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(f"# 🔥 {report_title.upper()} FOR: {target_url} {report_suffix.replace('_', ' ')} 🔥\n\n")
            f.write(full_report)
            
        console.print(f"\n[bold cyan][+] Report successfully saved to: {report_filename}[/bold cyan]")
        
    except ResourceExhausted:
        console.print("[bold red][!] Rate limit hit. Please wait a minute and try again.[/bold red]")
    except Exception as e:
        console.print(f"[bold red][!] Error from AI: {str(e)}[/bold red]")
        
    Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold yellow]")

def param_discovery_module():
    console.print("\n[bold yellow][*] Module 2: Smart Parameter & Mass Assignment Discovery[/bold yellow]")
    
    console.print("[bold cyan][?] How do you want to provide the HTTP Request?[/bold cyan]")
    console.print("[1] Read from a file (e.g., req.txt)")
    console.print("[2] Paste directly in terminal")
    
    try:
        input_choice = Prompt.ask("[bold yellow]Select option[/bold yellow]", choices=["1", "2"])
    except UnicodeDecodeError:
        console.print("[bold red][!] English keyboard please![/bold red]")
        return

    http_request = ""
    
    if input_choice == "1":
        file_path = Prompt.ask("[bold cyan][?] Enter the path to the HTTP Request file[/bold cyan]")
        if not os.path.exists(file_path):
            console.print(f"[bold red][!] File '{file_path}' not found![/bold red]")
            Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold yellow]")
            return
        with open(file_path, 'r', encoding='utf-8') as file:
            http_request = file.read()
    else:
        console.print("[bold cyan][!] Paste your complete HTTP Request below.[/bold cyan]")
        console.print("[bold red]When you are done, type 'EOF' on a new empty line and press Enter.[/bold red]")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            except UnicodeDecodeError:
                console.print("[bold red][!] Invalid char detected, skipping line...[/bold red]")
        http_request = "\n".join(lines)
        
    if not http_request.strip():
        console.print("[bold red][!] No HTTP request provided.[/bold red]")
        Prompt.ask("\n[bold yellow]Press Enter to return...[/bold yellow]")
        return
        
    try:
        with console.status("[bold green]AI is analyzing the Request Context & Headers...[/bold green]", spinner="aesthetic"):
            prompt = f"""
            أنت خبير Bug Bounty و Web Application Security.
            قم بتحليل طلب الـ HTTP التالي لاكتشاف ثغرات Mass Assignment, IDOR, Privilege Escalation, و Header Manipulation.
            
            الطلب:
            ```http
            {http_request}
            ```
            
            المطلوب منك:
            1. 🔍 **تحليل السياق والـ Headers:** ما هو هدف الطلب؟ وهل يوجد JWT, Auth tokens أو Custom Headers يمكن استغلالها؟
            2. 🎯 **اكتشاف الباراميترز (Hidden Parameters):** استنتج أهم 15 Parameter أو JSON Key مخفي متوقع وجوده في الـ Backend بناءً على سياق الطلب لتجربتهم (مثل is_admin, role, user_id, permissions). اشرح باختصار سبب اقتراحك لكل مجموعة.
            3. 📝 **استخراج Wordlist:** يجب أن تضع القائمة الصافية للباراميترز في نهاية ردك تماماً تحت عنوان بالضبط هكذا: `[WORDLIST]` بحيث يكون كل باراميتر في سطر منفصل وبدون أي رموز أو ترقيم.
            
            [تعليمات هامة للتنسيق]:
            - استخدم الـ Markdown باحترافية.
            - أي مصطلح تقني بالإنجليزي أو كود أو باراميتر يجب أن يوضع بين علامات `backticks` لعدم تداخل الكلام العربي مع الإنجليزي.
            """
            result = model.generate_content(prompt)
            full_output = result.text
            
        console.print("\n[bold red]🔥 [ SMART PARAMETER & CONTEXT ANALYSIS ] 🔥[/bold red]")
        
        # استخراج الـ Wordlist لوحده
        if "[WORDLIST]" in full_output:
            parts = full_output.split("[WORDLIST]")
            analysis_report = parts[0].strip()
            wordlist_raw = parts[1].strip()
            
            # تنظيف الـ Wordlist
            wordlist_lines = [line.strip().replace('`', '').replace('-', '').replace('*', '').strip() for line in wordlist_raw.split('\n') if line.strip()]
            
            console.print(Panel(analysis_report, border_style="red", title="[0xHamid] Context-Aware Analysis"))
            
            # حفظ الـ Wordlist
            if wordlist_lines:
                wordlist_name = f"zero_wordlist_{int(time.time())}.txt"
                with open(wordlist_name, "w", encoding="utf-8") as wf:
                    wf.write("\n".join(wordlist_lines))
                console.print(f"\n[bold green][+] Generated {len(wordlist_lines)} Context-Aware Parameters![/bold green]")
                console.print(f"[bold cyan][+] Wordlist saved successfully for Fuzzing: {wordlist_name}[/bold cyan]")
        else:
            # لو الـ AI مالتزمش بصيغة الـ [WORDLIST]
            console.print(Panel(full_output, border_style="red", title="[0xHamid] Context-Aware Analysis"))
            console.print("\n[bold yellow][!] AI didn't provide a formatted wordlist block, but you can read the suggestions above.[/bold yellow]")
            
    except ResourceExhausted:
        console.print("[bold red][!] Rate limit hit. Please wait a minute and try again.[/bold red]")
    except Exception as e:
        console.print(f"[bold red][!] Error: {str(e)}[/bold red]")
        
    Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold Menu...[/bold yellow]")

def api_auth_bypass_module():
    console.print("\n[bold yellow][*] Module 3: API Auth Bypass & BOLA (IDOR) Analyzer[/bold yellow]")
    
    console.print("[bold cyan][?] How do you want to provide the HTTP Request?[/bold cyan]")
    console.print("[1] Read from a file (e.g., req.txt)")
    console.print("[2] Paste directly in terminal")
    
    try:
        input_choice = Prompt.ask("[bold yellow]Select option[/bold yellow]", choices=["1", "2"])
    except UnicodeDecodeError:
        console.print("[bold red][!] English keyboard please![/bold red]")
        return

    http_request = ""
    
    if input_choice == "1":
        file_path = Prompt.ask("[bold cyan][?] Enter the path to the HTTP Request file[/bold cyan]")
        if not os.path.exists(file_path):
            console.print(f"[bold red][!] File '{file_path}' not found![/bold red]")
            Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold yellow]")
            return
        with open(file_path, 'r', encoding='utf-8') as file:
            http_request = file.read()
    else:
        console.print("[bold cyan][!] Paste your complete HTTP Request below.[/bold cyan]")
        console.print("[bold red]When you are done, type 'EOF' on a new empty line and press Enter.[/bold red]")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            except UnicodeDecodeError:
                console.print("[bold red][!] Invalid char detected, skipping line...[/bold red]")
        http_request = "\n".join(lines)
        
    if not http_request.strip():
        console.print("[bold red][!] No HTTP request provided.[/bold red]")
        Prompt.ask("\n[bold yellow]Press Enter to return...[/bold yellow]")
        return
        
    try:
        with console.status("[bold green]AI is tearing down the API Request for BOLA/Auth Bypass...[/bold green]", spinner="bouncingBar"):
            prompt = f"""
            أنت خبير أمن سيبراني متخصص في اختبار اختراق واجهات برمجة التطبيقات (API Security & Bug Bounty).
            قم بتحليل طلب الـ HTTP التالي لاكتشاف ثغرات BOLA (Broken Object Level Authorization) و BFLA و Auth Bypass.
            
            الطلب:
            ```http
            {http_request}
            ```
            
            المطلوب منك كتابة تقرير فني منظم جداً يحتوي على:
            1. 🔑 **تحليل المصادقة (Auth Analysis):** كيف يتم التحقق من هوية المستخدم؟ (Tokens, Cookies, Custom Headers). وهل هناك أخطاء شائعة في تنفيذها يمكن استغلالها؟
            2. 🎯 **تحديد الأهداف (Resource Identifiers):** استخرج أي معرّفات (IDs, UUIDs, Usernames) في الـ URL أو الـ Body أو الـ Headers قابلة لاختبار الـ BOLA.
            3. 🚀 **سيناريوهات الهجوم (Attack Scenarios):** اقترح 5 سيناريوهات محددة وعملية لاختبار الثغرة على هذا الطلب بالتحديد. (مثال: HTTP Parameter Pollution، إضافة .json للمسار، تغيير الـ Method، مسح الـ Header، دمج الـ IDs، إلخ).
            4. 🛠️ **Payloads جاهزة:** اكتب لي شكل الـ JSON أو الـ URL المعدل الذي يجب أن أجربه لكسر الحماية.
            
            [تعليمات هامة للتنسيق]:
            - استخدم الـ Markdown باحترافية.
            - أي مصطلح تقني بالإنجليزي، Payload، أو مسار يجب أن يوضع بين علامات `backticks` أو داخل كتل برمجية (Code Blocks) ``` لعدم تداخل الكلام العربي مع الإنجليزي ولضمان سهولة نسخ الـ Payloads.
            """
            result = model.generate_content(prompt)
            full_output = result.text
            
        console.print("\n[bold red]🔥 [ API AUTH BYPASS & BOLA REPORT ] 🔥[/bold red]")
        console.print(Panel(full_output, border_style="red", title="[0xHamid] API Security Analyzer"))
        
        # حفظ التقرير
        report_name = f"BOLA_Report_{int(time.time())}.md"
        with open(report_name, "w", encoding="utf-8") as wf:
            wf.write(f"# 🔥 API AUTH BYPASS & BOLA REPORT 🔥\n\n{full_output}")
        console.print(f"\n[bold cyan][+] Attack Plan saved successfully to: {report_name}[/bold cyan]")
        
    except ResourceExhausted:
        console.print("[bold red][!] Rate limit hit. Please wait a minute and try again.[/bold red]")
    except Exception as e:
        console.print(f"[bold red][!] Error: {str(e)}[/bold red]")
        
    Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold yellow]")

def main():
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            show_banner()
            console.print("\n[bold cyan]=== MAIN MENU ===[/bold cyan]")
            console.print("[1] JS Secrets & Endpoint Hunter (Scrape + AI)")
            console.print("[2] Context-Aware Parameter Discovery (AI)")
            console.print("[3] API Auth Bypass / BOLA Analyzer (AI)")
            console.print("[0] Exit")
            
            try:
                choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=["0", "1", "2", "3"])
            except UnicodeDecodeError:
                continue # لو داس عربي بالغلط، القائمة هترستر من غير ما يقفل
                
            if choice == "1":
                js_hunter_module()
            elif choice == "2":
                param_discovery_module()
            elif choice == "3":
                api_auth_bypass_module()
            elif choice == "0":
                console.print("[bold green]Exiting... See you in the shadows, Zero.[/bold green]")
                break
            else:
                console.print("[bold yellow][!] Module under development.[/bold yellow]")
                Prompt.ask("\n[bold yellow]Press Enter to return to the Main Menu...[/bold yellow]")
    except KeyboardInterrupt:
        console.print("\n\n[bold red][!] Program interrupted by user. Exiting...[/bold red]")
        exit()

if __name__ == "__main__":
    main()