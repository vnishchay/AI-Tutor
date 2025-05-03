import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set the API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}.",
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}

def process_query(query: str) -> str:
    """Process user query using OpenAI's API.

    Args:
        query (str): The user's question about weather or time.

    Returns:
        str: The response to the user's query.
    """
    # Define the available functions
    functions = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "get_current_time",
            "description": "Get the current time for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        }
    ]

    # Create the chat completion
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can tell the weather and time for cities. Currently, you only have data for New York."},
            {"role": "user", "content": query}
        ],
        functions=functions,
        function_call="auto"
    )

    # Get the response message
    message = response.choices[0].message

    # If the model wants to call a function
    if message.function_call:
        function_name = message.function_call.name
        function_args = eval(message.function_call.arguments)
        
        # Call the appropriate function
        if function_name == "get_weather":
            result = get_weather(function_args["city"])
        elif function_name == "get_current_time":
            result = get_current_time(function_args["city"])
        
        # Return the result
        if result["status"] == "success":
            return result["report"]
        else:
            return result["error_message"]
    
    # If no function call, return the model's response
    return message.content

if __name__ == "__main__":
    # Example usage
    while True:
        query = input("Ask about weather or time (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        response = process_query(query)
        print(f"\nResponse: {response}\n")