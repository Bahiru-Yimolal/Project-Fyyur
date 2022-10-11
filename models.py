from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

  #----------------------------------------------------------------------------#
  # Models.
  #----------------------------------------------------------------------------#

class Venue(db.Model):
      __tablename__ = 'venue'

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String)
      city = db.Column(db.String(120))
      state = db.Column(db.String(120))
      address = db.Column(db.String(120))
      phone = db.Column(db.String(120))
      genres = db.Column(db.ARRAY(db.String()))
      image_link = db.Column(db.String(500))
      facebook_link = db.Column(db.String(120))
      website_link =  db.Column(db.String(120))
      looking_talent = db.Column(db.String(5))
      seeking_description = db.Column(db.String(250))
      shows = db.relationship('Show', backref=db.backref('venues', lazy=True))


      def __repr__(self):

       return f'<venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.geners} {self.image_link} {self.facebook_link} {self.website_link} {self.looking_talent} {self.seeking_description}>'

      # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
      __tablename__ = 'artist'

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String)
      city = db.Column(db.String(120))
      state = db.Column(db.String(120))
      phone = db.Column(db.String(120))
      genres = db.Column(db.ARRAY(db.String()))
      image_link = db.Column(db.String(500))
      facebook_link = db.Column(db.String(120))
      website_link =  db.Column(db.String(120))
      looking_venues = db.Column(db.String(5))
      seeking_description = db.Column(db.String(250))
      shows = db.relationship('Show', backref=db.backref('artists', lazy=True))


      def __repr__(self):
       return f'<artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.website_link} {self.looking_venues} {self.seeking_description}>'
      
      # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)



  # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
