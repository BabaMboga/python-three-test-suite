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

