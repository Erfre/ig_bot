from img_bot import img_bot
import schedule
import time
from random import randint

def start_bot():
    delay = randint(3, 30000)
    now = time.time()
    run = time.strftime("%H:%M", time.localtime(now+delay))
    print("Next bot run is at: " + run)
    time.sleep(delay)
    # Start a session and at the end post an image
    bot = img_bot()
    bot.start_session()
    print("Done for the day")

schedule.every().day.at('09:00').do(start_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
