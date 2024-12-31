import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from scrapy.exceptions import DropItem

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    title = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    image_urls = Column(String, nullable=True)  # Store image URLs as a comma-separated string
    url = Column(String, nullable=False)

class HotelScrapperPipeline:
    def __init__(self):
        DATABASE_URL = "postgresql://shino:shinopass123@postgres:5432/llm_test_DB"
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            # Join image URLs as a single string
            if 'image_urls' in item and isinstance(item['image_urls'], list):
                item['image_urls'] = ','.join(item['image_urls'])

            # Save data to the database
            hotel = Hotel(**item)
            session.add(hotel)
            session.commit()
            spider.log(f"Successfully added to database: {item['title']}")
        except Exception as e:
            spider.log(f"Error adding to database: {e}")
            session.rollback()
            raise DropItem(f"Failed to process item: {e}")
        finally:
            session.close()
        return item
