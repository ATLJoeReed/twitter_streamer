import tweepy

from config import settings


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # print(status.place.full_name, ' - ', status.source, ' - ', ' - ', status.text)  # noqa
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


auth = tweepy.OAuthHandler(
    settings.TWITTER_APP_KEY,
    settings.TWITTER_APP_SECRET
)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# stream.filter(track=['#TheVoice'])
stream.filter(track=['HeartBeat', 'Parenthood', 'Pro-Life', 'ProLife'], is_async=True) # noqa
# stream.filter(locations=[-125,25,-65,48], async=True)
# stream.filter(locations=[-122.75,36.8,-121.75,37.8], async=True)
