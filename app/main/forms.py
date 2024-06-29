from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class MusicUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    file = FileField('Upload Music', validators=[DataRequired(), FileAllowed(['mp3', 'wav'], 'Audio files only!')])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')

class PlaylistForm(FlaskForm):
    name = StringField('Playlist Name', validators=[DataRequired()])
    cover_image = FileField('Cover Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Create Playlist')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Create Category')

class FavoriteForm(FlaskForm):
    submit = SubmitField('Add to Favorites')

class SmartPlaylistForm(FlaskForm):
    criteria = SelectField('Criteria', choices=[('genre', 'Genre'), ('artist', 'Artist'), ('mood', 'Mood'), ('tempo', 'Tempo')], validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Create Playlist')
