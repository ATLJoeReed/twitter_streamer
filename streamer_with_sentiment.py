from sqlalchemy import create_engine, MetaData, Table
import tweepy

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. # noqa
# Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014. # noqa

from config import settings, twitter_filters


metadata = MetaData(schema='raw')
engine = create_engine(settings.DB_URL)
tweets = Table('dem_debate_20190626', metadata, autoload=True, autoload_with=engine) # noqa
connection = engine.connect()

analyzer = SentimentIntensityAnalyzer()


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

        created_at = status.created_at
        id_str = status.id_str
        name = status.user.name
        screen_name = status.user.screen_name
        source = status.source
        followers_count = status.user.followers_count
        location = status.user.location
        description = status.user.description
        verified_account = status.user.verified

        if original_tweet:
            vs = analyzer.polarity_scores(original_tweet)
        else:
            vs = analyzer.polarity_scores(tweet)

        ins = tweets.insert().values(
            created_at_utc=created_at,
            id_str=id_str,
            name=name,
            screen_name=screen_name,
            source=source,
            followers_count=followers_count,
            location=location,
            description=description,
            verified_account=verified_account,
            tweet=tweet,
            retweeted=retweeted,
            original_tweet=original_tweet,
            neg=vs.get('neg'),
            neu=vs.get('neu'),
            pos=vs.get('pos'),
            compound=vs.get('compound'),
        )
        connection.execute(ins)

    def on_error(self, status_code):
        if status_code == 420:
            return False


auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET) # noqa
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(
    auth=api.auth,
    listener=stream_listener,
    tweet_mode='extended',
)

filters = twitter_filters.NBC_DEBATE_HASH_TAGS
filters.extend(twitter_filters.NBC_DEBATE_CANDIDATES_20190626)
# filters.extend(twitter_filters.NBC_DEBATE_CANDIDATES_20190627)

stream.filter(languages=["en"], track=filters)
