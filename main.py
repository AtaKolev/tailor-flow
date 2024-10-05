import csv
import datetime
import os
import pickle
import requests
from typing import List
from fpdf import FPDF

# Constants for CSV file path
CSV_REPO_PATH = "https://github.com/AtaKolev/tailor-flow/blob/main/data.csv"
LOCAL_CSV_PATH = "data.csv"
PKL_MODEL_PATH = "model.pkl"
OPENAI_API_URL = "https://api.openai.com/v1/completions"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your API key


class BackendApp:
    def __init__(self):
        self.model = None

    # Function to validate if an array is valid
    def validFrontEndArray(self, array: List[int]) -> List[int]:
        # receive array from frontend here
        if all(isinstance(i, int) and 0 <= i <= 4 for i in array):
            return array
        else:
            raise ValueError("Array contains invalid elements. Only integers between 0-4 are allowed.")

    # Function to create a desires object
    def getDesires(self, desires: List[str]) -> dict:
        # receive desires from frontend here
        if len(desires) != 2:
            raise ValueError("Desires array must contain exactly two strings.")
        return {
            'position': desires[0],
            'skillset': desires[1]
        }

    # Function to pull the CSV data file from GitHub repo
    def pullDataCSV(self):
        response = requests.get(CSV_REPO_PATH)
        if response.status_code == 200:
            with open(LOCAL_CSV_PATH, 'w') as file:
                file.write(response.text)
        else:
            raise Exception("Failed to pull CSV from repository.")

    # Function to push the CSV data file to GitHub repo (stub for versioning and repository interaction)
    def pushDataCSV(self):
        # Assuming authentication and Git interaction will be implemented
        raise NotImplementedError("CSV push functionality to be implemented.")

    # Function to load and integrate ML model
    def loadEvalML(self):
        with open(PKL_MODEL_PATH, 'rb') as model_file:
            self.model = pickle.load(model_file)

    def evaluateArray(self, array: List[int]) -> int:
        if self.model is None:
            raise Exception("ML model not loaded. Call loadEvalML() first.")
        # Assuming the model takes an array and returns an integer
        return self.model.predict([array])[0]

    # Function to create an array with 13 elements
    def createArray(self, frontend_array: List[int]) -> List:
        today_date = datetime.datetime.now().strftime("%d/%m/%Y")
        last_id = self.getLastIDFromCSV()
        new_id = last_id + 1
        ml_result = self.evaluateArray(frontend_array)
        return [
            today_date,
            new_id,
            *frontend_array[:10],
            ml_result
        ]

    # Function to add a row to the CSV file
    def addRowToData(self, array: List):
        with open(LOCAL_CSV_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(array)

    # Helper function to get the last ID from CSV
    def getLastIDFromCSV(self) -> int:
        try:
            with open(LOCAL_CSV_PATH, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:
                    return int(rows[-1][1])
                else:
                    return 0
        except FileNotFoundError:
            return 0

    # Function to make REST call to OpenAI API
    def callChatGPT(self, prompt: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        data = {
            'model': 'text-davinci-003',
            'prompt': prompt,
            'max_tokens': 100
        }
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('choices', [{}])[0].get('text', '').strip()
        else:
            raise Exception("Failed to fetch response from OpenAI API.")

    # Function to create PDF from ChatGPT response
    def chatGPTWrapper(self, response: str):
        pdf = FPDF()
        pdf.add_page()
        # put logo here
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=response, ln=True)
        pdf.output("chatgpt_response.pdf")

    # Function to send PDF to frontend
    def sendPdfFront(self):
        # send to frontend here
        pass


# Example usage
if __name__ == "__main__":
    backend = BackendApp()   
    fArray = backend.validFrontEndArray()#get the array from frontend
    fDesires = backend.getDesires()#get the desires array from frontend
    csvData = backend.pullDataCSV()
    backend.loadEvalML()
    newRow = backend.addRowToData(backend.createArray(fArray))
    backend.addRowToData(newRow)
