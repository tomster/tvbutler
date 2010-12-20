from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column
from sqlalchemy import String
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import DB_URL

engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
Base = declarative_base(metadata=metadata)

class TVShow(Base):
    __tablename__ = 'shows'

    name = Column(String, primary_key=True)
    episode = Column(String, primary_key=True)
    season = Column(String, primary_key=True)
    quality = Column(types.Enum(u'sd', u'720p',
        u'1080p', convert_unicode=True, native_enum=False), nullable=False,
        primary_key=True,
        default=u'sd')
    title = Column(String)
    filename = Column(String)
    torrent_url = Column(String)
    transmission_hash = Column(String, nullable=True, default=u'')
    status = Column(types.Enum(u'new', u'torrent_downloaded', u'file_downloaded',
        u'archived', convert_unicode=True, native_enum=False), nullable=False,
        default=u'new')

    def __repr__(self):
        return "<TVShow('%(name)s S%(season)sE%(episode)s' in %(quality)s)>" % self.__dict__

metadata.create_all(engine)

def migrate_001():
    session = Session()
    session.execute("ALTER TABLE shows ADD COLUMN transmission_hash STRING DEFAULT '';")
    session.commit()

migrations = [migrate_001]