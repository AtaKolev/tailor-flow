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
def get_personalized_learning_path(persType, curr_work, desired_work, desired_skills):
    print(persType)
    prompt = (
    f"I am a {persType} based on Big Five Inventory, short version (BFI-10), and I am currently working as a {curr_work}. "
    f"I am looking for a personalized learning path to transition to {desired_work} and learn the following skills: {desired_skills}. "
    "Please create a detailed, step-by-step learning path that is suitable for both my personality type and my career goals. "
    "For each step, include the following structure:\n"
    "- Step number and title\n"
    "- A brief description of the step and why it is important\n"
    "- A course recommendation\n"
    "- A clickable link to the course\n"
    "- An explanation of why the course fits my personality traits, but without directly mentioning the personality traits themselves\n"
    "Do not explicitly reference my personality type in the suggestions. Begin your response immediately with the steps formatted like this:\n\n"
    "Step X: [Title]\n"
    "[Description]\n"
    "Course: [Course Name]\n"
    "Link: [Course URL]\n"
    "Why this course fits: [Brief explanation of why the course fits the personality type and career goals]\n\n"
    "This format will help visualize the learning path in the frontend. "
    "Be concise and practical in your suggestions."
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
        
        # Print the raw response for debugging purposes
        print("Raw response from model:", response_message)
        
        # Save the raw response to a .txt file
        with open("learning_path.txt", "w") as f:
            f.write(response_message)
        
        # Inform the user that the response was saved
        print("Learning path has been saved to 'learning_path.txt'")
        # Save response to file
       
        
        # Print response
    except json.JSONDecodeError as e:
        print(f"Error parsing response as JSON: {e}")
        print(f"Raw response: {response_message}")
    except Exception as e:
        print(f"General error: {e}")
