from ai_tutor.base_agent import BaseTutorAgent

class RevisionAgent(BaseTutorAgent):
    """Agent responsible for creating personalized revision materials."""
    
    def __init__(self):
        """Initialize the Revision Agent."""
        super().__init__(
            agent_name="revision_agent",
            description="An agent that creates personalized revision materials",
            instruction="""
            You are an AI educational revision specialist tasked with creating effective review materials.
            For each revision plan:
            
            1. Focus on the student's identified weak areas from evaluations
            2. Provide concise summaries of key concepts
            3. Create targeted practice exercises
            4. Offer memory aids and learning techniques
            5. Develop spaced repetition schedules
            6. Adapt materials to the student's learning style
            
            Ensure the revision materials are engaging and address specific knowledge gaps.
            """
        )
    
    def create_revision_plan(self, student_id):
        """Create a personalized revision plan based on evaluations."""
        # Get the student data
        student_data = self.get_student_context(student_id)
        
        # Check if we have evaluations to base the revision on
        if 'evaluations' not in student_data or not student_data['evaluations']:
            return {
                'status': 'error',
                'message': 'No evaluations found. Complete an evaluation before creating a revision plan.'
            }
            
        # Get the most recent evaluation
        evaluation = student_data['evaluations'][-1]
        
        # Get the roadmap and lessons
        roadmap = student_data.get('roadmap', {})
        lessons = student_data.get('lessons', {})
        
        # Get the student's learning style if available
        learning_style = student_data.get('purpose', {}).get('learning_style', 'Interactive exercises')
        
        # In a real implementation, this would call the LLM to generate a revision plan
        # For demonstration purposes, we'll create a sample revision plan
        
        # Extract weaknesses from the evaluation
        weaknesses = evaluation.get('weaknesses', [])
        difficult_topics = evaluation.get('difficult_topics', [])
        
        # Create revision materials for each weakness
        revision_materials = []
        
        for weakness in weaknesses:
            # Get the unit and topic if available
            unit = weakness.get('unit')
            topic = weakness.get('topic')
            
            # Skip if we don't have enough info
            if not unit:
                continue
                
            # Create revision material
            revision_material = {
                'unit': unit,
                'topic': topic if topic else 'General unit concepts',
                'score': weakness.get('score', 0),
                'materials': []
            }
            
            # Add a concept summary
            revision_material['materials'].append({
                'type': 'summary',
                'title': 'Concept Review',
                'content': f'A concise summary of the key concepts in {topic if topic else unit} would go here.',
                'estimated_time': '15 minutes'
            })
            
            # Add practice exercises based on learning style
            if learning_style == 'Interactive exercises':
                revision_material['materials'].append({
                    'type': 'interactive_exercise',
                    'title': 'Interactive Practice',
                    'content': f'An interactive exercise focusing on {topic if topic else unit} would go here.',
                    'estimated_time': '20 minutes'
                })
            elif learning_style == 'Visual':
                revision_material['materials'].append({
                    'type': 'visual_aid',
                    'title': 'Visual Concept Map',
                    'content': f'A visual representation of {topic if topic else unit} concepts would go here.',
                    'estimated_time': '15 minutes'
                })
            else:
                revision_material['materials'].append({
                    'type': 'practice_problems',
                    'title': 'Practice Problems',
                    'content': f'A set of practice problems for {topic if topic else unit} would go here.',
                    'estimated_time': '20 minutes'
                })
            
            # Add memory aid
            revision_material['materials'].append({
                'type': 'memory_aid',
                'title': 'Memory Aid',
                'content': f'A mnemonic or other memory device for {topic if topic else unit} would go here.',
                'estimated_time': '5 minutes'
            })
            
            # Add quiz
            revision_material['materials'].append({
                'type': 'quiz',
                'title': 'Quick Check Quiz',
                'content': f'A short quiz to test understanding of {topic if topic else unit} would go here.',
                'estimated_time': '10 minutes'
            })
            
            revision_materials.append(revision_material)
        
        # Create a spaced repetition schedule
        schedule = []
        
        # Day 1: Initial review of all weak areas
        day1 = {
            'day': 1,
            'focus': 'Initial review of all weak areas',
            'activities': [
                {'material': f"{material['unit']} - {material['topic']}", 'time': '20 minutes'}
                for material in revision_materials
            ],
            'total_time': f"{len(revision_materials) * 20} minutes"
        }
        schedule.append(day1)
        
        # Day 2: Focused practice on the weakest areas
        weakest_areas = revision_materials[:2] if len(revision_materials) > 2 else revision_materials
        day2 = {
            'day': 2,
            'focus': 'Focused practice on weakest areas',
            'activities': [
                {'material': f"{material['unit']} - {material['topic']} (deep focus)", 'time': '30 minutes'}
                for material in weakest_areas
            ],
            'total_time': f"{len(weakest_areas) * 30} minutes"
        }
        schedule.append(day2)
        
        # Day 4: Spaced review of all weak areas
        day4 = {
            'day': 4,
            'focus': 'Spaced review of all areas',
            'activities': [
                {'material': f"{material['unit']} - {material['topic']} (quick review)", 'time': '15 minutes'}
                for material in revision_materials
            ],
            'total_time': f"{len(revision_materials) * 15} minutes"
        }
        schedule.append(day4)
        
        # Day 7: Final review and self-test
        day7 = {
            'day': 7,
            'focus': 'Final review and self-assessment',
            'activities': [
                {'material': f"Comprehensive Quiz on Weak Areas", 'time': '30 minutes'},
                {'material': f"Review of Quiz Results", 'time': '20 minutes'}
            ],
            'total_time': '50 minutes'
        }
        schedule.append(day7)
        
        # Create the complete revision plan
        revision_plan = {
            'student_id': student_id,
            'created_at': '__CURRENT_TIMESTAMP__',  # This would be the actual timestamp in a real implementation
            'based_on_evaluation': student_data['evaluations'].index(evaluation),
            'focus_areas': [f"{material['unit']} - {material['topic']}" for material in revision_materials],
            'materials': revision_materials,
            'spaced_repetition_schedule': schedule,
            'recommendations': [
                'Set aside specific times each day for revision',
                'Focus on understanding concepts rather than memorization',
                'Take short breaks between revision sessions',
                'Regularly test yourself on the material'
            ]
        }
        
        # Store the revision plan in the student's data
        revision_plans = student_data.get('revision_plans', [])
        revision_plans.append(revision_plan)
        self.update_student_context(student_id, {'revision_plans': revision_plans})
        
        # Record this revision plan creation session
        self.record_session(student_id, 'revision_plan_creation', {
            'based_on_evaluation': student_data['evaluations'].index(evaluation),
            'revision_plan': revision_plan
        })
        
        return {
            'status': 'created',
            'revision_plan': revision_plan
        }