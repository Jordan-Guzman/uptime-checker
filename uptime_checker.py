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
def check_websites():
	for url in URLS:
		try:
			response = requests.get(url, timeout=1)
			if response.status_code == 200:
				print(f"{url} is UP")
			else:
				print(f"{url} is DOWN")
				send_alert(url)
		except requests.exceptions.RequestException:
			print(f"{url} is DOWN")
			send_alert(url)

# Schedule the check eveery minute
schedule.every(1).minutes.do(check_websites)

def send_alert(url):
	message = {"content": f"{url} is DOWN!"}
	requests.post(DISCORD_WEBHOOk, json=message)

# Run the scheduler
while True:
	schedule.run_pending()
	time.sleep(1)
