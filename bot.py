import requests
import random
import time
import string
from bs4 import BeautifulSoup

# === CONFIG ===
REGISTER_URL = "https://coinkove.com/?handler=Subscribe"
HOME_URL = "https://coinkove.com/"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
]
COUNTRIES = ["Jamaica", "Austria", "Canada", "Brazil", "Japan", "Indonesia"]
NAMES = ["Voidd", "Zeroth", "Gloomy", "Skye", "Nyx", "Dread", "Kairo"]

# === FUNCTIONS ===
def generate_random_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{prefix}@gmail.com"

def generate_random_name():
    return random.choice(NAMES)

def get_verification_token(session):
    resp = session.get(HOME_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})
    return token_input['value'] if token_input else None

def register_wallet(wallet_address, index):
    session = requests.Session()
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": HOME_URL,
        "Origin": "https://coinkove.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    session.headers.update(headers)

    token = get_verification_token(session)
    if not token:
        print(f"[{index}] Gagal ambil token.")
        return

    fullname = generate_random_name()
    email = generate_random_email()
    country = random.choice(COUNTRIES)

    data = {
        "Fullname": fullname,
        "emailaddress": email,
        "country": country,
        "walletaddress": wallet_address,
        "__RequestVerificationToken": token
    }

    response = session.post(REGISTER_URL, data=data)
    if response.status_code == 200:
        print(f"[{index}] {email} | {wallet_address} | {country}")
    else:
        print(f"[{index}] Gagal daftar | Status: {response.status_code}")

# === MAIN ===
with open("address.txt", "r") as f:
    addresses = [line.strip() for line in f if line.strip()]

for i, addr in enumerate(addresses, start=1):
    register_wallet(addr, i)
    time.sleep(random.uniform(3, 7))  # delay biar aman
