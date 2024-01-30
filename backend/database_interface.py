from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class DatabaseInterface:
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(self.app)

        # Define the Video model
        class Video(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            title = self.db.Column(self.db.String(255), nullable=False)
            description = self.db.Column(self.db.String(255))

    def add_video(self, title, description=''):
        with self.app.app_context():
            new_video = self.Video(title=title, description=description)
            self.db.session.add(new_video)
            self.db.session.commit()

    def get_videos(self):
        with self.app.app_context():
            videos = self.Video.query.all()
            return [{'title': video.title, 'description': video.description} for video in videos]
