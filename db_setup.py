from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, Text, DateTime, Boolean, Numeric
)

from config import settings


engine = create_engine(settings.DB_URL)

metadata = MetaData(schema='raw')

tweets = Table(
    'dem_debate_20190626', metadata,
    Column('ukey', Integer(), primary_key=True),
    Column('created_at_utc', DateTime(timezone=False)),
    Column('id_str', Text(), nullable=True),
    Column('name', Text(), nullable=True),
    Column('screen_name', Text(), nullable=True),
    Column('source', Text(), nullable=True),
    Column('followers_count', Integer(), nullable=True),
    Column('location', Text(), nullable=True),
    Column('description', Text(), nullable=True),
    Column('verified_account', Boolean(), default=False),
    Column('tweet', Text(), nullable=False),
    Column('retweeted', Boolean(), default=False),
    Column('original_tweet', Text(), nullable=True),
    Column('neg', Numeric(5, 3), nullable=True),
    Column('neu', Numeric(5, 3), nullable=True),
    Column('pos', Numeric(5, 3), nullable=True),
    Column('compound', Numeric(5, 3), nullable=True),
)

metadata.create_all(engine)
