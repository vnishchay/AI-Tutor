from ai_tutor.base_agent import BaseTutorAgent
import re
import openai
import os

class LessonsAgent(BaseTutorAgent):
    """Agent responsible for generating lesson content based on the roadmap."""
    
    def __init__(self):
        """Initialize the Lessons Agent."""
        super().__init__(
            agent_name="lessons_agent",
            description="An agent that generates educational lesson content",
            instruction="""
            You are an AI educational content creator tasked with generating high-quality lesson materials.
            For each lesson, create content that:
            
            1. Introduces the topic clearly with plain language and examples
            2. Explains core concepts step by step with visual illustrations when appropriate
            3. Provides practical examples and code snippets when applicable
            4. Includes exercises of varying difficulty for practice
            5. Summarizes key points for easy review
            6. Adds supplementary resources for deeper learning
            
            Adapt the content to the student's level and learning style.
            Use markdown formatting for clarity and structure.
            When a student is preparing for a specific board exam (CBSE, ICSE, etc.), 
            strictly follow that board's curriculum and syllabus.
            """
        )
        # Ensure OpenAI API key is set
        if os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_lesson(self, student_id, unit_id, topic_id=None):
        """Generate a lesson based on a unit from the roadmap."""
        # Get the student's roadmap data
        student_data = self.get_student_context(student_id)
        
        if 'roadmap' not in student_data:
            return {
                'status': 'error',
                'message': 'No roadmap found. Please generate a roadmap first.'
            }
            
        roadmap = student_data['roadmap']
        
        # Find the specified unit in the roadmap
        unit = None
        for u in roadmap.get('units', []):
            if u.get('title', '').lower() == unit_id.lower():
                unit = u
                break
        
        if not unit:
            return {
                'status': 'error',
                'message': f'Unit "{unit_id}" not found in the roadmap.'
            }
            
        # Get learning style preference from student's purpose if available
        learning_style = student_data.get('purpose', {}).get('learning_style', 'Interactive exercises')
        
        # Check if this is a board-specific curriculum request
        subject = student_data.get('purpose', {}).get('subject', '').lower()
        is_board_specific = any(board in subject for board in ['cbse', 'icse', 'igcse', 'state board'])
        board_type = None
        class_level = None
        
        # Extract board type and class level if applicable
        if is_board_specific:
            # Identify the board
            if 'cbse' in subject:
                board_type = 'CBSE'
            elif 'icse' in subject:
                board_type = 'ICSE'
            elif 'igcse' in subject:
                board_type = 'IGCSE'
            elif 'state board' in subject:
                # Try to extract which state board
                state_match = re.search(r'(\w+)\s+state\s+board', subject, re.IGNORECASE)
                if state_match:
                    board_type = f"{state_match.group(1).capitalize()} State Board"
                else:
                    board_type = 'State Board'
            
            # Extract class/grade level
            class_match = re.search(r'class\s*(\d+)', subject, re.IGNORECASE)
            if class_match:
                class_level = class_match.group(1)
            elif 'grade' in subject:
                grade_match = re.search(r'grade\s*(\d+)', subject, re.IGNORECASE)
                if grade_match:
                    class_level = grade_match.group(1)
            
        # In a real implementation, this would call the LLM to generate lesson content
        # based on the unit data and student's learning style
        # For demonstration purposes, we'll create sample lesson content
        
        # If a specific topic is provided, generate content for that topic
        if topic_id:
            # Check if topic exists in the unit
            topic_exists = False
            for topic in unit.get('topics', []):
                if topic.lower() == topic_id.lower():
                    topic_exists = True
                    break
                    
            if not topic_exists:
                return {
                    'status': 'error',
                    'message': f'Topic "{topic_id}" not found in unit "{unit_id}".'
                }
            
            # If this is a board-specific request, generate curriculum-aligned content
            if is_board_specific and board_type and class_level:
                lesson_content = self.generate_board_specific_lesson(
                    board_type, class_level, unit_id, topic_id, subject
                )
            elif topic_id.lower() == 'variables and data types':
                # Example lesson for Python Variables
                lesson_content = {
                    'title': 'Python Variables and Data Types',
                    'introduction': '''
# Python Variables and Data Types

Welcome to this lesson on Python variables and data types! Variables are fundamental to any programming language, allowing us to store and manipulate data.

In this lesson, we'll learn how to create variables, understand different data types, and use them effectively in your programs.
                    ''',
                    # ... rest of the Python variables lesson content ...
                    'sections': [
                        {
                            'title': 'What are Variables?',
                            'content': '''
Variables are containers for storing data values. Unlike other programming languages, Python has no command for declaring a variable. A variable is created the moment you first assign a value to it.

```python
# Creating variables
name = "John"
age = 30
height = 1.75
is_student = True

# Printing variables
print(name)       # Output: John
print(age)        # Output: 30
print(height)     # Output: 1.75
print(is_student) # Output: True
```

Variables in Python do not need to be declared with any particular type, and can even change type after they have been set.
                            '''
                        },
                        # ... remaining sections ...
                        {
                            'title': 'Python Data Types',
                            'content': '''
Python has several built-in data types:

1. **Text Type**: `str`
2. **Numeric Types**: `int`, `float`, `complex`
3. **Sequence Types**: `list`, `tuple`, `range`
4. **Mapping Type**: `dict`
5. **Set Types**: `set`, `frozenset`
6. **Boolean Type**: `bool`
7. **Binary Types**: `bytes`, `bytearray`, `memoryview`
8. **None Type**: `NoneType`

Here are examples of each:

```python
# Text Type
text = "Hello, Python!"

# Numeric Types
integer_number = 10
float_number = 10.5
complex_number = 1j

# Sequence Types
my_list = ["apple", "banana", "cherry"]
my_tuple = ("apple", "banana", "cherry")
my_range = range(6)

# Mapping Type
my_dict = {"name": "John", "age": 30}

# Set Types
my_set = {"apple", "banana", "cherry"}
my_frozenset = frozenset({"apple", "banana", "cherry"})

# Boolean Type
my_bool = True

# Binary Types
my_bytes = b"Hello"
my_bytearray = bytearray(5)
my_memoryview = memoryview(bytes(5))

# None Type
my_none = None
```

You can use the `type()` function to check the type of a variable:

```python
x = 5
print(type(x))  # Output: <class 'int'>
```
                            '''
                        },
                    ],
                    'exercises': [
                        {
                            'title': 'Basic Variable Practice',
                            'description': 'Create variables to store your name, age, and favorite color. Then print them.',
                            'solution': '''
```python
# Solution
name = "Your Name"
age = 25
favorite_color = "Blue"

print("My name is", name)
print("I am", age, "years old")
print("My favorite color is", favorite_color)
```
                            '''
                        },
                    ],
                    'summary': '''
# Summary

In this lesson, we covered:

- **Variables** - Containers for storing data values
- **Data Types** - Different categories of data (strings, numbers, lists, etc.)
- **Type Conversion** - Converting from one data type to another

Key points to remember:
1. Python variables don't need explicit declaration
2. Variables can change type after being set
3. Use type() function to check a variable's type
4. Type conversion functions: int(), float(), str(), etc.

Practice working with different data types to become comfortable with them!
                    ''',
                    'additional_resources': [
                        'Python.org Official Documentation: https://docs.python.org/3/tutorial/introduction.html',
                        'W3Schools Python Variables: https://www.w3schools.com/python/python_variables.asp',
                        'Interactive Python Data Types Tutorial: https://www.learnpython.org/en/Variables_and_Types'
                    ]
                }
            else:
                # Generic lesson for other topics - try to generate with OpenAI if possible
                try:
                    lesson_content = self.generate_dynamic_lesson(unit_id, topic_id, learning_style)
                except Exception as e:
                    print(f"Error generating lesson with OpenAI: {e}")
                    # Fallback to generic content
                    lesson_content = {
                        'title': topic_id,
                        'introduction': f'# Introduction to {topic_id}\n\nWelcome to this lesson on {topic_id}!',
                        'sections': [
                            {
                                'title': 'Basic Concepts',
                                'content': 'This section would contain the core concepts of the topic.'
                            },
                            {
                                'title': 'Examples',
                                'content': 'This section would provide practical examples.'
                            }
                        ],
                        'exercises': [
                            {
                                'title': 'Basic Exercise',
                                'description': 'A beginner-friendly exercise to practice the concepts.'
                            }
                        ],
                        'summary': '# Summary\n\nThis lesson covered the basics of ' + topic_id,
                        'additional_resources': [
                            'Relevant documentation',
                            'Tutorial websites',
                            'Practice exercises'
                        ]
                    }
                
            # Store the lesson in the database under the student's lessons
            lessons = student_data.get('lessons', {})
            if unit_id not in lessons:
                lessons[unit_id] = {}
            
            lessons[unit_id][topic_id] = lesson_content
            self.update_student_context(student_id, {'lessons': lessons})
            
            # Record this lesson generation session
            self.record_session(student_id, 'lesson_generation', {
                'unit_id': unit_id,
                'topic_id': topic_id,
                'generated_lesson': lesson_content
            })
            
            return {
                'status': 'generated',
                'lesson': lesson_content
            }
            
        else:
            # Generate summaries for all topics in the unit
            topic_summaries = []
            
            for topic in unit.get('topics', []):
                # In a real implementation, this would call the LLM to generate topic summaries
                # For demonstration purposes, we'll create sample summaries
                summary = f"Brief overview of {topic}: This would be a short introduction to what the topic covers."
                topic_summaries.append({
                    'topic': topic,
                    'summary': summary
                })
                
            return {
                'status': 'unit_overview',
                'unit': unit_id,
                'topics': topic_summaries
            }
            
    def generate_board_specific_lesson(self, board_type, class_level, unit_id, topic_id, subject):
        """Generate a lesson specific to a particular educational board's curriculum."""
        try:
            # Use OpenAI to generate curriculum-specific content
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert teacher following the {board_type} curriculum for Class {class_level}. Create a detailed, academically accurate lesson about '{topic_id}' from the unit '{unit_id}' for the subject '{subject}'. The lesson should strictly adhere to the official {board_type} syllabus for Class {class_level}, including all required concepts, definitions, and examples as specified in the curriculum."},
                    {"role": "user", "content": f"Please create a comprehensive lesson on '{topic_id}' following the {board_type} Class {class_level} curriculum. Include an introduction, detailed sections covering all key points from the syllabus, relevant examples, exercises for practice, and a summary."}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the generated content into our lesson structure
            introduction_match = re.search(r'#\s*Introduction.*?(?=#|$)', content, re.DOTALL)
            introduction = introduction_match.group(0) if introduction_match else f"# Introduction to {topic_id}\n\nWelcome to this lesson on {topic_id}!"
            
            # Extract sections
            sections = []
            section_matches = re.finditer(r'##\s*(.*?)\n(.*?)(?=##|\Z)', content, re.DOTALL)
            for match in section_matches:
                sections.append({
                    'title': match.group(1).strip(),
                    'content': match.group(2).strip()
                })
            
            # Extract exercises if present
            exercises = []
            exercise_match = re.search(r'#\s*Exercises.*?((?:\d+\.\s*.*?\n.*?)+)', content, re.DOTALL)
            if exercise_match:
                exercise_text = exercise_match.group(1)
                exercise_items = re.finditer(r'(\d+\.\s*.*?)\n(.*?)(?=\d+\.\s*|\Z)', exercise_text, re.DOTALL)
                for item in exercise_items:
                    exercises.append({
                        'title': item.group(1).strip(),
                        'description': item.group(2).strip()
                    })
            
            # If no exercises were found, create a default one
            if not exercises:
                exercises = [{
                    'title': f'Practice {topic_id}',
                    'description': f'Complete these exercises to test your understanding of {topic_id}.'
                }]
                
            # Extract summary
            summary_match = re.search(r'#\s*Summary.*?$', content, re.DOTALL)
            summary = summary_match.group(0) if summary_match else f"# Summary\n\nThis lesson covered {topic_id} according to the {board_type} Class {class_level} curriculum."
            
            # Create a structured lesson
            lesson = {
                'title': f'{topic_id} ({board_type} Class {class_level})',
                'introduction': introduction,
                'sections': sections,
                'exercises': exercises,
                'summary': summary,
                'additional_resources': [
                    f'{board_type} Class {class_level} Textbook',
                    f'{board_type} {subject} Reference Guide',
                    f'{board_type} Official Website for additional study materials'
                ],
                'curriculum_alignment': {
                    'board': board_type,
                    'class': class_level,
                    'subject': subject,
                    'unit': unit_id,
                    'topic': topic_id
                }
            }
            
            return lesson
        
        except Exception as e:
            print(f"Error generating board-specific lesson: {e}")
            # Fallback to a simplified board-specific structure
            return {
                'title': f'{topic_id} ({board_type} Class {class_level})',
                'introduction': f'# {topic_id}\n\nThis lesson follows the {board_type} curriculum for Class {class_level}.',
                'sections': [
                    {
                        'title': 'Key Concepts',
                        'content': f'The {board_type} curriculum requires students to understand the following key concepts for {topic_id}:'
                    },
                    {
                        'title': 'Examples from the Curriculum',
                        'content': 'Examples will be provided based on the textbook examples.'
                    }
                ],
                'exercises': [
                    {
                        'title': 'Practice Questions',
                        'description': f'These questions are designed to match the {board_type} examination pattern for Class {class_level}.'
                    }
                ],
                'summary': f'# Summary\n\nThis lesson covered the {board_type} Class {class_level} curriculum requirements for {topic_id}.',
                'additional_resources': [
                    f'{board_type} Class {class_level} Textbook',
                    f'{board_type} Sample Papers',
                    f'{board_type} Examination Guidelines'
                ]
            }
    
    def generate_dynamic_lesson(self, unit_id, topic_id, learning_style):
        """Generate a lesson dynamically using the OpenAI API."""
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert teacher creating a lesson on '{topic_id}' from the unit '{unit_id}'. The student prefers {learning_style} learning style. Create a detailed, engaging lesson with proper markdown formatting."},
                    {"role": "user", "content": f"Please create a comprehensive lesson on '{topic_id}' with an introduction, detailed explanations, examples, exercises for practice, and a summary."}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the generated content into our lesson structure (similar to board-specific parsing)
            introduction_match = re.search(r'#\s*.*?Introduction.*?(?=#|$)', content, re.DOTALL)
            introduction = introduction_match.group(0) if introduction_match else f"# Introduction to {topic_id}\n\nWelcome to this lesson on {topic_id}!"
            
            # Extract sections
            sections = []
            section_matches = re.finditer(r'##\s*(.*?)\n(.*?)(?=##|\Z)', content, re.DOTALL)
            for match in section_matches:
                sections.append({
                    'title': match.group(1).strip(),
                    'content': match.group(2).strip()
                })
            
            # Extract exercises if present
            exercises = []
            exercise_match = re.search(r'#.*?Exercises.*?((?:\d+\..*?\n.*?)+)', content, re.DOTALL)
            if exercise_match:
                exercise_text = exercise_match.group(1)
                exercise_items = re.finditer(r'(\d+\..*?)\n(.*?)(?=\d+\.|\Z)', exercise_text, re.DOTALL)
                for item in exercise_items:
                    exercises.append({
                        'title': item.group(1).strip(),
                        'description': item.group(2).strip()
                    })
            
            # If no exercises were found, create a default one
            if not exercises:
                exercises = [{
                    'title': f'Practice {topic_id}',
                    'description': f'Complete these exercises to test your understanding of {topic_id}.'
                }]
                
            # Extract summary
            summary_match = re.search(r'#\s*Summary.*?$', content, re.DOTALL)
            summary = summary_match.group(0) if summary_match else f"# Summary\n\nThis lesson covered the key aspects of {topic_id}."
            
            # Create a structured lesson
            return {
                'title': topic_id,
                'introduction': introduction,
                'sections': sections,
                'exercises': exercises,
                'summary': summary,
                'additional_resources': [
                    'Online tutorials and documentation',
                    'Practice exercises',
                    'Reference guides'
                ]
            }
        
        except Exception as e:
            # If OpenAI call fails, throw the exception up for the caller to handle
            print(f"Error in generate_dynamic_lesson: {e}")
            raise e