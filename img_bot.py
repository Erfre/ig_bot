import sys

from time import sleep
from random import randint, choice
from InstagramAPI import InstagramAPI
from json_loader import get_account
from json_loader import get_settings
from db_manager import db_manager

from instapy import InstaPy

class img_bot:
    def __init__(self):
        self.api = None
        self.pic_api = None
        self.db = None
        self.photo = None
        self.conn = None
        self.tags = None
        self.similar_acc = None

    def db_connect(self, subreddit):
        path, img_path = get_settings(subreddit)

        self.db = db_manager(path)
        self.db.table = subreddit
        self.conn = self.db.create_connect()
        self.db.count_row(self.conn)
        return img_path

    def start_session(self):
        """
        Startes a session for each account in the json file. By creating a random schedule
        of functions to go through before moving to the next account."""
        accounts = get_account()
        for account in accounts:
            delay = randint(7,18)
            print("\nSessions started for user: ", account["username"])
            subreddit = account["subreddit"]
            # These are list which get replaced with every loop
            self.similar_acc = account["similar_accounts"]
            self.tags = account["tags"]
            self.pic_api = InstagramAPI(account["username"], account["password"])
            self.api = InstaPy(username=account["username"], password=account["password"], multi_logs=True)
            self.api.login()
            sleep(delay)
            img_path = self.db_connect(subreddit)
            self.schedule()
            sleep(delay)
            self.pic_api.login()
            self.post_image(img_path)
            self.end_session()
            print("Session done for user: ", account["username"])

    def schedule(self):
        """
        Chooses what functions to run.
        Sleeps for a minimum of 10 minutes to avoid bans.
        """
        runs = randint(1,8)
        functions = [self.follow_people, self.interact_feed, self.unfollow_inactive,
                self.interact_tags]
        while runs > 0:
            try:
                choice(functions)()
            except:
                continue
            cooldown = randint(601, 1800)
            sleep(cooldown)
            runs -= 1
        return

    def follow_people(self):
        """Follow people from a list of similar acccounts"""
        follow = randint(20, 150)
        pictures = randint(1,5)
        interact = randint(20, 45)
        print("Started following users. Total number to follow: ", follow)
        self.api.set_user_interact(amount=pictures, randomize=True, percentage=interact, media='Photo')
        self.api.follow_user_followers(self.similar_acc, amount=follow, randomize=True, sleep_delay=600)
        return


    def unfollow_inactive(self):
        """Unfollows inactive users """
        unfollow = randint(20, 150)
        print("Started unfollwing people. Total number to unfollow: ", unfollow)
        self.api.set_dont_unfollow_active_users(enabled=True, posts=3)
        self.api.unfollow_users(amount=unfollow, onlyNotFollowMe=True, sleep_delay=600)
        return

    def interact_feed(self):
        """Like pictures in the feed and go into profiles and like pictures."""
        likes = randint(2,35)
        interact = randint(20, 45)
        pictures = randint(1, 5)
        print("Started interacting with feed. Total likes to give: ", likes)
        self.api.set_user_interact(amount=pictures, randomize=True, percentage=interact, media='Photo')
        self.api.like_by_feed(amount=likes, randomize=True, interact=True)
        return

    def interact_tags(self):
        """Interact with users based off tags."""
        interact = randint(20, 45)
        tag_likes = randint(5, 30)
        pictures = randint(1, 5)
        print("Started looking at tags. Total likes to give: ", tag_likes)
        self.api.set_user_interact(amount=pictures, randomize=True, percentage=interact, media='Photo')
        self.api.like_by_tags(self.tags, amount=tag_likes, interact=True)
        return

    def end_session(self):
        self.db.close_connection(self.conn)
        self.pic_api.logout()
        self.api.end()

    def post_image(self, path):
        """Post a random picture from database and delete row from the database """

        row = self.db.get_random_row(self.conn, 1)

        id = row[0]
        img_path = path + row[1] + '0.jpg'
        description = row[2]
        # Try uploading the picture and if that's not working then just delete the image and db entry
        while True:
            try:
                self.pic_api.uploadPhoto(img_path, caption=description)
                print("Image uploaded: " + row)
                print("Removing from database" + str(id))
                self.db.delete_row(self.conn, row)
                break
            except:
                print("Problem detected. Deleted from database: " + str(id), sys.exc_info()[0])
                self.db.delete_row(self.conn, row)
        return
