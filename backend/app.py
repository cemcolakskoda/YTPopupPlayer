from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\cemc\\Documents\\YTPopupPlayer\\backend\\instance\\sqlite.db'  # Replace with your actual path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Other configurations...

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Video(db.Model):
    __tablename__ = 'Video'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String(255))
    model = db.Column(db.String(255))
    file_id = db.Column(db.Integer)
    file_name = db.Column(db.String(255))
    created_date = db.Column(db.String(255))
    url = db.Column(db.VARCHAR(1000))


class VideoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Video

video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)

@app.route('/add_video', methods=['POST'])
def add_video():
    try:
        data = request.get_json()
        videos = data.get('videos', [])

        for video_data in videos:
            video = Video(
                category_id=video_data['category_id'],
                category_name=video_data['category_name'],
                model=video_data['model'],
                file_id=video_data['file_id'],
                file_name=video_data['file_name'],
                created_date=video_data['created_date'],
                url=video_data['url']
            )
            db.session.add(video)

        db.session.commit()
        return jsonify({"message": "Videos added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/get_videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    result = videos_schema.dump(videos)
    return jsonify({'videos': result})

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)

