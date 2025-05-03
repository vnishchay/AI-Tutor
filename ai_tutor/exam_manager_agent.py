from ai_tutor.base_agent import BaseTutorAgent

class ExamManagerAgent(BaseTutorAgent):
    """Agent responsible for creating and evaluating exams."""
    
    def __init__(self):
        """Initialize the Exam Manager Agent."""
        super().__init__(
            agent_name="exam_manager_agent",
            description="An agent that creates and evaluates assessments",
            instruction="""
            You are an AI educational assessment specialist tasked with creating effective examinations.
            For each assessment:
            
            1. Create varied question types (multiple choice, short answer, coding exercises, etc.)
            2. Ensure questions test understanding, not just memorization
            3. Include questions of varying difficulty
            4. Provide clear instructions for each question
            5. Create a comprehensive rubric for evaluation
            6. Generate detailed solutions for all questions
            
            Adapt assessments to the student's level and the topics they've studied.
            """
        )
    
    def create_exam(self, student_id, unit_id=None):
        """Create an exam based on completed lessons."""
        # Get the student data
        student_data = self.get_student_context(student_id)
        
        # Check if we have lessons to base the exam on
        if 'lessons' not in student_data:
            return {
                'status': 'error',
                'message': 'No lessons found. Complete some lessons before taking an exam.'
            }
            
        lessons = student_data['lessons']
        
        # If unit_id is provided, create an exam for that specific unit
        if unit_id and unit_id in lessons:
            unit_lessons = lessons[unit_id]
            
            # In a real implementation, this would call the LLM to generate an exam
            # based on the specific unit lessons
            # For demonstration purposes, we'll create a sample exam
            
            # Create questions from the unit's topics
            questions = []
            
            for topic, lesson in unit_lessons.items():
                # Example: Create a multiple choice question
                questions.append({
                    'type': 'multiple_choice',
                    'topic': topic,
                    'question': f'Which of the following is true about {topic}?',
                    'options': [
                        'Option A - This would be the correct answer',
                        'Option B - This would be incorrect',
                        'Option C - This would be incorrect',
                        'Option D - This would be incorrect'
                    ],
                    'correct_answer': 0,  # Index of the correct option
                    'points': 5
                })
                
                # Example: Create a short answer question
                questions.append({
                    'type': 'short_answer',
                    'topic': topic,
                    'question': f'Explain the key concept of {topic} in your own words.',
                    'sample_answer': 'This would be a sample acceptable answer that demonstrates understanding.',
                    'rubric': [
                        'Demonstrates clear understanding of the concept - 5 points',
                        'Uses appropriate terminology - 3 points',
                        'Provides relevant example - 2 points'
                    ],
                    'points': 10
                })
                
                # For coding topics, add a coding question
                if 'Python' in topic or 'program' in topic.lower():
                    questions.append({
                        'type': 'coding',
                        'topic': topic,
                        'question': 'Write a Python function that does something relevant to this topic.',
                        'starter_code': '# Your code here\ndef solution():\n    pass',
                        'test_cases': [
                            {'input': 'test_input_1', 'expected_output': 'expected_output_1'},
                            {'input': 'test_input_2', 'expected_output': 'expected_output_2'}
                        ],
                        'points': 15
                    })
            
            # Create the exam object
            exam = {
                'title': f'Assessment for {unit_id}',
                'description': f'This exam tests your knowledge of the topics covered in {unit_id}.',
                'total_points': sum(q['points'] for q in questions),
                'passing_score': int(sum(q['points'] for q in questions) * 0.7),  # 70% to pass
                'time_limit_minutes': 60,
                'questions': questions
            }
            
            # Store the exam in the student's data
            exams = student_data.get('exams', {})
            if unit_id not in exams:
                exams[unit_id] = []
            
            exams[unit_id].append(exam)
            self.update_student_context(student_id, {'exams': exams})
            
            # Record this exam creation session
            self.record_session(student_id, 'exam_creation', {
                'unit_id': unit_id,
                'exam': exam
            })
            
            return {
                'status': 'created',
                'exam': exam
            }
        
        # If no specific unit is provided, create a comprehensive exam across all lessons
        else:
            # In a real implementation, this would call the LLM to generate a comprehensive exam
            # For demonstration purposes, we'll create a sample comprehensive exam
            
            # Create questions sampling from all units
            questions = []
            total_questions = 0
            
            for unit_id, unit_lessons in lessons.items():
                # Limit to 2 questions per unit to keep the exam reasonable
                for topic in list(unit_lessons.keys())[:2]:
                    # Add a mixed question
                    questions.append({
                        'type': 'mixed',
                        'unit': unit_id,
                        'topic': topic,
                        'question': f'Explain and provide an example of {topic}.',
                        'rubric': [
                            'Explanation is clear and accurate - 5 points',
                            'Example is relevant and demonstrates understanding - 5 points'
                        ],
                        'points': 10
                    })
                    
                    total_questions += 1
                    
                    # Stop at 10 questions for a comprehensive exam
                    if total_questions >= 10:
                        break
                
                if total_questions >= 10:
                    break
            
            # Create the comprehensive exam object
            exam = {
                'title': 'Comprehensive Assessment',
                'description': 'This exam tests your knowledge across all units you have studied.',
                'total_points': sum(q['points'] for q in questions),
                'passing_score': int(sum(q['points'] for q in questions) * 0.7),  # 70% to pass
                'time_limit_minutes': 90,
                'questions': questions
            }
            
            # Store the comprehensive exam in the student's data
            exams = student_data.get('exams', {})
            if 'comprehensive' not in exams:
                exams['comprehensive'] = []
            
            exams['comprehensive'].append(exam)
            self.update_student_context(student_id, {'exams': exams})
            
            # Record this exam creation session
            self.record_session(student_id, 'exam_creation', {
                'type': 'comprehensive',
                'exam': exam
            })
            
            return {
                'status': 'created',
                'exam': exam
            }
    
    def evaluate_exam(self, student_id, unit_id, exam_index, answers):
        """Evaluate student's exam answers."""
        # Get the student data
        student_data = self.get_student_context(student_id)
        
        # Check if we have exams for the student
        if 'exams' not in student_data:
            return {
                'status': 'error',
                'message': 'No exams found for this student.'
            }
            
        exams = student_data.get('exams', {})
        
        # Check if unit_id exists in exams
        if unit_id not in exams:
            return {
                'status': 'error',
                'message': f'No exams found for unit {unit_id}.'
            }
            
        # Check if the exam_index is valid
        if exam_index >= len(exams[unit_id]):
            return {
                'status': 'error',
                'message': f'Invalid exam index {exam_index} for unit {unit_id}.'
            }
            
        # Get the exam
        exam = exams[unit_id][exam_index]
        
        # Check if answers match questions in length
        if len(answers) != len(exam['questions']):
            return {
                'status': 'error',
                'message': f'Number of answers ({len(answers)}) does not match number of questions ({len(exam["questions"])}).'
            }
            
        # In a real implementation, this would call the LLM to evaluate subjective answers
        # For demonstration purposes, we'll simulate evaluation
        
        evaluation_results = []
        total_earned_points = 0
        
        for i, (question, answer) in enumerate(zip(exam['questions'], answers)):
            # Evaluate based on question type
            if question['type'] == 'multiple_choice':
                # For multiple choice, check if the answer matches the correct option index
                correct = answer == question['correct_answer']
                points_earned = question['points'] if correct else 0
                
                evaluation_results.append({
                    'question_index': i,
                    'correct': correct,
                    'points_earned': points_earned,
                    'points_possible': question['points'],
                    'feedback': 'Correct!' if correct else f'Incorrect. The correct answer was option {question["correct_answer"] + 1}.'
                })
                
            elif question['type'] in ['short_answer', 'mixed']:
                # For short answer/mixed questions, simulate evaluation
                # In a real implementation, this would use the LLM to evaluate against the rubric
                
                # Simulate a score between 60% and 100% of possible points
                import random
                score_percent = random.uniform(0.6, 1.0)
                points_earned = int(question['points'] * score_percent)
                
                evaluation_results.append({
                    'question_index': i,
                    'points_earned': points_earned,
                    'points_possible': question['points'],
                    'feedback': f'Good attempt. You earned {points_earned}/{question["points"]} points.'
                    + '\nFeedback: Your answer covered the main points but could have provided more specific examples.'
                })
                
            elif question['type'] == 'coding':
                # For coding questions, simulate code evaluation
                # In a real implementation, this would execute the code against test cases
                
                # Simulate a score between 50% and 100% of possible points
                import random
                score_percent = random.uniform(0.5, 1.0)
                points_earned = int(question['points'] * score_percent)
                
                evaluation_results.append({
                    'question_index': i,
                    'points_earned': points_earned,
                    'points_possible': question['points'],
                    'feedback': f'Your code solution earned {points_earned}/{question["points"]} points.'
                    + '\nFeedback: Your code handles the main test cases, but could be optimized further.'
                })
                
            # Add the earned points to the total
            total_earned_points += points_earned
        
        # Calculate the final score
        final_score = {
            'points_earned': total_earned_points,
            'points_possible': exam['total_points'],
            'percentage': round((total_earned_points / exam['total_points']) * 100, 1),
            'passed': total_earned_points >= exam['passing_score']
        }
        
        # Add comments based on performance
        if final_score['passed']:
            if final_score['percentage'] >= 90:
                final_score['comments'] = 'Excellent work! You have a strong understanding of the material.'
            elif final_score['percentage'] >= 80:
                final_score['comments'] = 'Very good job! You have a solid grasp of most concepts.'
            else:
                final_score['comments'] = 'Good job! You have passed the exam, but there are areas for improvement.'
        else:
            final_score['comments'] = 'You did not pass the exam. Review the feedback and consider revisiting the lessons before trying again.'
        
        # Store the evaluation results in the student's data
        exam_results = student_data.get('exam_results', {})
        if unit_id not in exam_results:
            exam_results[unit_id] = []
            
        exam_results[unit_id].append({
            'exam_index': exam_index,
            'timestamp': '__CURRENT_TIMESTAMP__',  # This would be the actual timestamp in a real implementation
            'results': evaluation_results,
            'final_score': final_score
        })
        
        self.update_student_context(student_id, {'exam_results': exam_results})
        
        # Record this exam evaluation session
        self.record_session(student_id, 'exam_evaluation', {
            'unit_id': unit_id,
            'exam_index': exam_index,
            'results': evaluation_results,
            'final_score': final_score
        })
        
        return {
            'status': 'evaluated',
            'results': evaluation_results,
            'final_score': final_score
        }