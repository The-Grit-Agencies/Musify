import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://default:COelESN7m1vV@ep-delicate-credit-a2nkv9v5.eu-central-1.aws.neon.tech:5432/verceldb?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/tmp/uploads'

    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID') or 'your_spotify_client_id'
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') or 'your_spotify_client_secret'
    GOOGLE_DRIVE_CREDENTIALS_JSON = os.environ.get('GOOGLE_DRIVE_CREDENTIALS_JSON') or 'client_secrets.json'
