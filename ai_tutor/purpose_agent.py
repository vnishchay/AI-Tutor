from ai_tutor.base_agent import BaseTutorAgent
import openai
import re
import os

class PurposeAgent(BaseTutorAgent):
    """Agent responsible for determining the student's learning purpose."""
    
    def __init__(self):
        """Initialize the Purpose Agent."""
        super().__init__(
            agent_name="purpose_agent",
            description="An agent that determines student's learning goals and objectives",
            instruction="""
            You are an AI educational counselor tasked with understanding a student's learning goals.
            Ask thoughtful questions to determine:
            
            1. What specific subject or skill they want to learn
            2. Their current knowledge level in this area (beginner, intermediate, advanced)
            3. Their motivation for learning this subject
            4. Their preferred learning style (visual, reading, interactive exercises, etc.)
            5. Their available time commitment (hours per day/week)
            6. Any specific goals or outcomes they hope to achieve
            
            Be empathetic, encouraging, and ask follow-up questions to get detailed information.
            Summarize their purpose concisely at the end of the conversation.
            """
        )
        # Ensure OpenAI API key is set
        if os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def determine_purpose(self, student_id, initial_query=None):
        """Determine the student's learning purpose through conversation."""
        # Get any existing information about the student
        student_data = self.get_student_context(student_id)
        
        # If the student already has a purpose defined, return it
        if 'purpose' in student_data:
            return {
                'status': 'existing',
                'purpose': student_data['purpose']
            }
        
        # Start the conversation to determine purpose
        messages = []
        
        # Add the initial query if provided
        if initial_query:
            messages.append({
                'role': 'user',
                'content': initial_query
            })
        else:
            messages.append({
                'role': 'user',
                'content': "I'd like to learn something new. Can you help me figure out what I need?"
            })
        
        # Parse the initial query to determine the purpose
        determined_purpose = self.extract_purpose_from_query(initial_query)
        
        # Store the purpose in the database
        self.update_student_context(student_id, {'purpose': determined_purpose})
        
        # Record this session
        self.record_session(student_id, 'purpose_determination', {
            'messages': messages,
            'determined_purpose': determined_purpose
        })
        
        return {
            'status': 'determined',
            'purpose': determined_purpose
        }
    
    def extract_purpose_from_query(self, query):
        """Extract learning purpose details from the user's query."""
        if not query:
            return self.get_default_purpose()
            
        # Use OpenAI to extract purpose information from the query
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract learning purpose details from the student's query. Provide a JSON structure with subject, level, motivation, learning_style, time_commitment, and specific_goals fields."},
                    {"role": "user", "content": f"Student query: {query}"}
                ],
                temperature=0.3
            )
            
            # Try to parse the result as a structured purpose
            content = response.choices[0].message.content
            
            # Extract subject
            subject_match = re.search(r'"subject"\s*:\s*"([^"]+)"', content)
            subject = subject_match.group(1) if subject_match else self.extract_subject_from_query(query)
            
            # Extract level - default to beginner if not specified
            level_match = re.search(r'"level"\s*:\s*"([^"]+)"', content)
            level = level_match.group(1) if level_match else "beginner"
            
            # Extract or set defaults for other fields
            motivation_match = re.search(r'"motivation"\s*:\s*"([^"]+)"', content)
            motivation = motivation_match.group(1) if motivation_match else "Personal interest"
            
            learning_style_match = re.search(r'"learning_style"\s*:\s*"([^"]+)"', content)
            learning_style = learning_style_match.group(1) if learning_style_match else "Mixed approach"
            
            time_commitment_match = re.search(r'"time_commitment"\s*:\s*"([^"]+)"', content)
            time_commitment = time_commitment_match.group(1) if time_commitment_match else "3-5 hours per week"
            
            goals_match = re.search(r'"specific_goals"\s*:\s*"([^"]+)"', content)
            specific_goals = goals_match.group(1) if goals_match else f"Master the basics of {subject}"
            
            return {
                'subject': subject,
                'level': level,
                'motivation': motivation,
                'learning_style': learning_style,
                'time_commitment': time_commitment,
                'specific_goals': specific_goals
            }
            
        except Exception as e:
            print(f"Error extracting purpose: {e}")
            # Fallback to direct subject extraction
            return {
                'subject': self.extract_subject_from_query(query),
                'level': 'beginner',
                'motivation': 'Personal interest',
                'learning_style': 'Mixed approach',
                'time_commitment': '3-5 hours per week',
                'specific_goals': f'Learn the fundamentals'
            }
    
    def extract_subject_from_query(self, query):
        """Extract the subject directly from the query if possible."""
        if not query:
            return "General knowledge"
            
        # Look for common patterns like "I want to learn X" or "Help me with X"
        if "learn" in query.lower():
            parts = query.lower().split("learn")
            if len(parts) > 1 and parts[1].strip():
                return parts[1].strip().capitalize()
                
        # Check for explicit subject mentions
        subject_keywords = ["history", "math", "science", "english", "physics", "chemistry", 
                           "biology", "programming", "geography", "computer", "art", "c++",
                           "cbse", "class"]
                           
        for keyword in subject_keywords:
            if keyword in query.lower():
                # If we find "class X" try to extract the full subject
                if keyword == "class" or keyword == "cbse":
                    # Extract the whole query as it likely contains the subject with class info
                    return query.strip()
                return keyword.capitalize()
        
        # Default if we can't determine
        return query.strip() if query.strip() else "General knowledge"
    
    def get_default_purpose(self):
        """Return a default purpose if none could be determined."""
        return {
            'subject': 'General knowledge',
            'level': 'beginner',
            'motivation': 'Personal interest',
            'learning_style': 'Mixed approach',
            'time_commitment': '2-3 hours per week',
            'specific_goals': 'Build a foundation of knowledge'
        }