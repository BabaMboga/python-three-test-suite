from app import init_db, session
from app.models import Band, Venue, Concert

#Initialise the database and create tables
init_db()

#optionally, add some test data here
band = Band(name="Rockstars", hometown="Nairobi")
venue = Venue(title="Madison Squre Garden", city="New York")
session.add_all([band, venue])
session.commit()

#add a concert
band.play_in_venue(venue, "2023-03-15")
print(f"Band '{band.name}' plated at {venue.title} on {band.concerts[0].date}")