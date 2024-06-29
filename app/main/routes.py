import os
from flask import render_template, redirect, url_for, flash, current_app, send_file, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.main import main
from app.main.forms import MusicUploadForm, PlaylistForm, FavoriteForm
from app.main.models import Music, Playlist, Favorite

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    greeting = "Good night!"  # This can be dynamic based on the time of day
    recent_music = Music.query.order_by(Music.date_posted.desc()).limit(5).all()
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', greeting=greeting, recent_music=recent_music, playlists=playlists, favorites=favorites)
    
@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = MusicUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        music = Music(
            title=form.title.data, 
            artist=form.artist.data, 
            file=filename, 
            user_id=current_user.id
        )

        if form.image.data:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            image_upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            os.makedirs(os.path.dirname(image_upload_path), exist_ok=True)
            image.save(image_upload_path)
            music.image = image_filename

        db.session.add(music)
        db.session.commit()

        flash('Music uploaded successfully.')
        return redirect(url_for('main.dashboard'))
    
    return render_template('upload.html', form=form)

@main.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        playlist = Playlist(name=form.name.data, user_id=current_user.id)
        if form.cover_image.data:
            cover_image = form.cover_image.data
            cover_image_filename = secure_filename(cover_image.filename)
            cover_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cover_image_filename))
            playlist.cover_image = cover_image_filename
        db.session.add(playlist)
        db.session.commit()
        flash('Playlist created successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('create_playlist.html', form=form)

@main.route('/add_favorite/<int:music_id>', methods=['POST'])
@login_required
def add_favorite(music_id):
    form = FavoriteForm()
    if form.validate_on_submit():
        favorite = Favorite(user_id=current_user.id, music_id=music_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Music added to favorites.')
    return redirect(url_for('main.dashboard'))

@main.route('/stream/<int:music_id>')
@login_required
def stream_music(music_id):
    music = Music.query.get_or_404(music_id)
    file_path = os.path.join(os.path.dirname(current_app.root_path), 'uploads', music.file)
    return send_file(file_path)

@main.route('/create_smart_playlist', methods=['GET', 'POST'])
@login_required
def create_smart_playlist():
    form = SmartPlaylistForm()
    if form.validate_on_submit():
        criteria = form.criteria.data
        value = form.value.data
        if criteria == 'genre':
            music_list = Music.query.filter_by(genre=value).all()
        elif criteria == 'artist':
            music_list = Music.query.filter_by(artist=value).all()
        elif criteria == 'mood':
            music_list = Music.query.filter_by(mood=value).all()
        elif criteria == 'tempo':
            music_list = Music.query.filter(Music.tempo >= int(value)).all()

        playlist = Playlist(name=f'{value} {criteria} Playlist', user_id=current_user.id)
        db.session.add(playlist)
        db.session.commit()
        
        for music in music_list:
            playlist_music = PlaylistMusic(playlist_id=playlist.id, music_id=music.id)
            db.session.add(playlist_music)
        
        db.session.commit()
        flash('Smart playlist created successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('create_smart_playlist.html', form=form)

@main.route('/rename_playlist/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def rename_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = RenamePlaylistForm()
    if form.validate_on_submit():
        playlist.name = form.name.data
        db.session.commit()
        flash('Playlist renamed successfully.')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.name.data = playlist.name
    return render_template('rename_playlist.html', form=form)

@main.route('/reorder_playlist/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def reorder_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    # Add logic for reordering songs
    pass

@main.route('/delete_playlist/<int:playlist_id>', methods=['POST'])
@login_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist)
    db.session.commit()
    flash('Playlist deleted successfully.')
    return redirect(url_for('main.dashboard'))

@main.route('/add_track_to_playlist/<int:playlist_id>/<int:music_id>', methods=['POST'])
@login_required
def add_track_to_playlist(playlist_id, music_id):
    playlist_music = PlaylistMusic(playlist_id=playlist_id, music_id=music_id)
    db.session.add(playlist_music)
    db.session.commit()
    flash('Track added to playlist.')
    return redirect(url_for('main.dashboard'))

@main.route('/spotify_login')
def spotify_login():
    spotify_auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": url_for('main.spotify_callback', _external=True),
        "scope": "playlist-read-private"
    }
    url = f"{spotify_auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)

@main.route('/spotify_callback')
def spotify_callback():
    code = request.args.get('code')
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": url_for('main.spotify_callback', _external=True),
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    token_response = requests.post(token_url, data=token_data)
    tokens = token_response.json()
    access_token = tokens['access_token']
    session['spotify_token'] = access_token
    return redirect(url_for('main.dashboard'))

@main.route('/import_spotify_playlists')
@login_required
def import_spotify_playlists():
    headers = {"Authorization": f"Bearer {session['spotify_token']}"}
    playlists_response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    playlists = playlists_response.json()['items']
    for playlist in playlists:
        new_playlist = Playlist(name=playlist['name'], user_id=current_user.id)
        db.session.add(new_playlist)
        db.session.commit()
    flash('Spotify playlists imported successfully.')
    return redirect(url_for('main.dashboard'))

@main.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = PlaylistCategory(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('create_category.html', form=form)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

@main.route('/init-db')
def init_db():
    db.create_all()
    return "Database initialized!"
