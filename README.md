<!-- !pip install google-adk
!pip install --upgrade google-adk -->

from googlesearch import search
from google.adk.agents import LlmAgent

dice_agent = LlmAgent(
model="gemini-2.0-flash-exp", # Required: Specify the LLM
name="question_answer_agent", # Requdired: Unique agent name
description="A helpful assistant agent that can answer questions.",
instruction="""Respond to the query using google search""",
tools=[search], # Provide an instance of the tool
)

<!-- !adk web -->

User : [ 6 th -> Board ( CBSE ) : [ Roadmap : Roadmap , follow ] ]

Project : Ai tutor.
make sure to store all the contexts into a mondo db, so that we have trak of learnings of student at all the stages.

- Purpose : it will ask the student about his purpose, basically why he want the ai tutor. This will be stored in db, a mongodb will work. create a mcp to add data to mongo db.
- Roadmap : this agent will create a raodmap for the student for the purpose.
- Lessons : this agent will generate lessons for the roadmap.
- Exam manager : once student completed learning leassons, this agent will ask the student questions based on the leassons.
- Evaluate learning : on the basis of exam, this agent will evaluate the student, his learning and how this student is learning, basically students learning behaviour will be analysed.
- Roadmap adjust : based on the students learning behavior the road map can be adjustted, like more time to some lessons which studnet is finding diffcult.
- Revesion Agent based on user learning evaluation.
- Exam manager2 : Based on the timeline, this exam manager will conduct mock exams to analyse the students strengeths and weakness
- Evaluate learning : based on the results of exam manager 2 the student will be guided to do best in examingations.
