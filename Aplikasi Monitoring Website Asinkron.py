import asyncio
import aiohttp
from datetime import datetime

# Daftar situs yang akan dimonitor
URLS = [
    "https://openai.com",
    "https://example.com",
    "https://www.python.org",
    "https://httpstat.us/503",  # contoh situs yang akan mengembalikan error
    "https://httpstat.us/404"   # contoh situs yang akan mengembalikan error
]

LOG_FILE = "log.txt"

async def log_to_file(message: str):
    """Mencatat log ke file log.txt."""
    async with asyncio.Lock():
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")

async def check_website(session, url):
    """Mengecek status HTTP dari sebuah situs."""
    try:
        async with session.get(url) as response:
            status = response.status
            now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            if status == 200:
                message = f"{now} {url} - Status: {status}"
            else:
                message = f"{now} {url} - Status: {status} SITE DOWN!"
                print('\a')  # bunyi notifikasi di terminal jika down
            print(message)
            await log_to_file(message)
    except Exception as e:
        now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        message = f"{now} {url} - ERROR: {str(e)}"
        print('\a')  # bunyi notifikasi di terminal jika error
        print(message)
        await log_to_file(message)

async def monitor_websites():
    """Melakukan monitoring website dalam loop tanpa henti."""
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [check_website(session, url) for url in URLS]
            await asyncio.gather(*tasks)
            await asyncio.sleep(10)  # tunggu 10 detik sebelum pengecekan berikutnya

if __name__ == "__main__":
    print("Memulai Monitoring Website...")
    asyncio.run(monitor_websites())
