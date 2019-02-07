# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:02:32 2018

@author: Ariclenes Silva
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 17:21:56 2018

@author: Ariclenes Silva
"""
import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, session as session2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Albums, Playlists, Users, Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from back_end_spotify import spotify_back_end

Base = declarative_base()

class Albums(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    album_id = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    release_date = Column(String(250), nullable=False)
    total_track = Column(Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {     
            'total_track': self.total_track,   
            'release_date': self.release_date,   
            'album_id': self.album_id,   
            'name': self.name,
            'id': self.id,
        }

class Playlists(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    list_songs = Column(String(250), nullable=True)
 #   user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    password = Column(String(250))
    album_id = Column(Integer, ForeignKey('album.id'))
    list_albums = relationship("Albums")
    playlist_id = Column(Integer, ForeignKey('playlist.id'))
    list_playlists = relationship("Playlists") 

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'username': self.username,
            'id': self.id,
            'password': self.password,
        }

app = Flask(__name__)   
engine = create_engine('sqlite:///music_library3.db')

Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

#session = DBSession()


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


           
@app.route('/PUT/playlists/{id}', methods=['GET', 'POST'])
def album_playlist_id():
    session = DBSession()
    if request.method == 'POST':
        if session.query(Albums).filter_by(id=int(request.form['delete_albumid'])).count() and session2['username']:
            useruser=session.query(Albums).filter_by(id=int(request.form['delete_albumid'])).first()
            useruser2=session.query(Users).filter_by(username=session2['username']).first()
            
            user1 = Users(username=useruser2.username,password=useruser2.password,album_id=useruser.id)
            session.add(user1)
            session.commit()
            return render_template('album_playlist_id.html')
        else:
            return """
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Untitled Document</title>
            	
            	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            </head>
            
            <body>
            	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
            	
            	<div class="alert alert-success" role="alert" style="top: 35%;width: 70%;left: 10%;position: absolute">
              <h4 class="alert-heading">Wrong!!</h4>
              <p>You inserted wrong information</p>
              <hr>
              <p class="mb-0"></p>
            </div>
            	
            	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            </body>
            </html> 
            """

    else:
        return """
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Untitled Document</title>
        	
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        
        <body>
        	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
        	<div style="top: 5%;left: 42%;position: absolute">Insert the album ID to insert in your playlist</div>
        	
        <form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
        	  <div class="form-group">
        		<label for="exampleInputEmail1">Album ID</label>
        		<input type="text" name="delete_albumid" class="form-control" placeholder="Enter the album ID">
        	  </div>
              <input class="btn btn-primary" type="submit" value="Submit">
        </form>
        	
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        
@app.route('/DELETE/albums/{id}', methods=['GET', 'POST'])
def delete_album_id():
    session = DBSession()
    if request.method == 'POST':
        if session.query(Albums).filter_by(id=int(request.form['delete_albumid'])).count():
            useruser=session.query(Albums).filter_by(id=int(request.form['delete_albumid'])).first()
            session.delete(useruser)
            session.commit()
            return render_template('delete_album_id.html')
        else:
            return """
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Untitled Document</title>
            	
            	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            </head>
            
            <body>
            	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
            	
            	<div class="alert alert-success" role="alert" style="top: 35%;width: 70%;left: 10%;position: absolute">
              <h4 class="alert-heading">Wrong!!</h4>
              <p>You inserted wrong information</p>
              <hr>
              <p class="mb-0"></p>
            </div>
            	
            	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            </body>
            </html> 
            """

    else:
        return """
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Untitled Document</title>
        	
        	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        
        <body>
        	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
        	<div style="top: 5%;left: 42%;position: absolute">Insert the album ID to delete</div>
        	
        	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
        	  <div class="form-group">
        		<label for="exampleInputEmail1">Album ID</label>
        		<input type="text" name="delete_albumid" class="form-control" placeholder="Enter the album ID">
        	  </div>
              <input class="btn btn-primary" type="submit" value="Delete Album">
        	</form>
        	
        	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html>
        """


@app.route('/DELETE/users/{id}', methods=['GET', 'POST'])
def delete_user_id():
    session = DBSession()
    if request.method == 'POST':
        if session.query(Users).filter_by(username=request.form['delete_users_username'],password=request.form['delete_users_password']).count() and session2['username']==request.form['delete_users_username']:
            session2.pop('username', None)
            useruser=session.query(Users).filter_by(username=request.form['delete_users_username'],password=request.form['delete_users_password']).first()
            session.delete(useruser)
            session.commit()
            return render_template('delete_user_id.html')
        else:
            return """
            <html>
            <head>
            <meta charset="utf-8">
            <title>Untitled Document</title>
            	
            	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            </head>
            
            <body>
            	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
            	
            	<div class="alert alert-success" role="alert" style="top: 35%;width: 70%;left: 10%;position: absolute">
              <h4 class="alert-heading">Wrong!!</h4>
              <p>You can not delete because the account does not exist or you are not allowed</p>
              <hr>
              <p class="mb-0"></p>
            </div>
            	
            	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            </body>
            </html> 
            """

    else:
        return """
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Untitled Document</title>
        	
        	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        
        <body>
        	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
        	<div style="top: 5%;left: 42%;position: absolute">Insert your informations to delete your account</div>
        	<div  style="top: 15%;left: 30%;position: absolute"> Please, your password should have at least one character and one number</div>
        	
        	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
        	  <div class="form-group">
        		<label for="exampleInputEmail1">Username</label>
        		<input type="text" name="delete_users_username" class="form-control" placeholder="Enter email or username">
        		<small id="emailHelp" class="form-text text-muted">We'll never share your username/email with anyone else.</small>
        	  </div>
        	  <div class="form-group">
        		<label for="exampleInputPassword1">Password</label>
        		<input type="password" name="delete_users_password" class="form-control" placeholder="Password">
        	  </div>
              <input class="btn btn-primary" type="submit" value="Submit">
        	</form>
        	
        	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html>
        """

@app.route('/DELETE/playlists/{id}', methods=['GET', 'POST'])
def delete_playlist_id():
    session = DBSession()
    if request.method == 'POST':
        if session.query(Playlists).filter_by(id=request.form['delete_playlistsid']).count():
            useruser=session.query(Playlists).filter_by(id=request.form['delete_playlistsid']).first()
            session.delete(useruser)
            session.commit()
            return render_template('delete_playlist_id.html')
        else:
            return """
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Untitled Document</title>
            	
            	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            </head>
            
            <body>
            	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
            	
            	<div class="alert alert-success" role="alert" style="top: 35%;width: 70%;left: 10%;position: absolute">
              <h4 class="alert-heading">Wrong!!</h4>
              <p>You inserted wrong information</p>
              <hr>
              <p class="mb-0"></p>
            </div>
            	
            	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            </body>
            </html> 
            """

    else:
        return """
        <!doctype html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Untitled Document</title>
        
        	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        
        <body>
        	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
        	<div style="top: 5%;left: 42%;position: absolute">Insert the playlist ID to delete</div>
        
        	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
        	  <div class="form-group">
        		<label for="exampleInputEmail1">Playlist ID</label>
        		<input type="text" name="delete_playlistsid" class="form-control" placeholder="Enter the playlist ID">
        	  </div>
        	  <input class="btn btn-primary" type="submit" value="Submit">
        	</form>
        
        	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        
@app.route('/', methods=['GET', 'POST'])
def login():
    session = DBSession()
    if 'username' in session2:
        return render_template('home.html', username=session2['username'], login_logout="Logout")
    else:
        if request.method == 'POST':
            user_check=session.query(Users).filter_by(username=request.form['username']).first()
            if user_check and request.form['password']==user_check.password:
                session2['username'] = request.form['username']
            else:
                return """
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Untitled Document</title>
            	
            	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            </head>
            
            <body>
            	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
            	
            	<div class="alert alert-success" role="alert" style="top: 35%;width: 70%;left: 10%;position: absolute">
              <h4 class="alert-heading">Wrong!!</h4>
              <p>You inserted wrong information</p>
              <hr>
              <p class="mb-0"></p>
            </div>
            	
            	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            </body>
            </html> 
            """
            return render_template('home.html', username=user_check.username, login_logout="Logout")
          #  return redirect(url_for('home'))
        
        return render_template('login_welcome.html')

@app.route('/home')
def home():
    return render_template('home.html', login_logout="Login")

@app.route('/POST/users', methods=['GET', 'POST'])
def post_users():
    session = DBSession()
    if request.method == 'POST':
        un = str(request.form['post_users_username'])
        pd = str(request.form['post_users_password'])
        
        user1 = Users(username=un,password=pd)
        session.add(user1)
        session.commit()

        return render_template('added_user.html')
    else:
        return render_template('post_users.html')
    
@app.route('/POST/playlists', methods=['GET', 'POST'])
def post_playlists():
    session = DBSession()
    if request.method == 'POST':
        un = str(request.form['delete_playlistsid'])
        
        user1 = Playlists(name=un)
        session.add(user1)
        session.commit()

        return """
        <html>
        <head>
        <meta charset="utf-8">
        <title>Untitled Document</title>
        	
        	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        </head>
        
        <body>
        	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
        	
        	<div class="alert alert-success" role="alert" style="top: 35%;width: 70%;left: 10%;position: absolute">
          <h4 class="alert-heading">Well Done!!</h4>
          <p>Playlist created</p>
          <hr>
          <p class="mb-0"></p>
        </div>
        	
        	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        </body>
        </html> 
        """
    else:
        return render_template('post_playlists.html')

@app.route('/GET/playlists')
def get_playlists():
    session = DBSession()
    user_check=session.query(Playlists).order_by(Playlists.id)
    return render_template('get_playlists.html', album_list=user_check)

@app.route('/GET/playlists/{id}', methods=['GET', 'POST'])
def get_playlists_id():
    session = DBSession()
    if request.method == 'POST':
        user_check=session.query(Playlists).order_by(Playlists.id)
        print(request.form['find_playlistid'])
        return render_template('get_playlists_id.html', album_list=user_check, album_id=int(request.form['find_playlistid']))
    else:
        pass

    return """
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Untitled Document</title>
    	
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    
    <body>
    	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
    	<div style="top: 5%;left: 42%;position: absolute">Insert the Playlist ID to find the Playlist</div>
    	
    	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
    	  <div class="form-group">
    		<label for="exampleInputEmail1">Album ID</label>
    		<input type="text" name="find_playlistid" class="form-control" placeholder="Enter the playlist ID">
    	  </div>
          <input class="btn btn-primary" type="submit" value="Submit">
    	</form>
    	
    	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
    """

@app.route('/GET/users')
def get_users():
    session = DBSession()
    user_check=session.query(Users).order_by(Users.id)
    session.close()
    return render_template('get_users.html', album_list=user_check)


@app.route('/GET/users/{id}', methods=['GET', 'POST'])
def get_users_id():
    session = DBSession()
    if request.method == 'POST':
        user_check=session.query(Users).order_by(Users.id)
        user_check2=session.query(Albums).order_by(Albums.id)
        user_check3=session.query(Playlists).order_by(Playlists.id)
        return render_template('get_users_id.html', album_list=user_check, album_list2=user_check2, album_list3=user_check3,album_id=int(request.form['find_userid']))
    else:
        pass

    return """
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Untitled Document</title>
    	
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    
    <body>
    	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
    	<div style="top: 5%;left: 42%;position: absolute">Insert the user ID to find the user</div>
    	
    	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
    	  <div class="form-group">
    		<label for="exampleInputEmail1">User ID</label>
    		<input type="text" name="find_userid" class="form-control" placeholder="Enter the user ID">
    	  </div>
          <input class="btn btn-primary" type="submit" value="Submit">
    	</form>
    	
    	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
    """

@app.route('/GET/users/{id}/albums', methods=['GET', 'POST'])
def get_users_id_album():
    session = DBSession()
    if request.method == 'POST':
        user_check=session.query(Users).order_by(Users.id)
        user_check2=session.query(Albums).order_by(Albums.id)
        user_check3=session.query(Playlists).order_by(Playlists.id)
        return render_template('get_users_id_album.html', album_list=user_check, album_list2=user_check2, album_list3=user_check3,album_id=int(request.form['find_userid']))
    else:
        pass

    return """
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Untitled Document</title>
    	
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    
    <body>
    	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
    	<div style="top: 5%;left: 42%;position: absolute">Insert the user ID to find the user</div>
    	
    	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
    	  <div class="form-group">
    		<label for="exampleInputEmail1">User ID</label>
    		<input type="text" name="find_userid" class="form-control" placeholder="Enter the user ID">
    	  </div>
          <input class="btn btn-primary" type="submit" value="Submit">
    	</form>
    	
    	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
    """

@app.route('/GET/users/{id}/playlists', methods=['GET', 'POST'])
def get_users_id_playlists():
    session = DBSession()
    if request.method == 'POST':
        user_check=session.query(Users).order_by(Users.id)
        user_check2=session.query(Albums).order_by(Albums.id)
        user_check3=session.query(Playlists).order_by(Playlists.id)
        return render_template('get_users_id_playlists.html', album_list=user_check, album_list2=user_check2, album_list3=user_check3,album_id=int(request.form['find_userid']))
    else:
        pass

    return """
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Untitled Document</title>
    	
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    
    <body>
    	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
    	<div style="top: 5%;left: 42%;position: absolute">Insert the user ID to find the user</div>
    	
    	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
    	  <div class="form-group">
    		<label for="exampleInputEmail1">User ID</label>
    		<input type="text" name="find_userid" class="form-control" placeholder="Enter the user ID">
    	  </div>
          <input class="btn btn-primary" type="submit" value="Submit">
    	</form>
    	
    	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    
@app.route('/GET/albums')
def get_album():
    session = DBSession()
    user_check=session.query(Albums).order_by(Albums.id)
    return render_template('get_albums.html', album_list=user_check)

@app.route('/GET/albums/{id}', methods=['GET', 'POST'])
def get_album_id():
    session = DBSession()
    if request.method == 'POST':
        user_check=session.query(Albums).order_by(Albums.id)
        print(request.form['find_albumid'])
        return render_template('get_album_id.html', album_list=user_check, album_id=int(request.form['find_albumid']))
    else:
        pass

    return """
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>Untitled Document</title>
    	
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    
    <body>
    	<div><a class="btn btn-primary" href="/home" style="top: 5%;left: 2%;position: absolute">Go back to HOMEPAGE</a></div>
    	<div style="top: 5%;left: 42%;position: absolute">Insert the album ID to find the album</div>
    	
    	<form method='POST' enctype='multipart/form-data' style="top: 35%;width: 70%;left: 10%;position: absolute">
    	  <div class="form-group">
    		<label for="exampleInputEmail1">Album ID</label>
    		<input type="text" name="find_albumid" class="form-control" placeholder="Enter the album ID">
    	  </div>
          <input class="btn btn-primary" type="submit" value="Submit">
    	</form>
    	
    	<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
    </html>
    """

@app.route('/POST/albums', methods=['GET', 'POST'])
def post_album():
    if request.method == 'POST':
        p_a = request.form['post_albums']
        mc=str(p_a)
        album_name = mc.split()
        album_name_final=""
        for i in album_name:
        	album_name_final+=i
        	album_name_final+="+"
        
        album_name_final=album_name_final[:-1]
        
        sbe=spotify_back_end(album_name_final)
        final_result=sbe.start()
        return render_template('post_album2.html', final_result_spotify=final_result)
    else:
        return render_template('post_album.html')
    

@app.route('/logout')
def logout():
    session2.pop('username', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    #return render_template('page_not_found.html'), 404
    return "page_not_found"

@app.errorhandler(500)
def page_overload(e):
    return str(e)

with app.test_request_context():
    print(url_for('login'))
    print(url_for('home'))
    print(url_for('post_users'))
    print(url_for('get_playlists'))
    print(url_for('get_users'))
    print(url_for('get_users_id'))
    print(url_for('get_users_id_album'))
    print(url_for('get_users_id_playlists'))
    print(url_for('get_album'))
    print(url_for('get_album_id'))
    print(url_for('post_album'))
    print(url_for('logout'))


    
if __name__ == '__main__':
    app.debug = True
    app.run()