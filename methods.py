from models import db,Venue,Artist,Show
from forms import *
#....................................................#
# Function to edit both Artists and Venue  lists     #
#....................................................#
def edit_artist_venue(form_request,artist_venue,flag =0):
    artist_venue.name = form_request['name']
    artist_venue.city = form_request['city']
    artist_venue.state = form_request['state']
    if flag == 1:
      artist_venue.address = form_request['address']
    artist_venue.phone = form_request['phone']
    artist_venue.genres = form_request.getlist('genres')
    artist_venue.image_link = form_request['image_link']
    artist_venue.facebook_link = form_request['facebook_link']
    artist_venue.website_link = form_request['website_link']
    if flag == 0:
     if form_request['seeking_venue'] == True:
      artist_venue.looking_venues = "True" 
     else:
      artist_venue.looking_venues = "False"
    if flag == 1:
     if form_request['seeking_talent'] == True:
      artist_venue.looking_venues = "True" 
     else:
      artist_venue.looking_venues = "False"

    artist_venue.seeking_description = form_request['seeking_description']
    db.session.commit()
#....................................................#
# Function to delete both Artists and Venue  lists   #
#....................................................#
def deletes(num_delete_shows,delete_shows,delete_venue_artist):
    index = 0
    while index < num_delete_shows:
      db.session.delete(delete_shows[index])
      db.session.commit()
      index +=1
    db.session.delete(delete_venue_artist)
    db.session.commit()
#....................................................#
# Function to add both Artists and Venue lists       #
#....................................................#
def venue_artist_form(request_form,flag=0):

    Name = request_form['name']
    City = request_form['city']
    State = request_form['state']
    Phone = request_form['phone']
    Genres = request_form.getlist('genres')
    Image_link = request_form['image_link']
    Facebook_link = request_form['facebook_link']
    Website_link = request_form['website_link']
    Seeking_description = request_form['seeking_description']
    if flag == 0:
     Address = request_form['address']
     if request_form['seeking_talent'] == True:
      looking_talent = "True" 
     else:
      looking_talent = "False"

     venue = Venue(name=Name, city=City, 
                   state=State, address=Address, 
                   phone=Phone, genres=Genres,image_link=Image_link, 
                   facebook_link=Facebook_link,website_link=Website_link, 
                   looking_talent=looking_talent, seeking_description=Seeking_description)
     db.session.add(venue)
    else:
     if request_form['seeking_venue'] == True:
      looking_venues = "True" 
     else:
      looking_venues = "False"
     artist = Artist(name=Name, city=City, state=State, 
                     phone=Phone, genres=Genres,image_link=Image_link, 
                     facebook_link=Facebook_link,website_link=Website_link, 
                     looking_venues=looking_venues, seeking_description=Seeking_description)
     db.session.add(artist)
    db.session.commit()
#....................................................#
# Function to show both Artists and Venue lists      #
#....................................................#
def shows_venue_artist(num_show_list,shows_lists,flag=0):
     value_shows = []
     index = 0
     while index < num_show_list:
      if flag == 0:
        value_shows.append({
            "artist_id": shows_lists[index].artist_id,
            "artist_name": shows_lists[index].artists.name,
            "artist_image_link": shows_lists[index].artists.image_link,
            "start_time": shows_lists[index].start_time.strftime("%Y-%m-%d %H:%M:%S")
        })
      else:
        value_shows.append({
            "artist_id": shows_lists[index].venue_id,
            "artist_name": shows_lists[index].venues.name,
            "artist_image_link": shows_lists[index].venues.image_link,
            "start_time": shows_lists[index].start_time.strftime("%Y-%m-%d %H:%M:%S")
        })
      index +=1
     return value_shows
#....................................................#
# Function to search both Artists and Venue lists    #
#....................................................#
def search(num_searched,searched,flag = 0):

    index = 0
    value = []

    while index < num_searched:

      filter_format_id = Show.venue_id==searched[index].id
      
      filter_format_time = Show.start_time > datetime.now()
      if flag == 0 :
        upcoming_shows = Show.query.join(Venue).filter(filter_format_id, filter_format_time)
      else :
        upcoming_shows = Show.query.join(Artist).filter(filter_format_id, filter_format_time)

      value.append({
      "name": searched[index].name,
      "id": searched[index].id,
      "num_upcoming_shows": upcoming_shows
      })

      index +=1

    return value
#....................................................#
# Function to view Venue lists                       #
#....................................................#
def venue_city_state(num_city_state,citys_states):

    index = 0

    while index < num_city_state:
  
     fetched_venues = Venue.query.filter_by(city=citys_states[index].city).filter_by(state=citys_states[index].state).all() 

     data_venues = []

     for fetched_venue in fetched_venues:

      num_upcoming_shows = len(Show.query.filter(Show.venue_id==fetched_venue.id).filter(Show.start_time>datetime.now()).all()) 
      
      data_venues.append({
        'name':fetched_venue.name,
        'id':fetched_venue.id,
        'num_upcoming_shows': num_upcoming_shows
      })

     index +=1
     return data_venues