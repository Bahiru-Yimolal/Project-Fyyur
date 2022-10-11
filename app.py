#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment 
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from models import db,Venue,Artist,Show
from methods import venue_city_state,search,shows_venue_artist,venue_artist_form,deletes,edit_artist_venue
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database
# Connected to my local database with user name: postgres, password:newpasswords, port:5432 and database name:fyyurproject
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)# inorder to register th sqlalchemy extension in the current app because we are using another package for the models

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  ................................................................
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  city_state = Venue.query.distinct(Venue.city, Venue.state)
  citys_states = city_state.all()
  num_city_state  = city_state.count()
  fetch_venue = []
  index = 0
  while index < num_city_state:
      fetch_venue.append({    
      "state": citys_states[index].state,
      "city": citys_states[index].city,
      "venues": venue_city_state(num_city_state,citys_states)
      })
      index +=1
  return render_template('pages/venues.html', areas=fetch_venue);
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  find_venue_format = Venue.name.ilike('%{}%'.format(request.form.get('search_term', '')))
  searched_venue = Venue.query.filter(find_venue_format)
  searched_venues = searched_venue.all()
  num_searched_venues = searched_venue.count()
  result  = {
    "data": search(num_searched_venues,searched_venues),
    "count": num_searched_venues
  }
  find_word = request.form.get('search_term', '')
  return render_template('pages/search_venues.html', results=result, search_term = find_word)
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  value = []
  fetched_venue_id = Venue.query.get(venue_id)
  upcoming_show_list= Show.query.join(Artist).filter(Show.venue_id == venue_id).filter(
    Show.start_time > datetime.now())
  upcoming_shows_lists = upcoming_show_list.all()
  num_upcoming_show_list = upcoming_show_list.count()

  value_upcoming_shows = shows_venue_artist(num_upcoming_show_list,upcoming_shows_lists)
  past_show_list = Show.query.join(Artist).filter(Show.venue_id == venue_id).filter(
    Show.start_time < datetime.now())
  past_shows_lists = past_show_list.all()
  num_past_show_list = past_show_list.count()
  value_past_shows = shows_venue_artist(num_past_show_list,past_shows_lists)
  value = {
        'id': fetched_venue_id.id,
        'name': fetched_venue_id.name,
        'genres': fetched_venue_id.genres,
        'address': fetched_venue_id.address,
        'website_link': fetched_venue_id.website_link,
        'facebook_link': fetched_venue_id.facebook_link,
        'seeking_talent': fetched_venue_id.looking_talent,
        'seeking_description': fetched_venue_id.seeking_description,
        'image_link': fetched_venue_id.image_link,
        'city': fetched_venue_id.city,
        'state': fetched_venue_id.state,
        'phone': fetched_venue_id.phone,
        'past_shows': value_past_shows,
        'upcoming_shows': value_upcoming_shows,
        'past_shows_count': num_past_show_list,
        'upcoming_shows_count': num_upcoming_show_list
    }
  return render_template('pages/show_venue.html', venue=value)

#  ...............................................................
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # TODO: on unsuccessful db insert, flash an error instead.
  # on successful db insert, flash success
  venue_forms = request.form
  try:
    venue_artist_form(venue_forms)
    flash('Venue ' + 
             request.form['name'] + 
              ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Error, Venue ' + 
             request.form['name'] + 
              ' cannot be listed.')
    print(sys.exc_info())

  finally:
    db.session.close()

  return render_template('pages/home.html')
  
@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None
  delete_venue = Venue.query.get(venue_id)
  delete_show = Show.query.filter(Venue.id == venue_id)
  delete_shows = delete_show.all()
  num_delete_shows = delete_show.count()
  try:
    deletes(num_delete_shows,delete_shows,delete_venue)
    flash('Venue ' 
             + venue_id + 
           ' is deleted from both Venue and Show list')
  except:
    db.session.rollback()
    flash('Error. Venue ' 
            + venue_id + 
              ' cannot be deleted.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect('/venues')

@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  delete_artist = Artist.query.get(artist_id)
  delete_show = Show.query.filter(Artist.id == artist_id)
  delete_shows = delete_show.all()
  num_delete_shows = delete_show.count()
  try:
    deletes(num_delete_shows,delete_shows,delete_artist)
    flash('Artist ' + 
            artist_id + 
             ' is deleted from both Artist and Show list.')
  except:
    db.session.rollback()
    flash('Error. Artist ' + 
             artist_id + 
              ' cannot be deleted.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect('/artists')

#  ................................................................
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  fetch_artists = Artist.query.all()
  return render_template('pages/artists.html', artists=fetch_artists)
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  find_artist_format = Artist.name.ilike('%{}%'.format(request.form.get('search_term','')))
  searched_artist = Artist.query.filter(find_artist_format)
  searched_artists = searched_artist.all()
  num_searched_artists = searched_artist.count()
  result  = {
    "count": num_searched_artists,
    "data": search(num_searched_artists,searched_artists,flag=1)
  }
  find_word = request.form.get('search_term', '')
  return render_template('pages/search_artists.html', results=result, search_term = find_word)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  value = []
  fetched_artist_id = Artist.query.get(artist_id)
  upcoming_show_list= Show.query.join(Venue).filter(Show.artist_id == artist_id).filter(
    Show.start_time > datetime.now())
  upcoming_shows_lists = upcoming_show_list.all()
  num_upcoming_show_list = upcoming_show_list.count()

  value_upcoming_shows = shows_venue_artist(num_upcoming_show_list,upcoming_shows_lists,flag=1)
  past_show_list = Show.query.join(Venue).filter(Show.artist_id == artist_id).filter(
    Show.start_time < datetime.now())
  past_shows_lists = past_show_list.all()
  num_past_show_list = past_show_list.count()
  value_past_shows = shows_venue_artist(num_past_show_list,past_shows_lists,flag=1)
  value = {
        'id': fetched_artist_id.id,
        'name': fetched_artist_id.name,
        'genres': fetched_artist_id.genres,
        'website_link': fetched_artist_id.website_link,
        'facebook_link': fetched_artist_id.facebook_link,
        'seeking_venue': fetched_artist_id.looking_venues,
        'seeking_description': fetched_artist_id.seeking_description,
        'image_link': fetched_artist_id.image_link,
        'city': fetched_artist_id.city,
        'state': fetched_artist_id.state,
        'phone': fetched_artist_id.phone,
        'past_shows': value_past_shows,
        'upcoming_shows': value_upcoming_shows,
        'past_shows_count': num_past_show_list,
        'upcoming_shows_count': num_upcoming_show_list
    }
  return render_template('pages/show_artist.html', artist=value)

#..................................................................
#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
# TODO: populate form with fields from artist with ID <artist_id>
  artist_edit = Artist.query.get(artist_id)
  form = ArtistForm(    name=artist_edit.name, 
                        city=artist_edit.city, 
                        phone=artist_edit.phone, 
                        image_link=artist_edit.image_link, 
                        genres=artist_edit.genres,
                        facebook_link=artist_edit.facebook_link, 
                        website_link=artist_edit.website_link, 
                        state=artist_edit.state, 
                        seeking_venue=artist_edit.looking_venues, 
                        seeking_description=artist_edit.seeking_description)
  return render_template('forms/edit_artist.html', form=form, artist=artist_edit)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  edit_artist_form = request.form
  edit_artist = Artist.query.get(artist_id)
  try:
   edit_artist_venue(edit_artist_form,edit_artist)
   flash('Artist ' + 
           request.form['name'] + 
            ' is successfully updated.')
  except:
    db.session.rollback()
    flash('Error, Unable to update Artist ' 
              + request.form['name'] + 
                 '.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
# TODO: populate form with values from venue with ID <venue_id>
  venue_edit = Venue.query.get(venue_id)
  form = VenueForm(       name=venue_edit.name, 
                          city=venue_edit.city, 
                          state=venue_edit.state, 
                          image_link=venue_edit.image_link, 
                          genres=venue_edit.genres,
                          facebook_link=venue_edit.facebook_link, 
                          website_link=venue_edit.website_link, 
                          address = venue_edit.address,
                          phone=venue_edit.phone, 
                          seeking_talent=venue_edit.looking_talent, 
                          seeking_description=venue_edit.seeking_description)

  return render_template('forms/edit_venue.html', form=form, venue=venue_edit)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  edit_venue_form = request.form
  edit_venue = Venue.query.get(venue_id)
  try:
    edit_artist_venue(edit_venue_form,edit_venue,flag=1)
    flash('Venue ' + 
           request.form['name'] + 
           ' is successfully updated.')
  except:
    db.session.rollback()
    flash('Error, Unable to update Venue ' 
           + request.form['name'] + '.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))


#  ................................................................
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # TODO: on unsuccessful db insert, flash an error instead.
  # on successful db insert, flash success
  
  artist_forms = request.form
  try:
    venue_artist_form(artist_forms,flag=1)
    flash('Artist ' + 
               request.form['name'] + 
                ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Error, Artist ' + 
               request.form['name'] + 
                 ' cannot be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

#  ................................................................
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  value  = []
  fetched_show = Show.query.join(Artist).join(Venue)
  fetched_shows = fetched_show.all()
  num_fetched_show = fetched_show.count()
  index = 0 
  while index < num_fetched_show:
    value.append({
      "venue_id": fetched_shows[index].venue_id,
      "venue_name": fetched_shows[index].venues.name,
      "artist_id": fetched_shows[index].artist_id,
      "artist_name": fetched_shows[index].artists.name,
      "artist_image_link": fetched_shows[index].artists.image_link,
      "start_time": fetched_shows[index].start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
    index +=1
  return render_template('pages/shows.html', shows = value)
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
# called to create new shows in the db, upon submitting new show listing form
# TODO: insert form data as a new Show record in the db, instead
# TODO: on unsuccessful db insert, flash an error instead.
# on successful db insert, flash success
  fetch_show = request.form
  try:
    show = Show( venue_id = fetch_show['venue_id'], 
                  artist_id = fetch_show['artist_id'], 
                  start_time = fetch_show['start_time'])

    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('Error, Show Cannot be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
