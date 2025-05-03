from ai_tutor.ai_tutor import AITutor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the AI Tutor system."""
    print("AI Tutor System - Learning Made Personal")
    print("=======================================")
    
    # Initialize the AI Tutor
    tutor = AITutor()
    
    # Get or create student ID
    student_id = input("Enter your student ID (or create a new one): ").strip()
    if not student_id:
        student_id = f"student_{os.urandom(4).hex()}"
        print(f"Created new student ID: {student_id}")
    
    # Get the current status of the student
    status = tutor.get_student_status(student_id)
    
    # Welcome message
    if status['next_action'] == 'define_purpose':
        print(f"\nWelcome, new student {student_id}! Let's start your learning journey.")
        print("First, I need to understand your learning goals and preferences.")
        
        purpose_query = input("\nWhy do you want to learn? What are your goals? ")
        journey = tutor.start_learning_journey(student_id, purpose_query)
        
        if journey['status'] == 'started':
            print("\nGreat! I've recorded your purpose and created a learning roadmap:")
            print(f"Subject: {journey['purpose']['subject']}")
            print(f"Level: {journey['purpose']['level']}")
            print(f"Roadmap: {journey['roadmap']['title']}")
            print(f"Estimated completion time: {journey['roadmap']['estimated_completion_time']}")
        else:
            print(f"\nThere was an issue starting your learning journey: {journey.get('message', 'Unknown error')}")
    else:
        # Welcome back message
        print(f"\nWelcome back, {student_id}!")
        if status['roadmap_title']:
            print(f"You're currently working on: {status['roadmap_title']}")
        
        if status['next_action'] == 'create_roadmap':
            print("Let's create your learning roadmap based on your goals.")
        elif status['next_action'] == 'start_lessons':
            print("You're ready to start your lessons!")
        elif status['next_action'] == 'take_exam':
            print("You've completed some lessons. Ready for an exam?")
        elif status['next_action'] == 'evaluate_learning':
            print("Let's evaluate your learning progress so far.")
        elif status['next_action'] == 'create_revision_plan':
            print("Let's create a revision plan to help you improve.")
        else:
            print("Continue with your learning journey!")
    
    # Main interaction loop
    print("\n" + "="*50)
    print("Type your questions or commands, or 'exit' to quit.")
    print("Examples: 'What's my next lesson?', 'Create a quiz', 'How am I doing?'")
    print("="*50 + "\n")
    
    while True:
        query = input("\nYour query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Thank you for learning with AI Tutor. Goodbye!")
            break
            
        # Process the query
        response = tutor.process_query(student_id, query)
        
        # Display the response based on which agent handled it
        agent = response['agent']
        result = response['result']
        
        if agent == 'purpose':
            if result['status'] == 'determined':
                print("\nI've recorded your learning purpose:")
                for key, value in result['purpose'].items():
                    print(f"{key.capitalize()}: {value}")
            elif result['status'] == 'existing':
                print("\nYour current learning purpose:")
                for key, value in result['purpose'].items():
                    print(f"{key.capitalize()}: {value}")
        
        elif agent == 'roadmap':
            if result['status'] == 'generated':
                print(f"\nRoadmap: {result['roadmap']['title']}")
                print(f"Estimated completion time: {result['roadmap']['estimated_completion_time']}")
                print("\nUnits:")
                for i, unit in enumerate(result['roadmap']['units']):
                    print(f"{i+1}. {unit['title']} ({unit['duration']})")
            elif result['status'] == 'existing':
                print(f"\nYour existing roadmap: {result['roadmap']['title']}")
        
        elif agent == 'lessons':
            if result['status'] == 'next_lesson':
                print(f"\nNext lesson: {result['unit']} - {result['topic']}")
                if result['lesson']:
                    print(f"\n{result['lesson']['introduction']}")
                    print("\nWould you like to see the full lesson? (yes/no)")
                    see_lesson = input().strip().lower()
                    if see_lesson == 'yes':
                        print("\n" + "="*50)
                        print(f"LESSON: {result['lesson']['title']}")
                        print("="*50)
                        print(result['lesson']['introduction'])
                        for section in result['lesson']['sections']:
                            print(f"\n## {section['title']}")
                            print(section['content'])
                        print("\n## Exercises")
                        for exercise in result['lesson']['exercises']:
                            print(f"\n### {exercise['title']}")
                            print(exercise['description'])
                        print("\n" + "="*50)
            elif result['status'] == 'complete':
                print(result['message'])
        
        elif agent == 'exam_manager':
            if result['status'] == 'created':
                print(f"\nExam created: {result['exam']['title']}")
                print(f"Description: {result['exam']['description']}")
                print(f"Total points: {result['exam']['total_points']}")
                print(f"Passing score: {result['exam']['passing_score']}")
                print(f"Time limit: {result['exam']['time_limit_minutes']} minutes")
                print(f"Number of questions: {len(result['exam']['questions'])}")
                print("\nWould you like to take this exam now? (yes/no)")
            else:
                print(result.get('message', 'Could not create exam.'))
        
        elif agent == 'evaluation':
            if result['status'] == 'evaluated':
                eval_data = result['evaluation']
                print("\nLearning Evaluation:")
                print(f"Overall assessment: {eval_data['progress_assessment']}")
                
                if eval_data['strengths']:
                    print("\nStrengths:")
                    for strength in eval_data['strengths'][:3]:  # Show top 3
                        print(f"- {strength['comment']}")
                
                if eval_data['weaknesses']:
                    print("\nAreas for improvement:")
                    for weakness in eval_data['weaknesses'][:3]:  # Show top 3
                        print(f"- {weakness['comment']}")
                
                print("\nRecommendations:")
                for rec in eval_data['recommendations']:
                    print(f"- {rec}")
            else:
                print(result.get('message', 'Could not evaluate learning.'))
        
        elif agent == 'revision':
            if result['status'] == 'created':
                plan = result['revision_plan']
                print("\nRevision Plan Created!")
                print(f"Focus areas: {', '.join(plan['focus_areas'][:3])}")
                
                print("\nSpaced Repetition Schedule:")
                for day in plan['spaced_repetition_schedule']:
                    print(f"Day {day['day']}: {day['focus']} ({day['total_time']})")
                
                print("\nRecommendations:")
                for rec in plan['recommendations']:
                    print(f"- {rec}")
            else:
                print(result.get('message', 'Could not create revision plan.'))
        
        else:  # General or unknown agent
            print(f"\n{result.get('message', 'I didn\'t understand that query.')}")

if __name__ == "__main__":
    main()