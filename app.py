#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate=Migrate(app,db)
# TODO: connect to a local postgresql database


from model import Shows
from model import Venue
from model import Artist


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format,locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    todayDate=datetime.now()
    today_Date= todayDate.strftime("%Y-%M-%D %H:%M")
    data=[]
    city_state=set() #to make unique entery of city&state
    venues=Venue.query.all()
    for venue in venues:
        city_state.add((venue.city,venue.state))
    for city in city_state:
        venueArr=[]
        for venue in venues:
            if (venue.city,venue.state)==city:
                no_of_upcoming_shows=0
                ven_Id=venue.id
                venueshows=Shows.query.filter_by(venue_id=ven_Id).all()
                for show in venueshows:
                    showdate=show.start_time
                    if showdate >today_Date:
                        no_of_upcoming_shows=+1
                    else:
                        continue
                venue_Entry={"id":ven_Id,"name":venue.name,"num_upcoming_shows":  no_of_upcoming_shows}
                venueArr.append(venue_Entry)
            else:
                continue;
        dataEntry={"city":city[0],"state":city[1],"venues":venueArr}
        data.append(dataEntry)
    return render_template('pages/venues.html', areas=data)
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # implement search on artists with partial string search. Ensure it is case-insensitive.
    sear=request.form.get('search_term','')
    data=Venue.query.filter(Venue.name.ilike(f'%{sear}%')).all()
    count=Venue.query.filter(Venue.name.ilike(f'%{sear}%')).count()
    response={'count':count,'data':data}
    return render_template('pages/search_venues.html', results=response, search_term=sear)
 
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    upcoming_shows=[]
    past_shows=[]
    data_q=Venue.query.get(venue_id)
    if not data_q :
            return render_template('errors/404.html')
    data={"id":data_q.id,"name":data_q.name,"genres":data_q.genres,"address":data_q.address,"city":data_q.city,
         "state":data_q.state,"phone":data_q.phone,"website":data_q.website,"facebook_link":data_q.facebook_link,"image_link":data_q.image_link}
    
    #shows=Shows.query.filter_by(venue_id=venue_id).all()
    shows=db.session.query(Shows).join(Venue,Shows.venue_id==venue_id).all()
    todayDate=datetime.now()
    today_Date= todayDate.strftime("%Y-%M-%D %H:%M")
    for show in shows:
            id=show.artist_id
            Entry=Artist.query.get(id)
            showEntry={"artist_id":show.artist_id,"artist_name":Entry.name,"artist_image_link":Entry.image_link,"start_time":show.start_time}
            showdate=show.start_time
            if showdate >=today_Date:
                upcoming_shows.append(showEntry)
            else:
                past_shows.append(showEntry)
    data['past_shows']=past_shows
    data['upcoming_shows']=upcoming_shows
    data['past_shows_count']= len(past_shows)
    data['upcoming_shows_count']= len(upcoming_shows)
    data1= list(filter(lambda d: d['id'] == venue_id, [data]))[0]
    return render_template('pages/show_venue.html', venue=data1)  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
        nam=request.form.get('name')
        cit=request.form.get('city')
        stat=request.form.get('state')
        phon=request.form.get('phone')
        add=request.form.get('address')
        imag=request.form.get('image_link')
        genr=request.form.getlist('genres')
        facebook=request.form.get('facebook_link')
        web=request.form.get('website')
        venue=Venue(name=nam,city=cit,state=stat,address=add,phone=phon,genres=genr,image_link=imag,facebook_link=facebook,website=web) 
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    finally:
        db.session.close()
        return render_template('pages/home.html')
    
@app.route('/venues/<venue_id>/dele', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()    
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify({ 'success': True })

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
 
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.order_by(Artist.id)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # implement search on artists with partial string search. Ensure it is case-insensitive.
    sear=request.form.get('search_term','')
    data=Artist.query.filter(Artist.name.ilike(f'%{sear}%')).all()
    count=Artist.query.filter(Artist.name.ilike(f'%{sear}%')).count()
    response={'count':count,'data':data}
    return render_template('pages/search_artists.html', results=response, search_term=sear)
@app.route('/all')
def all():
    data1=Artist.query.all()
    data2=Venue.query.all()
    return render_template('pages/find_all.html', artists=data1,venues=data2)
    
@app.route('/findall', methods=['POST'])
def find_all():
    sear=request.form.get('search_term','')
    lis=sear.split(", ")
    count1=0
    count2=0
    da=[]
    d2=[]
    data1=Artist.query.filter(Artist.city.ilike(f'%{lis[0]}%')).all()
    for data in data1:
        id=data.id
        elem=data.query.get(id)
        if lis[1]==elem.state:
            count1=count1+1
            da.append(data)
        else:
            continue
    data2=Venue.query.filter(Venue.city.ilike(f'%{lis[0]}%')).all()
    for data in data2:
        id=data.id
        elem=data.query.get(id)
        if lis[1]==elem.state:
            count2=count2+1
            d2.append(data)
        else:
            continue
    count=count1+count2
    response1={'count':count1,'data':da}
    response2={'count':count2,'data':d2}
    response={'count':count}
    return render_template('pages/search_all.html', results=response, results2=response2, results1=response1, search_term=sear)

  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    upcoming_shows=[]
    past_shows=[]
    data_q=Artist.query.get(artist_id)
    if not data_q :
            return render_template('errors/404.html')
    data={"id":data_q.id,"name":data_q.name,"genres":data_q.genres,"city":data_q.city,
         "state":data_q.state,"phone":data_q.phone,"website":data_q.website,"facebook_link":data_q.facebook_link,"image_link":data_q.image_link}
    #shows=Shows.query.filter_by(artist_id=artist_id).all()
    shows=db.session.query(Shows).join(Artist,Shows.artist_id==artist_id).all()
    todayDate=datetime.now()
    today_Date= todayDate.strftime("%Y-%M-%D %H:%M")
    for show in shows:
            id=show.venue_id
            Entry=Venue.query.get(id)
            showEntry={"venue_id":show.venue_id,"venue_name":Entry.name,"venue_image_link":Entry.image_link,"start_time":show.start_time}
            showdate=show.start_time
            if showdate >=today_Date:
                upcoming_shows.append(showEntry)
            else:
                past_shows.append(showEntry)
    data['past_shows']=past_shows
    data['upcoming_shows']=upcoming_shows
    data['past_shows_count']= len(past_shows)
    data['upcoming_shows_count']= len(upcoming_shows)
    data1= list(filter(lambda d: d['id'] == artist_id, [data]))[0]
    return render_template('pages/show_artist.html', artist=data1)  

  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
        form = ArtistForm()
        artist=Artist.query.get(artist_id)
        if not artist:
                return render_template('errors/404.html')
        data={
              "id": artist_id,
              "name": artist.name,
              "genres": artist.genres,
              "city": artist.city,
              "state":  artist.state,
              "phone":  artist.phone,
              "website": artist.website,
              "facebook_link":  artist.facebook_link,
              "image_link": artist.image_link
            }
        return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist=Artist.query.get(artist_id)
        artist.name=request.form.get('name')
        artist.city=request.form.get('city')
        artist.state=request.form.get('state')
        artist.phone=request.form.get('phone')
        artist.image_link=request.form.get('image_link')
        artist.genres=request.form.getlist('genres')
        artist.facebook_link=request.form.get('facebook_link')
        artist.website=request.form.get('website')
        db.session.commit()
        flash('Edit was successfully done!')
    except:
        flash('Edit was unsuccessfully done!')
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))
        

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
        form = VenueForm()
        venue=Venue.query.get(venue_id)
        if not venue:
                return render_template('errors/404.html')
        data={
              "id": venue_id,
              "name": venue.name,
              "genres": venue.genres,
              "address":venue.address,
              "city": venue.city,
              "state":  venue.state,
              "phone":  venue.phone,
              "website": venue.website,
              "facebook_link":  venue.facebook_link,
              "image_link": venue.image_link
            }
        return render_template('forms/edit_venue.html', form=form, venue=data) 
    
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue=Venue.query.get(venue_id)
        venue.name=request.form.get('name')
        venue.city=request.form.get('city')
        venue.state=request.form.get('state')
        venue.phone=request.form.get('phone')
        venue.image_link=request.form.get('image_link')
        venue.genres=request.form.getlist('genres')
        venue.facebook_link=request.form.get('facebook_link')
        venue.website=request.form.get('website')
        venue.address=request.form.get('address')
        db.session.commit()
        flash('Edit was successfully done!')
    except:
        flash('Edit was unsuccessfully done!')
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
         # called upon submitting the new artist listing form
         # TODO: insert form data as a new Venue record in the db, instead
        nam=request.form.get('name')
        cit=request.form.get('city')
        stat=request.form.get('state')
        phon=request.form.get('phone')
        imag=request.form.get('image_link')
        genr=request.form.getlist('genres')
        facebook=request.form.get('facebook_link')
        web=request.form.get('website')
        artist=Artist(name=nam,city=cit,state=stat,phone=phon,genres=genr,image_link=imag,facebook_link=facebook,website=web) 
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    finally:
        db.session.close()
        # TODO: on unsuccessful db insert, flash an error instead.
        return render_template('pages/home.html')
@app.route('/artists/<artist_id>/dele', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        Artist.query.filter_by(id=artist_id).delete()    
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify({ 'success': True })
        
   
    
  

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data=[]
    data1=Shows.query.all()
    for dat in data1:
        venueid=dat.venue_id
        artistid=dat.artist_id
        entry={
            "venue_id":venueid ,
            "venue_name":Venue.query.get(venueid).name,
            "artist_id": artistid,
            "artist_name": Artist.query.get(artistid).name,
            "artist_image_link":Artist.query.get(artistid).image_link ,
            "start_time":dat.start_time
        }
        data.append(entry)
    return render_template('pages/shows.html', shows=data)
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #num_shows should be aggregated based on number of upcoming shows per venue.

 
  

@app.route('/shows/create',methods=['GET'])
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        # called to create new shows in the db, upon submitting new show listing form
        # TODO: insert form data as a new Show record in the db, instead
        # on successful db insert, flash success
        artistId=request.form['artist_id']
        venueId=request.form['venue_id']
        #venuename=Venue.query.get(venueId).name
        #venueimg=Venue.query.get(venueId).image_link
        #artistname=Artist.query.get(artistId).name
        #artistimg=Artist.query.get(artistId).image_link
        #artistimg=Artist.query.get(artistId).image_link
        startDate=request.form['start_time'] 
        show=Shows(venue_id=venueId,artist_id=artistId,start_time=startDate)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
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
