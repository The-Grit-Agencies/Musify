import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'youdr_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID') or '5efe8b646c624df3804e02c19f759b31'
    
  
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') or 'b2673fad7c384ddf80d2f5822e8c3dc7'