import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import os

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
    room_type = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    images = Column(String, nullable=True)  # Store image paths as comma-separated string
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
            # If images were downloaded, convert to stored image paths
            if 'images' in item and isinstance(item['images'], list):
                # Assuming Scrapy's ImagesPipeline stores images in media/images/
                # and provides paths relative to IMAGES_STORE
                image_paths = [
                    os.path.join('media', 'images', img['path']) 
                    for img in item['images'] 
                    if img.get('path')
                ]
                # Store image paths as comma-separated string
                item['images'] = ','.join(image_paths) if image_paths else None

            hotel = Hotel(**item)
            session.add(hotel)
            session.commit()
            spider.log(f"Successfully added to database: {item['title']}")
        except Exception as e:
            spider.log(f"Error adding to database: {e}")
            session.rollback()
        finally:
            session.close()
        return item