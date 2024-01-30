from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Video model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)  # Fix the column definition
    category_name = db.Column(db.String(255))  # Fix the column definition
    model = db.Column(db.String(255))
    file_id = db.Column(db.Integer)
    file_name = db.Column(db.String(255))
    created_date = db.Column(db.String(255))
    url = db.Column(db.String(255))

# Create SQLite tables
with app.app_context():
    db.create_all()

@app.route('/add_video', methods=['POST'])
def add_video():
    data = request.get_json()
    new_video = Video(category_id=data['category_id'],
                      category_name=data['category_name'],
                      model=data['model'],
                      file_id=data['file_id'],
                      file_name=data['file_name'],
                      created_date=data['created_date'],
                      url=data['url'])
    db.session.add(new_video)
    db.session.commit()
    return jsonify({'message': 'Video added successfully'})

@app.route('/get_videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    video_list = [{'category_id': video.category_id,
                   'category_name': video.category_name,
                   'model': video.model,
                   'file_id': video.file_id,
                   'file_name': video.file_name,
                   'created_date': video.created_date,
                   'url': video.url} for video in videos]
    return jsonify({'videos': video_list})

if __name__ == '__main__':
    app.run(debug=True)
