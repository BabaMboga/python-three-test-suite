import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Band, Venue, Concert



@pytest.fixture(scope="module")
def session():
    # create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def create_sample_data(session):
    #sample data for tests

    band1 = Band(name="The Beatles", hometown="Liverpool")
    band2 = Band(name= "The Rolling Stone", hometown="London")
    venue1 = Venue(title="Madison Square Garden", city="New York")
    venue2 = Venue(title="The 02", city="London")

    session.add_all([band1, band2, venue1, venue2])
    session.commit()

    concert1 = Concert(band=band1, venue=venue1, date="2024-01-01")
    concert2 = Concert(band=band1, venue=venue2, date="2024-02-01")
    concert3 = Concert(band=band2, venue=venue2, date="2024-03-01")

    session.add_all([concert1, concert2, concert3])
    session.commit()

    return {
        "band1":band1,
        "band2":band2,
        "venue1":venue1,
        "venue2":venue2,
        "concert1":concert1,
        "concert2":concert2,
        "concert3":concert3
    }

def test_band_concerts(session, create_sample_data):
    band1 = create_sample_data["band1"]
    venue1 = create_sample_data["venue1"]

    #Band plays at the same venue again
    band1.play_in_venue(venue1, "2024-04-01")
    session.commit()

    assert len(band1.concerts()) == 3

def test_band_all_introductions(session, create_sample_data):
    band1 = create_sample_data["band1"]
    introductions = band1.all_introductions()
    assert len(introductions) == 2
    assert introductions[0] == "Hello New York !!!!! We are The Beatles and we're from Liverpool"

def test_band_most_performances(session, create_sample_data):
    band_most_performances = Band.most_performances()
    assert band_most_performances.name == "The Beatles"

def test_venue_concerts(session, create_sample_data):
    venue1 = create_sample_data["venue1"]
    assert len(venue1.concerts())

def test_venue_bands(session, create_sample_data):
    venue2 = create_sample_data["venue2"]
    assert len(venue2.bands()) == 2

def test_venue_concert_on(session, create_sample_data):
    venue2 = create_sample_data["venue2"]
    concert = venue2.concert_on("2024-02-01")
    assert concert.band.name == "The Beatles"

def test_venue_most_frequent_band(session, create_sample_data):
    venue2 = create_sample_data["venue2"]
    most_frequent_band = venue2.most_frequent_band()
    assert most_frequent_band.name == "The Beatles"

def test_concert_band(session, create_sample_data):
    concert1 = create_sample_data["concert1"]
    assert concert1.band().name == "The Beatles"

def test_concern_venue(session, create_sample_data):
    concert1 = create_sample_data["concert1"]
    assert concert1.venue().title == "Madison Square Garden"

def test_concert_hometown_show(session, create_sample_data):
    concert1 = create_sample_data["concert1"]
    concert2 = create_sample_data["concert2"]

    #Not in the band's hometown
    assert not concert1.hometown_show() 
    #Band plays in its hometown
    assert concert2.hometown_show()

def test_concert_introduction(session, create_sample_data):
    concert1 = create_sample_data["concert1"]
    intro = concert1.introduction()
    assert intro == "Hello New York!!!!! We are The Beatles and we're from Liverpool"