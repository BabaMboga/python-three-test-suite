from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .import Base, session

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key= True)
    name = Column (String, nullable = False)
    hometown = Column (String, nullable = False)
    concerts = relationship('Concert', backref='band')

    def concerts(self):
        return self.concerts
    
    def venues(self):
        return list({concert.venue from concert in self.concerts})
    
    def play_in_venue(self, venue, date):
        concert = Concert(band=self, venue=venue, date=date)
        session.add(concert)

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls):
        return max(session.query(cls).all(), key=lambda band: len(band.concerts))