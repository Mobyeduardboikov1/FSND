#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_wtf import CsrfProtect

csrf = CsrfProtect()
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf.init_app(app)

from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#------------------------------------------------------------------#
# Validation output
#------------------------------------------------------------------#

def render_validation_output(errors):
  for key in errors:
      flash("Validation errors: " + errors[key][0])

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = Venue.query.with_entities(func.count(Venue.id), Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  data_formatted = []
  for place in data:
    venues = Venue.query.filter_by(city=place.city, state=place.state).all()
    venues_formatted = []
    for venue in venues:
      venues_formatted.append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': Show.query.filter_by(venue_id=venue.id).count()
      })
    data_formatted.append({
      'city': place.city,
      'state': place.state,
      'venues': venues_formatted
    })

  return render_template('pages/venues.html', areas=data_formatted)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  data = []
  for venue in Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all():
    print(venue)
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(venue.shows),
    })

  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  data = { 
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genres or [],
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link   
    }
  #upcoming shows
  for show in Show.query.join(Artist).filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all():
    upcoming_shows.append({
      'artist_id': show.artist.id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.start_time)
    })
  data['upcoming_shows'] = upcoming_shows
  #past shows
  for show in Show.query.join(Artist).filter(Show.venue_id == venue_id, Show.start_time <= datetime.now()).all():
    past_shows.append({
      'artist_id': show.artist.id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.start_time)
    })
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  vf = VenueForm()
  if (vf.validate_on_submit()):
    try:    
        data = request.form
        new_venue = Venue(
          name=data['name'],
          city=data['city'],
          state=data['state'],
          address=data['address'],
          genres=data.getlist('genres'),
          phone=data['phone'],
          website=data['website'],
          image_link=data['image_link'],
          facebook_link=data['facebook_link'],
          seeking_description=data['seeking_description'],
          seeking_talent=True if 'seeking_talent' in request.form else False,
        )
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + data['name'] + ' could not be listed.'+'Exception: '+e)
  else:
    render_validation_output(vf.errors)
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  for artist in Artist.query.all():
    data.append({
      'id': artist.id,
      'name': artist.name
    })
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  data = []
  for artist in Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all():
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(artist.shows),
    })

  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  data = { 
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres or [],
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link   
    }
  #upcoming shows
  for show in Show.query.join(Venue).filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all():
    upcoming_shows.append({
      'venue_id': show.venue.id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': str(show.start_time)
    })
  data['upcoming_shows'] = upcoming_shows
  #past shows
  for show in Show.query.join(Venue).filter(Show.artist_id == artist_id, Show.start_time <= datetime.now()).all():
    past_shows.append({
      'venue_id': show.venue.id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': str(show.start_time)
    })
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(
    name=artist.name,
    genres=artist.genres,
    city=artist.city,
    state=artist.state,
    phone=artist.phone,
    website=artist.website,
    image_link=artist.image_link,
    facebook_link=artist.facebook_link,
    seeking_description=artist.seeking_description,
    seeking_venue=artist.seeking_venue
  )

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  edited_artist = Artist.query.get(artist_id)
  if (form.validate_on_submit()):
    try:        
      data = request.form     

      edited_artist.name=data['name']
      edited_artist.city=data['city']
      edited_artist.state=data['state']
      edited_artist.genres=data.getlist('genres')
      edited_artist.phone=data['phone']
      edited_artist.website=data['website']
      edited_artist.image_link=data['image_link']
      edited_artist.facebook_link=data['facebook_link']
      edited_artist.seeking_description=data['seeking_description']
      edited_artist.seeking_venue=True if 'seeking_venue' in data else False
      db.session.commit()
      flash('Artist ' + data['name'] + ' was successfully updated!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Artist ' + data['name'] + ' could not be edited.'+'Exception: '+str(e))
  else:
    render_validation_output(form.errors)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id): 
  venue = Venue.query.get(venue_id)
  form = VenueForm(
    name=venue.name,
    genres=venue.genres,
    city=venue.city,
    state=venue.state,
    address=venue.address,
    phone=venue.phone,
    website=venue.website,
    image_link=venue.image_link,
    facebook_link=venue.facebook_link,
    seeking_description=venue.seeking_description,
    seeking_talent=venue.seeking_talent
  )
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_edit(venue_id):
  form = VenueForm()
  edited_venue = Venue.query.get(venue_id)
  if (form.validate_on_submit()):
    try:        
      data = request.form     

      edited_venue.name=data['name']
      edited_venue.city=data['city']
      edited_venue.state=data['state']
      edited_venue.address=data['address']
      edited_venue.genres=data.getlist('genres')
      edited_venue.phone=data['phone']
      edited_venue.website=data['website']
      edited_venue.image_link=data['image_link']
      edited_venue.facebook_link=data['facebook_link']
      edited_venue.seeking_description=data['seeking_description']
      edited_venue.seeking_talent=True if 'seeking_talent' in data else False
      db.session.commit()
      flash('Venue ' + data['name'] + ' was successfully updated!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + data['name'] + ' could not be edited.'+'Exception: '+str(e))
  else:
    render_validation_output(form.errors)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  af = ArtistForm()
  if (af.validate_on_submit()):
    try:
      data = request.form
      new_artist = Artist(
        name=data['name'],
        city=data['city'],
        state=data['state'],
        phone=data['phone'],
        genres=data.getlist('genres'),
        image_link=data['image_link'],
        facebook_link=data['facebook_link'],
        website=data['website'],
        seeking_description=data['seeking_description'],
        seeking_venue=True if 'seeking_venue' in request.form else False,
      )
      db.session.add(new_artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Artist ' + data['name'] + ' could not be listed.'+'Exception: '+e)
  else:
    render_validation_output(af.errors)
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  for show in Show.query.join(Artist).join(Venue).all():
    data.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  try:
    data = request.form
    new_show = Show(
      artist_id=data['artist_id'],
      venue_id=data['venue_id'],
      start_time=data['start_time']
    )
    db.session.add(new_show)
    db.session.commit()
    # on successful db insert, flash success
    flash('New show was successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. New show could not be listed.'+'Exception: '+e)
  finally:
    return render_template('pages/home.html')

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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
