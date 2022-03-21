from app import db

class Shows(db.Model):
    __tablename__='shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id=db.Column(db.Integer,db.ForeignKey('venues.id'),nullable=False)
    #venue_name=db.Column(db.String,nullable=False)
    #venue_image_link=db.Column(db.String(500),nullable=False)
    artist_id= db.Column(db.Integer,db.ForeignKey('artists.id'),nullable=False)
    #artist_name=db.Column(db.String,nullable=False)
    #artist_image_link=db.Column(db.String(500),nullable=False)
    start_time=db.Column(db.String(),nullable=False)
    venue=db.relationship('Venue',backref='venue',lazy=True)
    artist=db.relationship('Artist',backref='artist',lazy=True)

    
    

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    genres = db.Column("genres",db.ARRAY(db.String()),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120),nullable=True)
    #artist=db.relationship('Artist',secondary=show,backref=db.backref('venues',lazy=True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    genres = db.Column("genres",db.ARRAY(db.String()),nullable=False)
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(120),nullable=False)
    website = db.Column(db.String(120),nullable=True)