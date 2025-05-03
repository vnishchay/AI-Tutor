from google.adk.agents import LlmAgent
from ai_tutor.db_handler import DatabaseHandler

class BaseTutorAgent:
    """Base class for all AI Tutor agents."""
    
    def __init__(self, agent_name, description, instruction):
        """Initialize the base agent with ADK LlmAgent."""
        self.agent = LlmAgent(
            model="gemini-2.0-flash-exp",
            name=agent_name,
            description=description,
            instruction=instruction
        )
        self.db = DatabaseHandler()
        
    def get_student_context(self, student_id):
        """Get student context from the database."""
        return self.db.get_student(student_id)
        
    def update_student_context(self, student_id, data):
        """Update student context in the database."""
        self.db.update_student(student_id, data)
        
    def record_session(self, student_id, session_type, data):
        """Record a learning session in the database."""
        return self.db.create_learning_session(student_id, session_type, data)