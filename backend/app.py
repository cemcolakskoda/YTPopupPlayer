from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set the path to the current directory and create an SQLite database file
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "videos.db"))

# SQLite database setup
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Video model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

# Create tables
db.create_all()

@app.route('/get_video_urls', methods=['POST'])
def get_video_urls():
    # You can perform any necessary checks or processing here
    # ...

    # Query all video URLs from the database
    video_urls = [video.url for video in Video.query.all()]

    # Return the list of video URLs as a JSON response
    return jsonify({'video_urls': video_urls})

if __name__ == '__main__':
    app.run(debug=True)
