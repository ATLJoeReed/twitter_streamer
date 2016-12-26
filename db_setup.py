from datetime import datetime

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, Text, DateTime
)

from config import settings


engine = create_engine(settings.DB_URL)

metadata = MetaData()

tweets = Table(
    'tweets', metadata,
    Column('ukey', Integer(), primary_key=True),
    Column('ymd', DateTime(timezone=True), default=datetime.now),
    Column('text', Text(), nullable=False)
)

metadata.create_all(engine)
