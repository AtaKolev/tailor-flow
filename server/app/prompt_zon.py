import os
import openai
import json
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("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")

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
        "based on Big Five Inventory, short version (BFI-10) and am working as " + curr_work +
        "I am looking for a personalised learning path to become" + desired_work + " that contains courses and would be suitable for both my personality type and my career goals. Focus on my personality type and adjust the courses accordingly "
        "Create a step by step guide."
    )
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Parse response and validate using Pydantic
    try:
        response_data = json.loads(response.choices[0].text)
        transition = Transition(**response_data)
        
        # Save response to file
        with open("test.txt", "w") as f:
            f.write(json.dumps(transition.dict(), indent=2))
        
        # Print response
        print(transition.json(indent=2))

    except Exception as e:
        print(f"Error parsing response: {e}")
