from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()

class DatabaseHandler:
    """MongoDB connection handler for AI Tutor system."""
    
    def __init__(self):
        """Initialize MongoDB connection."""
        mongodb_uri = os.getenv('MONGO_DB_URI') or os.getenv('MONGODB_URI') or 'mongodb+srv://nishi:Gtn02fc2NHW9F4Gj@cluster0.zjfve.mongodb.net/ai_tutor_db?retryWrites=true&w=majority'
        self.client = MongoClient(mongodb_uri)
        self.db = self.client['ai_tutor_db']
        self.students = self.db['students']
        self.learning_sessions = self.db['learning_sessions']
        
    def get_student(self, student_id):
        """Get student data from the database."""
        student = self.students.find_one({'_id': student_id})
        return student or {}
    
    def update_student(self, student_id, data):
        """Update student data in the database."""
        data['updated_at'] = datetime.datetime.now()
        
        # If the student doesn't exist, set created_at
        if not self.students.find_one({'_id': student_id}):
            data['created_at'] = datetime.datetime.now()
            
        self.students.update_one(
            {'_id': student_id},
            {'$set': data},
            upsert=True
        )
        
    def create_learning_session(self, student_id, session_type, data):
        """Create a new learning session record."""
        session = {
            'student_id': student_id,
            'session_type': session_type,
            'data': data,
            'timestamp': datetime.datetime.now()
        }
        return self.learning_sessions.insert_one(session).inserted_id
        
    def get_learning_sessions(self, student_id, session_type=None, limit=10):
        """Get learning sessions for a student."""
        query = {'student_id': student_id}
        if session_type:
            query['session_type'] = session_type
            
        return list(self.learning_sessions.find(query).sort('timestamp', -1).limit(limit))