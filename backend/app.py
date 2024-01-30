from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# SQLite database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded videos
db_sqlite = SQLAlchemy(app)

# SQLite Video model
class VideoSQLite(db_sqlite.Model):
    id = db_sqlite.Column(db_sqlite.Integer, primary_key=True)
    CategoryId = db_sqlite.Column(db_sqlite.Integer)
    CategoryName = db_sqlite.Column(db_sqlite.String(255))
    model = db_sqlite.Column(db_sqlite.String(255))
    FileId = db_sqlite.Column(db_sqlite.Integer)
    FileName = db_sqlite.Column(db_sqlite.String(255))
    CreatedDate = db_sqlite.Column(db_sqlite.String(255))
    url = db_sqlite.Column(db_sqlite.String(255), nullable=False)

# Create SQLite tables
db_sqlite.create_all()

# Route to add a video to the database
@app.route('/add_video', methods=['POST'])
def add_video():
    # Extract data from the request
    data = request.form
    category_id = data.get('CategoryId')
    category_name = data.get('CategoryName')
    model = data.get('model')
    file_id = data.get('FileId')
    file_name = data.get('FileName')
    created_date = data.get('CreatedDate')
    url = data.get('url')

    # Create a new VideoSQLite instance
    new_video = VideoSQLite(
        CategoryId=category_id,
        CategoryName=category_name,
        model=model,
        FileId=file_id,
        FileName=file_name,
        CreatedDate=created_date,
        url=url
    )

    # Add the new_video instance to the session
    db_sqlite.session.add(new_video)

    # Commit the changes to the database
    db_sqlite.session.commit()

    return jsonify({
        'message': 'Video added successfully!'
    })

# Route to get video URLs
@app.route('/get_video_urls', methods=['GET'])
def get_video_urls():
    # Query all video URLs from the SQLite database
    video_urls_sqlite = [video.url for video in VideoSQLite.query.all()]

    return jsonify({
        'video_urls_sqlite': video_urls_sqlite,
    })

# Route to serve videos
@app.route('/videos/<filename>', methods=['GET'])
def get_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
