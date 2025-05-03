from ai_tutor.base_agent import BaseTutorAgent
import openai
import re
import os

class RoadmapAgent(BaseTutorAgent):
    """Agent responsible for creating a learning roadmap based on student's purpose."""
    
    def __init__(self):
        """Initialize the Roadmap Agent."""
        super().__init__(
            agent_name="roadmap_agent",
            description="An agent that creates personalized learning roadmaps",
            instruction="""
            You are an AI educational planner tasked with creating personalized learning roadmaps.
            Based on the student's purpose and goals, create a structured learning path that:
            
            1. Breaks down the subject into logical learning units
            2. Sequences topics from foundational to advanced
            3. Estimates time required for each learning unit
            4. Sets milestones and checkpoints for progress tracking
            5. Includes practical exercises and projects
            6. Adapts to the student's learning style and time commitment
            
            The roadmap should be comprehensive yet realistic given the student's constraints.
            """
        )
        # Ensure OpenAI API key is set
        if os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_roadmap(self, student_id):
        """Generate a learning roadmap based on student's purpose."""
        # Get the student's purpose data
        student_data = self.get_student_context(student_id)
        
        # Check if the student has a defined purpose
        if 'purpose' not in student_data:
            return {
                'status': 'error',
                'message': 'Student purpose not defined. Please complete purpose determination first.'
            }
        
        purpose = student_data['purpose']
        
        # Check if roadmap already exists
        if 'roadmap' in student_data:
            return {
                'status': 'existing',
                'roadmap': student_data['roadmap']
            }
        
        # Create a subject-specific roadmap based on the purpose
        roadmap = self.create_subject_specific_roadmap(purpose)
        
        # Store the roadmap in the database
        self.update_student_context(student_id, {'roadmap': roadmap})
        
        # Record this session
        self.record_session(student_id, 'roadmap_generation', {
            'purpose': purpose,
            'generated_roadmap': roadmap
        })
        
        return {
            'status': 'generated',
            'roadmap': roadmap
        }
    
    def create_subject_specific_roadmap(self, purpose):
        """Create a roadmap specific to the subject and level provided in purpose."""
        subject = purpose['subject'].lower()
        level = purpose['level'].lower()
        
        # Check for CBSE curriculum specifically
        is_cbse = False
        class_level = None
        
        if "cbse" in subject:
            is_cbse = True
        if "class" in subject:
            match = re.search(r'class\s*(\d+)', subject, re.IGNORECASE)
            if match:
                class_level = match.group(1)
                
        # Check for history subject specifically
        if "history" in subject:
            if is_cbse and class_level == "6":
                return self.create_cbse_class6_history_roadmap()
            elif "history" in subject:
                return self.create_generic_history_roadmap(level)
        # C++ specific roadmap
        elif "c++" in subject:
            return self.create_cpp_roadmap(level)
        # Python fallback is kept as a reference for custom subjects
        elif "python" in subject or "programming" in subject:
            if level == "beginner":
                return self.create_python_beginner_roadmap()
        # Math specific roadmap
        elif "math" in subject or "mathematics" in subject:
            if is_cbse and class_level:
                return self.create_cbse_math_roadmap(class_level)
        # Science specific roadmap
        elif "science" in subject:
            if is_cbse and class_level:
                return self.create_cbse_science_roadmap(class_level)
            
        # Try to generate a custom roadmap using LLM if we don't have a specific template
        try:
            return self.generate_custom_roadmap_with_llm(purpose)
        except Exception as e:
            print(f"Error generating custom roadmap: {e}")
            # Fallback to a generic roadmap
            return self.create_generic_roadmap(purpose)
    
    def create_cpp_roadmap(self, level):
        """Create a roadmap for C++ learning."""
        if level == "beginner":
            return {
                'title': 'C++ Programming for Beginners',
                'estimated_completion_time': '12 weeks',
                'units': [
                    {
                        'title': 'C++ Basics and Environment Setup',
                        'duration': '1 week',
                        'topics': [
                            'Introduction to C++', 
                            'Setting up the Development Environment',
                            'Compiling and Running Your First Program',
                            'Basic Syntax and Structure'
                        ],
                        'exercises': ['Hello World program', 'Simple calculator'],
                        'resources': ['C++ Reference', 'Compiler documentation']
                    },
                    {
                        'title': 'Variables and Data Types',
                        'duration': '1 week',
                        'topics': [
                            'Basic Data Types', 
                            'Variables and Constants',
                            'Type Conversion and Casting',
                            'Operators and Expressions'
                        ],
                        'exercises': ['Temperature converter', 'Simple arithmetic calculations'],
                        'resources': ['C++ Primer', 'Online tutorials']
                    },
                    {
                        'title': 'Control Structures',
                        'duration': '2 weeks',
                        'topics': [
                            'Conditional Statements (if, else, switch)', 
                            'Loops (for, while, do-while)',
                            'Break and Continue',
                            'Nested Control Structures'
                        ],
                        'exercises': ['Number guessing game', 'Pattern printing', 'Simple menu system'],
                        'resources': ['C++ Control Flow tutorials', 'Practice problems']
                    },
                    {
                        'title': 'Functions and Scope',
                        'duration': '2 weeks',
                        'topics': [
                            'Function Declaration and Definition', 
                            'Parameters and Return Values',
                            'Pass by Value vs. Pass by Reference',
                            'Function Overloading',
                            'Variable Scope and Lifetime'
                        ],
                        'exercises': ['Calculator with functions', 'Array processing functions'],
                        'resources': ['C++ Function reference', 'Practice problems']
                    },
                    {
                        'title': 'Arrays, Vectors, and Strings',
                        'duration': '2 weeks',
                        'topics': [
                            'Arrays and Their Limitations', 
                            'Introduction to STL and Vectors',
                            'String Handling',
                            'Common String Operations'
                        ],
                        'exercises': ['Word counter', 'Simple text processor', 'Vector manipulation'],
                        'resources': ['C++ STL documentation', 'Practice projects']
                    },
                    {
                        'title': 'Object-Oriented Programming Basics',
                        'duration': '2 weeks',
                        'topics': [
                            'Classes and Objects', 
                            'Constructors and Destructors',
                            'Access Specifiers',
                            'Encapsulation'
                        ],
                        'exercises': ['Bank account class', 'Student record system'],
                        'resources': ['OOP in C++ books', 'Object design patterns']
                    },
                    {
                        'title': 'Inheritance and Polymorphism',
                        'duration': '2 weeks',
                        'topics': [
                            'Inheritance Basics', 
                            'Types of Inheritance',
                            'Virtual Functions',
                            'Polymorphism',
                            'Abstract Classes and Interfaces'
                        ],
                        'exercises': ['Shape hierarchy implementation', 'Employee management system'],
                        'resources': ['Advanced C++ programming resources']
                    },
                ],
                'milestones': [
                    {'week': 1, 'assessment': 'Basic C++ syntax and compilation quiz'},
                    {'week': 4, 'assessment': 'Control structures and functions project'},
                    {'week': 8, 'assessment': 'Arrays and OOP basics implementation'},
                    {'week': 12, 'assessment': 'Final C++ project combining all concepts'}
                ]
            }
        else:
            return {
                'title': 'Advanced C++ Programming',
                'estimated_completion_time': '16 weeks',
                'units': [
                    {'title': 'Advanced C++ Features', 'duration': '2 weeks'},
                    {'title': 'Memory Management and Smart Pointers', 'duration': '2 weeks'},
                    {'title': 'STL Deep Dive', 'duration': '3 weeks'},
                    {'title': 'Templates and Generic Programming', 'duration': '2 weeks'},
                    {'title': 'Exception Handling', 'duration': '1 week'},
                    {'title': 'Multithreading and Concurrency', 'duration': '3 weeks'},
                    {'title': 'Design Patterns in C++', 'duration': '3 weeks'},
                ],
                'milestones': [
                    {'week': 4, 'assessment': 'Advanced features implementation'},
                    {'week': 8, 'assessment': 'STL and templates project'},
                    {'week': 12, 'assessment': 'Multithreaded application development'},
                    {'week': 16, 'assessment': 'Final project with design patterns'}
                ]
            }
    
    def create_cbse_class6_history_roadmap(self):
        """Create a specific roadmap for Class 6 CBSE History."""
        return {
            'title': 'History for Class 6 CBSE',
            'estimated_completion_time': '4 months',
            'units': [
                {
                    'title': 'What, Where, How and When?',
                    'duration': '2 weeks',
                    'topics': [
                        'Introduction to History', 
                        'Sources of History',
                        'Timeline and Historical Periods',
                        'Early Civilizations'
                    ],
                    'exercises': ['Timeline creation', 'Source identification exercise'],
                    'resources': ['NCERT Textbook Ch. 1', 'Historical maps and timelines']
                },
                {
                    'title': 'From Hunting-Gathering to Growing Food',
                    'duration': '2 weeks',
                    'topics': [
                        'Paleolithic Age', 
                        'Mesolithic Age',
                        'Neolithic Age',
                        'Development of Agriculture'
                    ],
                    'exercises': ['Stone tool identification', 'Early settlement mapping'],
                    'resources': ['NCERT Textbook Ch. 2', 'Documentary: Early Humans']
                },
                {
                    'title': 'The Earliest Cities',
                    'duration': '3 weeks',
                    'topics': [
                        'Indus Valley Civilization', 
                        'Harappa and Mohenjo-Daro',
                        'Town Planning and Architecture',
                        'Trade and Economy'
                    ],
                    'exercises': ['Harappan city layout model', 'Artifact analysis'],
                    'resources': ['NCERT Textbook Ch. 3', 'Indus Valley virtual tour']
                },
                {
                    'title': 'What Books and Burials Tell Us',
                    'duration': '2 weeks',
                    'topics': [
                        'Vedic Literature', 
                        'Burial Practices',
                        'Megalithic Structures',
                        'Early Religious Practices'
                    ],
                    'exercises': ['Vedic literature chart', 'Burial types comparison'],
                    'resources': ['NCERT Textbook Ch. 4', 'Archaeological evidence resources']
                },
                {
                    'title': 'Kingdoms, Kings and an Early Republic',
                    'duration': '2 weeks',
                    'topics': [
                        'Janapadas and Mahajanapadas', 
                        'Rise of Kingdoms',
                        'Early Republics',
                        'Social Structure'
                    ],
                    'exercises': ['Map of 16 Mahajanapadas', 'Monarchy vs republic comparison'],
                    'resources': ['NCERT Textbook Ch. 5', 'Political systems in ancient India']
                },
                {
                    'title': 'New Questions and Ideas',
                    'duration': '2 weeks',
                    'topics': [
                        'Rise of Buddhism', 
                        'Rise of Jainism',
                        'Upanishadic Teachings',
                        'Social Reform Movements'
                    ],
                    'exercises': ['Buddhism vs Jainism chart', 'Timeline of philosophical thought'],
                    'resources': ['NCERT Textbook Ch. 6', 'Buddhist and Jain literature']
                },
                {
                    'title': 'Ashoka: The Emperor Who Gave Up War',
                    'duration': '2 weeks',
                    'topics': [
                        'Mauryan Empire', 
                        'Ashoka\'s Conquest of Kalinga',
                        'Ashoka\'s Dhamma',
                        'Edicts and Pillars'
                    ],
                    'exercises': ['Ashoka\'s pillar edict analysis', 'Mauryan empire map'],
                    'resources': ['NCERT Textbook Ch. 7', 'Ashokan inscriptions']
                },
                {
                    'title': 'Vital Villages, Thriving Towns',
                    'duration': '2 weeks',
                    'topics': [
                        'Iron Age Villages', 
                        'Urban Centers',
                        'Crafts and Trade',
                        'Coinage Systems'
                    ],
                    'exercises': ['Village vs town comparison chart', 'Craft documentation'],
                    'resources': ['NCERT Textbook Ch. 8', 'Ancient trade routes map']
                },
                {
                    'title': 'Traders, Kings and Pilgrims',
                    'duration': '2 weeks',
                    'topics': [
                        'Trade Routes', 
                        'Rise of New Kingdoms',
                        'Travels of Pilgrims',
                        'Cultural Exchange'
                    ],
                    'exercises': ['Silk route mapping', 'Pilgrim diary creation'],
                    'resources': ['NCERT Textbook Ch. 9', 'Ancient trade networks']
                },
                {
                    'title': 'New Empires and Kingdoms',
                    'duration': '2 weeks',
                    'topics': [
                        'Gupta Empire', 
                        'Samudragupta and Chandragupta II',
                        'Harsha\'s Empire',
                        'South Indian Kingdoms'
                    ],
                    'exercises': ['Empire comparison chart', 'Golden Age research'],
                    'resources': ['NCERT Textbook Ch. 10', 'Gupta period art and science']
                },
                {
                    'title': 'Buildings, Paintings and Books',
                    'duration': '3 weeks',
                    'topics': [
                        'Temple Architecture', 
                        'Stupa Architecture',
                        'Cave Paintings',
                        'Literature and Science'
                    ],
                    'exercises': ['Temple design elements', 'Ajanta cave art study'],
                    'resources': ['NCERT Textbook Ch. 11', 'Virtual tour of ancient monuments']
                }
            ],
            'milestones': [
                {'week': 4, 'assessment': 'Early civilization and prehistoric period quiz'},
                {'week': 8, 'assessment': 'Indus Valley and Early Vedic period project'},
                {'week': 14, 'assessment': 'Buddhism, Jainism, and Mauryan empire test'},
                {'week': 20, 'assessment': 'Gupta period and ancient architecture final project'}
            ]
        }
    
    def create_generic_history_roadmap(self, level):
        """Create a general history roadmap based on the level."""
        if level == "beginner":
            return {
                'title': 'Introduction to Historical Studies',
                'estimated_completion_time': '12 weeks',
                'units': [
                    {'title': 'Understanding Historical Sources', 'duration': '2 weeks'},
                    {'title': 'Ancient Civilizations', 'duration': '3 weeks'},
                    {'title': 'Medieval Period', 'duration': '3 weeks'},
                    {'title': 'Modern History', 'duration': '3 weeks'},
                    {'title': 'Historical Analysis Methods', 'duration': '1 week'}
                ],
                'milestones': [
                    {'week': 2, 'assessment': 'Source analysis exercise'},
                    {'week': 5, 'assessment': 'Ancient civilization project'},
                    {'week': 8, 'assessment': 'Medieval period test'},
                    {'week': 11, 'assessment': 'Modern history comparison'},
                    {'week': 12, 'assessment': 'Final historical analysis paper'}
                ]
            }
        else:
            return {
                'title': 'Advanced Historical Studies',
                'estimated_completion_time': '16 weeks',
                'units': [
                    {'title': 'Historiography', 'duration': '2 weeks'},
                    {'title': 'Specialized Historical Research', 'duration': '3 weeks'},
                    {'title': 'Comparative Historical Analysis', 'duration': '3 weeks'},
                    {'title': 'Historical Interpretation', 'duration': '4 weeks'},
                    {'title': 'Contemporary Historical Methods', 'duration': '4 weeks'}
                ],
                'milestones': [
                    {'week': 2, 'assessment': 'Historiographical review'},
                    {'week': 5, 'assessment': 'Research methodology paper'},
                    {'week': 8, 'assessment': 'Comparative analysis project'},
                    {'week': 12, 'assessment': 'Interpretation critique'},
                    {'week': 16, 'assessment': 'Original historical research paper'}
                ]
            }
    
    def create_python_beginner_roadmap(self):
        """Create a roadmap for Python beginners."""
        return {
            'title': 'Python Programming for Beginners',
            'estimated_completion_time': '8 weeks',
            'units': [
                {
                    'title': 'Python Basics',
                    'duration': '1 week',
                    'topics': [
                        'Installing Python', 
                        'Variables and Data Types',
                        'Basic Operators',
                        'Control Structures'
                    ],
                    'exercises': ['Simple calculator program', 'Temperature converter'],
                    'resources': ['Python.org documentation', 'Interactive tutorials']
                },
                # ... other Python units ...
            ],
            'milestones': [
                {'week': 2, 'assessment': 'Basic Python skills quiz'},
                {'week': 4, 'assessment': 'Data processing project review'},
                {'week': 6, 'assessment': 'Django application review'},
                {'week': 8, 'assessment': 'Final project presentation'}
            ]
        }
    
    def create_cbse_math_roadmap(self, class_level):
        """Create a CBSE Math roadmap for the given class level."""
        # Simplified implementation for example purposes
        return {
            'title': f'Mathematics for Class {class_level} CBSE',
            'estimated_completion_time': '4 months',
            'units': [
                {'title': 'Number Systems', 'duration': '3 weeks'},
                {'title': 'Algebra', 'duration': '3 weeks'},
                {'title': 'Geometry', 'duration': '3 weeks'},
                {'title': 'Mensuration', 'duration': '2 weeks'},
                {'title': 'Data Handling', 'duration': '2 weeks'},
                {'title': 'Practical Applications', 'duration': '3 weeks'}
            ],
            'milestones': [
                {'week': 3, 'assessment': 'Number systems test'},
                {'week': 6, 'assessment': 'Algebra quiz'},
                {'week': 9, 'assessment': 'Geometry project'},
                {'week': 11, 'assessment': 'Mensuration and data handling assessment'},
                {'week': 16, 'assessment': 'Final comprehensive exam'}
            ]
        }
    
    def create_cbse_science_roadmap(self, class_level):
        """Create a CBSE Science roadmap for the given class level."""
        # Simplified implementation for example purposes
        return {
            'title': f'Science for Class {class_level} CBSE',
            'estimated_completion_time': '4 months',
            'units': [
                {'title': 'Food and Nutrition', 'duration': '2 weeks'},
                {'title': 'Materials', 'duration': '2 weeks'},
                {'title': 'The World of Living', 'duration': '3 weeks'},
                {'title': 'Moving Things', 'duration': '2 weeks'},
                {'title': 'Natural Phenomena', 'duration': '3 weeks'},
                {'title': 'Natural Resources', 'duration': '2 weeks'},
                {'title': 'Practical Science', 'duration': '2 weeks'}
            ],
            'milestones': [
                {'week': 4, 'assessment': 'Food and materials test'},
                {'week': 7, 'assessment': 'Living organisms project'},
                {'week': 9, 'assessment': 'Movement and force quiz'},
                {'week': 12, 'assessment': 'Natural phenomena demonstration'},
                {'week': 16, 'assessment': 'Final science project and exam'}
            ]
        }
    
    def generate_custom_roadmap_with_llm(self, purpose):
        """Generate a custom roadmap using OpenAI API based on student's purpose."""
        try:
            subject = purpose['subject']
            level = purpose['level']
            learning_style = purpose['learning_style']
            time_commitment = purpose['time_commitment']
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Create a detailed learning roadmap with learning units, topics, exercises, resources and milestones for the given subject, level, learning style and time commitment."},
                    {"role": "user", "content": f"Subject: {subject}\nLevel: {level}\nLearning style: {learning_style}\nTime commitment: {time_commitment}"}
                ],
                temperature=0.7
            )
            
            # This is a simplified approach - in a real system you would parse the structured output
            content = response.choices[0].message.content
            
            # Simple parsing attempt - this would be more sophisticated in a real implementation
            title_match = re.search(r'Title:\s*(.*)', content)
            title = title_match.group(1) if title_match else f"{subject} Learning Path"
            
            time_match = re.search(r'Estimated.*?:\s*(.*)', content)
            estimated_time = time_match.group(1) if time_match else "12 weeks"
            
            # Create a simple roadmap structure
            roadmap = {
                'title': title,
                'estimated_completion_time': estimated_time,
                'units': [],
                'milestones': []
            }
            
            # Extract units section (simplified)
            units_section = re.search(r'Units:(.*?)Milestones:', content, re.DOTALL)
            if units_section:
                units_text = units_section.group(1)
                unit_blocks = re.findall(r'(\d+\.\s.*?)(?=\d+\.\s|Milestones:)', units_text + "Milestones:", re.DOTALL)
                
                for block in unit_blocks:
                    unit_title_match = re.search(r'\d+\.\s+(.*?)(?:\n|$)', block)
                    unit_title = unit_title_match.group(1) if unit_title_match else "Learning Unit"
                    
                    duration_match = re.search(r'Duration:\s*(.*?)(?:\n|$)', block)
                    duration = duration_match.group(1) if duration_match else "2 weeks"
                    
                    unit = {
                        'title': unit_title,
                        'duration': duration,
                        'topics': []
                    }
                    
                    # Try to extract topics
                    topics_match = re.search(r'Topics:(.*?)(?:Exercises:|$)', block, re.DOTALL)
                    if topics_match:
                        topics_text = topics_match.group(1)
                        topics = re.findall(r'-\s+(.*?)(?:\n|$)', topics_text)
                        unit['topics'] = topics if topics else ["Topic 1", "Topic 2", "Topic 3"]
                    
                    roadmap['units'].append(unit)
            
            # If no units were found, create some default ones
            if not roadmap['units']:
                roadmap['units'] = [
                    {'title': 'Fundamentals', 'duration': '3 weeks', 'topics': ['Basic concepts', 'Core principles', 'Foundations']},
                    {'title': 'Intermediate Concepts', 'duration': '3 weeks', 'topics': ['Building on basics', 'Practical applications', 'Problem solving']},
                    {'title': 'Advanced Topics', 'duration': '3 weeks', 'topics': ['Specialized knowledge', 'Integration of concepts', 'Advanced techniques']},
                    {'title': 'Mastery', 'duration': '3 weeks', 'topics': ['Real-world application', 'Projects', 'Self-directed learning']}
                ]
            
            # Create some milestones
            roadmap['milestones'] = [
                {'week': 3, 'assessment': 'Fundamentals assessment'},
                {'week': 6, 'assessment': 'Intermediate concepts project'},
                {'week': 9, 'assessment': 'Advanced topics quiz'},
                {'week': 12, 'assessment': 'Final comprehensive assessment'}
            ]
            
            return roadmap
        
        except Exception as e:
            print(f"Error generating custom roadmap with LLM: {e}")
            return self.create_generic_roadmap(purpose)
    
    def create_generic_roadmap(self, purpose):
        """Create a generic roadmap based on purpose."""
        return {
            'title': f'{purpose["subject"]} Learning Path',
            'estimated_completion_time': '8 weeks',
            'units': [
                {'title': 'Fundamentals', 'duration': '2 weeks', 'topics': ['Basic concepts', 'Core principles', 'Foundations']},
                {'title': 'Core Concepts', 'duration': '2 weeks', 'topics': ['Key ideas', 'Central theories', 'Main applications']},
                {'title': 'Advanced Topics', 'duration': '2 weeks', 'topics': ['Complex concepts', 'Specialized knowledge', 'In-depth analysis']},
                {'title': 'Practical Application', 'duration': '2 weeks', 'topics': ['Real-world use', 'Projects', 'Problem solving']}
            ],
            'milestones': [
                {'week': 2, 'assessment': 'Fundamentals quiz'},
                {'week': 4, 'assessment': 'Core concepts project'},
                {'week': 6, 'assessment': 'Advanced topics assessment'},
                {'week': 8, 'assessment': 'Final project'}
            ]
        }
    
    def adjust_roadmap(self, student_id, evaluation_data):
        """Adjust the roadmap based on student's learning evaluation."""
        # Get the student's current roadmap
        student_data = self.get_student_context(student_id)
        
        if 'roadmap' not in student_data:
            return {
                'status': 'error',
                'message': 'No existing roadmap to adjust.'
            }
        
        current_roadmap = student_data['roadmap']
        
        # In a real implementation, this would analyze the evaluation data
        # and make intelligent adjustments to the roadmap
        # For demonstration purposes, we'll make some sample adjustments
        
        # Example: If the student struggled with a particular unit, extend its duration
        adjusted_roadmap = current_roadmap.copy()
        
        # Simulate finding a unit the student struggled with
        if 'difficult_topics' in evaluation_data:
            for unit in adjusted_roadmap['units']:
                for topic in evaluation_data['difficult_topics']:
                    if 'topics' in unit and any(topic.lower() in t.lower() for t in unit['topics']):
                        # Extend the duration and add extra resources
                        original_duration = unit['duration']
                        duration_value = int(original_duration.split()[0])
                        unit['duration'] = f"{duration_value + 1} {original_duration.split()[1]}"
                        unit['resources'] = unit.get('resources', []) + ['Additional practice exercises', 'Simplified tutorials']
        
        # Store the adjusted roadmap
        self.update_student_context(student_id, {'roadmap': adjusted_roadmap})
        
        # Record this adjustment session
        self.record_session(student_id, 'roadmap_adjustment', {
            'evaluation_data': evaluation_data,
            'previous_roadmap': current_roadmap,
            'adjusted_roadmap': adjusted_roadmap
        })
        
        return {
            'status': 'adjusted',
            'previous_roadmap': current_roadmap,
            'adjusted_roadmap': adjusted_roadmap
        }