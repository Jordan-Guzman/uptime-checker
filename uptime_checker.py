import requests
import schedule
import time
import logging

# Configure logging to write a file with timestamps
logging.basicConfig(
	filename="uptime_checker.log",
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_status(url, status):
	"""Log the status of the website"""
	logging.info(f"{url} is {status}")

# List of websites to monitor
URLS = ["https://example.com", "https://yourclientside.com", "https://www.github.com", "https://downforeveryoneorjustme.com"]
DISCORD_WEBHOOk = "https://discord.com/api/webhooks/1343700023287877703/yMt4UFl9vVGX6Cdacow_Vrdmr15NiB56U_-Y-xfTGbcIJZxqbwRZT36LvlbsiAxDPV5i"

# Check website status
def check_websites(url, retries=3, delay=5):
	"""Check website status with retry mechanism"""
	for attempt in range(1, retries + 1):
		try:
			response = requests.get(url, timeout=2)

			if response.status_code == 200:
				print(f"{url} is UP")
				log_status(url, "UP")
				return True
			else:
				print(f"{url} is DOWN (Status: {response.status_code})")
				log_status(url, f"DOWN (Status: {response.status_code})")
				return False
		
		except requests.exceptions.RequestException as e:
			print(f"Attempt {attempt}: {url} is unreachable - {e}")
			log_status(url, f"Unreachable (Attempt {attempt})")

			if attempt < retries:
				print(f"Retrying in {delay} seconds...")
				time.sleep(delay)

	print(f"{url} is DOWN after {retries} retries")
	log_status(url, f"DOWN after {retries} retries")
	return False

# Schedule the check eveery minute
schedule.every(1).minutes.do(check_websites)

def send_alert(url):
	message = {"content": f"{url} is DOWN!"}
	requests.post(DISCORD_WEBHOOk, json=message)

for url in URLS:
	check_websites(url)
