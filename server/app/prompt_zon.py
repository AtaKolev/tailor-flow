import os
import openai
import json
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set OpenAI API key
openai.api_key = "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"

# Define Pydantic models for schema validation
class Resource(BaseModel):
    title: str
    url: str

class Step(BaseModel):
    title: str
    description: str
    resources: Optional[List[Resource]] = []

class Transition(BaseModel):
    title: str
    description: str
    steps: List[Step]

# Generate personalized learning path
def get_personalized_learning_path(persType,curr_work,desired_work,desired_skills):
    prompt = (
        "I am a " + persType +
        "based on Big Five Inventory, short version (BFI-10) and am working as a" + curr_work +
        "I am looking for a personalised learning path to become " + desired_work +
        " that contains courses and would be suitable for both my personality type and my career goals. "
        "Focus on my personality type and adjust the courses accordingly "
        "Create a step by step guide."
        "Don't directly mention the personality types in the suggestions."
        "Include links to each course."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates learning paths."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # Parse response and validate using Pydantic
    try:
        response_message = response['choices'][0]['message']['content']
        #response_data = json.loads(response_message)  # Assuming the model returns a valid JSON
        #transition = Transition(**response_data)
        
        # Print the raw response for debugging purposes
        print("Raw response from model:", response_message)
        
        # Save the raw response to a .txt file
        with open("learning_path.txt", "w") as f:
            f.write(response_message)
        
        # Inform the user that the response was saved
        print("Learning path has been saved to 'learning_path.txt'")
        # Save response to file
        #with open("test.txt", "w") as f:
        #    f.write(json.dumps(transition.dict(), indent=2))
        
        # Print response
        #print(transition.json(indent=2))

    except json.JSONDecodeError as e:
        print(f"Error parsing response as JSON: {e}")
        print(f"Raw response: {response_message}")
    except Exception as e:
        print(f"General error: {e}")
