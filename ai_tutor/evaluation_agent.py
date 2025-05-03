from ai_tutor.base_agent import BaseTutorAgent

class EvaluationAgent(BaseTutorAgent):
    """Agent responsible for evaluating student learning and behavior."""
    
    def __init__(self):
        """Initialize the Evaluation Agent."""
        super().__init__(
            agent_name="evaluation_agent",
            description="An agent that analyzes student learning patterns and behavior",
            instruction="""
            You are an AI educational analyst tasked with evaluating student performance.
            For each evaluation:
            
            1. Analyze exam results to identify strengths and weaknesses
            2. Detect patterns in student learning behavior
            3. Identify topics that need more attention
            4. Evaluate overall progress against learning goals
            5. Provide actionable recommendations
            6. Consider the student's learning style and preferences
            
            Be constructive, encouraging, and focus on areas for improvement.
            """
        )
    
    def evaluate_learning(self, student_id):
        """Evaluate student's learning based on exam results."""
        # Get the student data
        student_data = self.get_student_context(student_id)
        
        # Check if we have exam results to evaluate
        if 'exam_results' not in student_data or not student_data['exam_results']:
            return {
                'status': 'error',
                'message': 'No exam results found. Complete some exams before evaluation.'
            }
            
        exam_results = student_data['exam_results']
        
        # Get the student's purpose and roadmap
        purpose = student_data.get('purpose', {})
        roadmap = student_data.get('roadmap', {})
        
        # In a real implementation, this would call the LLM to perform analysis
        # For demonstration purposes, we'll create a sample evaluation
        
        # Perform analysis on exam results
        strengths = []
        weaknesses = []
        learning_patterns = {}
        
        # Process each unit's exam results
        for unit_id, results_list in exam_results.items():
            if not results_list:
                continue
                
            # Get the most recent exam result for this unit
            latest_result = results_list[-1]
            final_score = latest_result['final_score']
            
            # Check if this was a good performance
            if final_score['percentage'] >= 80:
                strengths.append({
                    'unit': unit_id,
                    'score': final_score['percentage'],
                    'comment': f'Strong performance in {unit_id} with a score of {final_score["percentage"]}%'
                })
            elif final_score['percentage'] <= 60:
                weaknesses.append({
                    'unit': unit_id,
                    'score': final_score['percentage'],
                    'comment': f'Needs improvement in {unit_id} with a score of {final_score["percentage"]}%'
                })
                
            # Analyze individual questions
            topic_performance = {}
            
            for q_result in latest_result.get('results', []):
                question = exam_results[unit_id][latest_result['exam_index']]['questions'][q_result['question_index']]
                topic = question.get('topic', 'Unknown')
                
                # Initialize topic if not present
                if topic not in topic_performance:
                    topic_performance[topic] = {
                        'total_points': 0,
                        'earned_points': 0,
                        'questions': 0
                    }
                    
                # Update topic performance
                topic_performance[topic]['questions'] += 1
                topic_performance[topic]['total_points'] += q_result['points_possible']
                topic_performance[topic]['earned_points'] += q_result.get('points_earned', 0)
                
            # Identify strong and weak topics
            for topic, perf in topic_performance.items():
                if perf['questions'] > 0:  # Only evaluate if we have data
                    percent = (perf['earned_points'] / perf['total_points']) * 100 if perf['total_points'] > 0 else 0
                    
                    if percent >= 80:
                        strengths.append({
                            'topic': topic,
                            'unit': unit_id,
                            'score': round(percent, 1),
                            'comment': f'Strong understanding of {topic} with a score of {round(percent, 1)}%'
                        })
                    elif percent <= 60:
                        weaknesses.append({
                            'topic': topic,
                            'unit': unit_id,
                            'score': round(percent, 1),
                            'comment': f'Needs improvement in {topic} with a score of {round(percent, 1)}%'
                        })
        
        # Analyze learning patterns (in a real implementation, this would be more sophisticated)
        # Here we'll just simulate some learning pattern detection
        
        # Simulate detecting learning patterns based on exam performance
        learning_patterns = {
            'time_management': {
                'assessment': 'Good',
                'evidence': 'Completed exams within time limits',
                'recommendation': 'Continue with current pace'
            },
            'conceptual_understanding': {
                'assessment': 'Strong' if len(strengths) > len(weaknesses) else 'Needs improvement',
                'evidence': f'Performed well on {len(strengths)} topics vs struggled on {len(weaknesses)} topics',
                'recommendation': 'Focus more on understanding concepts rather than memorization' if len(weaknesses) > len(strengths) else 'Continue developing deep understanding'
            }
        }
        
        # Add a learning style observation if we have that information
        if 'learning_style' in purpose:
            learning_patterns['preferred_learning_style'] = {
                'assessment': purpose['learning_style'],
                'evidence': 'Based on initial purpose assessment',
                'recommendation': f'Continue using {purpose["learning_style"]} learning materials'
            }
        
        # Create difficult topics list for roadmap adjustment
        difficult_topics = [w['topic'] for w in weaknesses if 'topic' in w]
        
        # Generate overall recommendations
        recommendations = [
            'Focus on reviewing the weak topics identified in the evaluation',
            'Spend more time on practical exercises for difficult concepts',
            'Consider revisiting foundational topics before moving to more advanced material'
        ]
        
        if len(strengths) > len(weaknesses):
            recommendations.append('You\'re making good progress! Consider tackling more challenging material next')
        
        # Create the evaluation object
        evaluation = {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'learning_patterns': learning_patterns,
            'difficult_topics': difficult_topics,
            'progress_assessment': 'Good progress' if len(strengths) > len(weaknesses) else 'Needs improvement',
            'recommendations': recommendations
        }
        
        # Store the evaluation in the student's data
        evaluations = student_data.get('evaluations', [])
        evaluations.append(evaluation)
        self.update_student_context(student_id, {'evaluations': evaluations})
        
        # Record this evaluation session
        self.record_session(student_id, 'learning_evaluation', {
            'evaluation': evaluation
        })
        
        return {
            'status': 'evaluated',
            'evaluation': evaluation
        }