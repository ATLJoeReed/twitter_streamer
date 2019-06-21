import tweepy

from config import settings


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        retweeted = False
        tweet = status.text
        original_tweet = None
        if hasattr(status, 'retweeted_status'):
            retweeted = True
            try:
                original_tweet = status.retweeted_status.extended_tweet["full_text"] # noqa
            except AttributeError:
                original_tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text

        try:
            screen_name = status.user.screen_name
        except AttributeError:
            screen_name = None

        if original_tweet:
            output_tweet = original_tweet
        else:
            output_tweet = tweet
        print(screen_name, '-', retweeted, '-', output_tweet)
        print('-'*120)

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
stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended') # noqa

stream.filter(track=['KamalaHarris'], is_async=True)
