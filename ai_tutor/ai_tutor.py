from ai_tutor.purpose_agent import PurposeAgent
from ai_tutor.roadmap_agent import RoadmapAgent
from ai_tutor.lessons_agent import LessonsAgent
from ai_tutor.exam_manager_agent import ExamManagerAgent
from ai_tutor.evaluation_agent import EvaluationAgent
from ai_tutor.revision_agent import RevisionAgent
from ai_tutor.db_handler import DatabaseHandler

class AITutor:
    """Main AI Tutor class that orchestrates all the specialized agents."""
    
    def __init__(self):
        """Initialize the AI Tutor system with all specialized agents."""
        # Initialize the database handler
        self.db = DatabaseHandler()
        
        # Initialize all the specialized agents
        self.purpose_agent = PurposeAgent()
        self.roadmap_agent = RoadmapAgent()
        self.lessons_agent = LessonsAgent()
        self.exam_manager = ExamManagerAgent()
        self.evaluation_agent = EvaluationAgent()
        self.revision_agent = RevisionAgent()
        
    def get_student_status(self, student_id):
        """Get the current status of a student's learning journey."""
        student_data = self.db.get_student(student_id)
        
        # Determine what stage the student is at in their learning journey
        stages = {
            'purpose_defined': 'purpose' in student_data,
            'roadmap_created': 'roadmap' in student_data,
            'lessons_started': 'lessons' in student_data and student_data['lessons'],
            'exams_taken': 'exam_results' in student_data and student_data['exam_results'],
            'evaluated': 'evaluations' in student_data and student_data['evaluations'],
            'revision_planned': 'revision_plans' in student_data and student_data['revision_plans']
        }
        
        # Determine the next recommended action
        next_action = None
        if not stages['purpose_defined']:
            next_action = 'define_purpose'
        elif not stages['roadmap_created']:
            next_action = 'create_roadmap'
        elif not stages['lessons_started']:
            next_action = 'start_lessons'
        elif not stages['exams_taken']:
            next_action = 'take_exam'
        elif not stages['evaluated']:
            next_action = 'evaluate_learning'
        elif not stages['revision_planned']:
            next_action = 'create_revision_plan'
        else:
            next_action = 'continue_learning'
        
        # Create a summary of the student's progress
        progress_summary = {
            'student_id': student_id,
            'stages': stages,
            'next_action': next_action,
            'purpose': student_data.get('purpose', None),
            'roadmap_title': student_data.get('roadmap', {}).get('title', None),
            'lessons_completed': len(student_data.get('lessons', {})),
            'exams_taken': sum(len(results) for results in student_data.get('exam_results', {}).values()),
            'evaluations': len(student_data.get('evaluations', [])),
            'revision_plans': len(student_data.get('revision_plans', []))
        }
        
        return progress_summary
    
    def start_learning_journey(self, student_id, initial_query=None):
        """Start a new learning journey for a student."""
        # Step 1: Determine the student's purpose
        purpose_result = self.purpose_agent.determine_purpose(student_id, initial_query)
        
        if purpose_result['status'] == 'error':
            return {
                'status': 'error',
                'message': purpose_result['message']
            }
        
        # Step 2: Generate a roadmap based on the purpose
        roadmap_result = self.roadmap_agent.generate_roadmap(student_id)
        
        if roadmap_result['status'] == 'error':
            return {
                'status': 'error',
                'message': roadmap_result['message']
            }
        
        return {
            'status': 'started',
            'purpose': purpose_result['purpose'],
            'roadmap': roadmap_result['roadmap']
        }
    
    def get_next_lesson(self, student_id):
        """Get the next lesson for a student based on their progress."""
        student_data = self.db.get_student(student_id)
        
        # Check if we have a roadmap
        if 'roadmap' not in student_data:
            return {
                'status': 'error',
                'message': 'No roadmap found. Please start a learning journey first.'
            }
            
        roadmap = student_data['roadmap']
        lessons = student_data.get('lessons', {})
        
        # Find the first unit in the roadmap that doesn't have all lessons completed
        for unit in roadmap.get('units', []):
            unit_id = unit['title']
            unit_topics = unit.get('topics', [])
            
            # Check if we have completed all topics in this unit
            if unit_id not in lessons:
                lessons[unit_id] = {}
            
            unit_lessons = lessons[unit_id]
            
            for topic in unit_topics:
                if topic not in unit_lessons:
                    # Generate a lesson for this topic
                    lesson_result = self.lessons_agent.generate_lesson(student_id, unit_id, topic)
                    return {
                        'status': 'next_lesson',
                        'unit': unit_id,
                        'topic': topic,
                        'lesson': lesson_result['lesson'] if lesson_result['status'] == 'generated' else None
                    }
        
        # If we get here, all lessons in the roadmap have been completed
        return {
            'status': 'complete',
            'message': 'Congratulations! You have completed all lessons in your roadmap.'
        }
    
    def process_query(self, student_id, query):
        """Process a general query from the student and route to the appropriate agent."""
        # This is a simplified version that would use an LLM to determine intent
        # and route to the appropriate agent
        
        # For demonstration purposes, we'll just check for keywords
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['purpose', 'goal', 'why', 'what for']):
            # Query about purpose
            purpose_result = self.purpose_agent.determine_purpose(student_id, query)
            return {
                'agent': 'purpose',
                'result': purpose_result
            }
            
        elif any(word in query_lower for word in ['roadmap', 'plan', 'path', 'journey']):
            # Query about roadmap
            roadmap_result = self.roadmap_agent.generate_roadmap(student_id)
            return {
                'agent': 'roadmap',
                'result': roadmap_result
            }
            
        elif any(word in query_lower for word in ['lesson', 'learn', 'teach', 'topic']):
            # Query about lessons
            # This would ideally parse the topic from the query
            next_lesson = self.get_next_lesson(student_id)
            return {
                'agent': 'lessons',
                'result': next_lesson
            }
            
        elif any(word in query_lower for word in ['exam', 'test', 'quiz', 'assessment']):
            # Query about exams
            # This would ideally determine which unit to test
            exam_result = self.exam_manager.create_exam(student_id)
            return {
                'agent': 'exam_manager',
                'result': exam_result
            }
            
        elif any(word in query_lower for word in ['evaluate', 'performance', 'progress', 'how am i doing']):
            # Query about evaluation
            eval_result = self.evaluation_agent.evaluate_learning(student_id)
            return {
                'agent': 'evaluation',
                'result': eval_result
            }
            
        elif any(word in query_lower for word in ['revise', 'review', 'practice', 'improve']):
            # Query about revision
            revision_result = self.revision_agent.create_revision_plan(student_id)
            return {
                'agent': 'revision',
                'result': revision_result
            }
            
        else:
            # General query - in a real implementation this would be handled by an LLM
            # to provide a helpful response based on the student's context
            return {
                'agent': 'general',
                'result': {
                    'status': 'response',
                    'message': f"I understand you're asking about: {query}. Could you be more specific about what aspect of your learning you need help with?"
                }
            }
    
    def complete_exam(self, student_id, unit_id, exam_index, answers):
        """Process a completed exam and evaluate the results."""
        # Evaluate the exam
        evaluation_result = self.exam_manager.evaluate_exam(student_id, unit_id, exam_index, answers)
        
        if evaluation_result['status'] == 'error':
            return {
                'status': 'error',
                'message': evaluation_result['message']
            }
        
        # After exam completion, trigger a learning evaluation
        self.evaluation_agent.evaluate_learning(student_id)
        
        # If the exam was failed, suggest revision
        if not evaluation_result['final_score']['passed']:
            self.revision_agent.create_revision_plan(student_id)
            
            return {
                'status': 'failed',
                'results': evaluation_result,
                'message': 'You did not pass the exam. A revision plan has been created to help you improve.'
            }
        
        return {
            'status': 'passed',
            'results': evaluation_result,
            'message': 'Congratulations! You passed the exam.'
        }