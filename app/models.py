# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, session

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)
    concerts = relationship('Concert', back_populates='band')

    def get_concerts(self):
        return self.concerts

    def venues(self):
        return list({concert.venue for concert in self.concerts})

    def play_in_venue(self, venue, date):
        concert = Concert(band=self, venue=venue, date=date)
        session.add(concert)
        session.commit()

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls):
        return max(session.query(cls).all(), key=lambda band: len(band.concerts))

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)
    concerts = relationship('Concert', back_populates='venue')

    def get_concerts(self):
        return self.concerts

    def bands(self):
        return list({concert.band for concert in self.concerts})

    def concert_on(self, date):
        return session.query(Concert).filter_by(venue_id=self.id, date=date).first()

    def most_frequent_band(self):
        bands = {concert.band for concert in self.concerts}
        return max(bands, key=lambda band: len(band.concerts))

class Concert(Base):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    date = Column(String)

    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def hometown_show(self):
        return self.venue.city == self.band.hometown

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
