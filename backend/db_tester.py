import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class DatabaseTester:
    def __init__(self, test_mode):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(self.app)

        # Define your VideoSQLite model
        class VideoSQLite(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            category_id = self.db.Column(self.db.Integer)
            category_name = self.db.Column(self.db.String(255))
            model = self.db.Column(self.db.String(255))
            file_id = self.db.Column(self.db.Integer)
            file_name = self.db.Column(self.db.String(255))
            created_date = self.db.Column(self.db.String(255))
            url = self.db.Column(self.db.String(255), nullable=False)

        # Create SQLite tables
        with self.app.app_context():
            self.db.create_all()

        self.VideoSQLite = VideoSQLite  # Assign the model to an attribute

        self.test_mode = test_mode

    def perform_test(self):
        with self.app.app_context():
            if self.test_mode == 1:
                # Querying Data
                all_videos = self.VideoSQLite.query.all()
                print(all_videos)

            elif self.test_mode == 2:
                # Filter records based on a condition
                videos_with_category_id_1 = self.VideoSQLite.query.filter_by(category_id=1).all()
                print(videos_with_category_id_1)

            elif self.test_mode == 3:
                # Adding Data
                new_video = self.VideoSQLite(category_id=1, category_name='Example', model='ExampleModel', file_id=123, file_name='ExampleFile', created_date='2024-01-30', url='https://example.com')
                self.db.session.add(new_video)
                self.db.session.commit()
                print("New video added successfully!")

            elif self.test_mode == 4:
                # Updating Data
                video_to_update = self.VideoSQLite.query.get(1)  # Replace 1 with the actual ID of the record you want to update
                video_to_update.category_name = 'UpdatedCategory'
                self.db.session.commit()
                print("Video updated successfully!")

            elif self.test_mode == 5:
                # Deleting Data
                video_to_delete = self.VideoSQLite.query.get(1)  # Replace 1 with the actual ID of the record you want to delete
                self.db.session.delete(video_to_delete)
                self.db.session.commit()
                print("Video deleted successfully!")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <test_mode>")
        sys.exit(1)

    try:
        test_mode = int(sys.argv[1])
        tester = DatabaseTester(test_mode)
        tester.perform_test()
    except ValueError:
        print("Invalid test_mode. Please provide an integer.")
        sys.exit(1)
