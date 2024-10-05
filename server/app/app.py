import csv
import datetime
import subprocess
import os
import pickle
import requests
from typing import List
from fpdf import FPDF
from sklearn.cluster import KMeans
import pandas as pd
from flask import Flask, request, render_template, url_for, redirect
import numpy as np

################################################################################################################
# APP VARIABLES
################################################################################################################
app = Flask(__name__, static_url_path='/static', static_folder='static')



# Constants for CSV file path
app.REPO_PATH = "https://github.com/AtaKolev/tailor-flow/blob/main"
app.LOCAL_CSV_PATH = r"D:\Repositories\tailor-flow\server\app\data\data.csv"
app.PKL_MODEL_PATH = "model.pkl"
app.OPENAI_API_URL = "https://api.openai.com/v1/completions"
app.OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your API key
app.CLUSTER_DICTIONARY = {
    0 : 'High Extraversion, Low Agreeableness, Low Conscientiousness, Medium Neuroticism, Medium Openness',
    1 : 'Medium Extraversion, Low Agreeableness, High Conscientiousness, Medium Neuroticism, High Openness',
    2 : 'Medium Extraversion, High Agreeableness, Medium Conscientiousness, High Neuroticism, High Openness',
    3 : 'High Extraversion, High Agreeableness, High Conscientiousness, Low Neuroticism, High Openness',
    4 : 'Low Extraversion, Medium Agreeableness, High Conscientiousness, High Neuroticism, Low Openness'
}
app.F_COLS = ['Q_1', 'Q_2', 'Q_3', 'Q_4', 'Q_5', 'Q_6', 'Q_7', 'Q_8', 'Q_9', 'Q_10']
app.REVERSED_QUESTIONS = ['Q_1', 'Q_2', 'Q_3', 'Q_4', 'Q_5']



class BackendApp:
    def __init__(self):
        self.model = None

    # Function to validate if an array is valid
    # Need frontend connection here
    def validFrontEndArray(self, array: List[int]) -> List[int]:
        # receive array from frontend here
        if all(isinstance(i, int) and 0 <= i <= 4 for i in array):
            return array
        else:
            raise ValueError("Array contains invalid elements. Only integers between 0-4 are allowed.")

    # Function to create a desires object
    # Need frontend connection here
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
        response = requests(app.REPO_PATH)
        if response.status_code == 200:
            with open(app.LOCAL_CSV_PATH, 'w') as file:
                file.write(response.text)
        else:
            raise Exception("Failed to pull CSV from repository.")

    # Function to push the CSV data file to GitHub repo (stub for versioning and repository interaction)
    def pushDataCSV():
        try:
            subprocess.run(["git", "add", "data.csv"], check=True)
            subprocess.run(["git", "commit", "-m", "updated data.csv file"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"Successfully pushed data.csv to the repository.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def processReversedQuestions(data):
        data[app.REVERSED_QUESTIONS] = data[app.REVERSED_QUESTIONS].apply(lambda col: 6 - col)
        return data

    def _fitModel(self, model):
        data = pd.read_csv('data.csv')
        data = self.processReversedQuestions(data)
        X = data[app.F_COLS]
        model.fit(X)

        return model

    # Function to load and integrate ML model
    def loadEvalML(self):
        kmeans = KMeans(n_clusters=5, random_state=42)
        self.model = self._fitModel(kmeans)

    def evaluateArray(self, array):
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
        with open(app.LOCAL_CSV_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(array)

    # Helper function to get the last ID from CSV
    def getLastIDFromCSV(self) -> int:
        try:
            with open(app.LOCAL_CSV_PATH, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:
                    return int(rows[-1][1])
                else:
                    return 0
        except FileNotFoundError:
            return 0

    # Function to make REST call to OpenAI API
    # Models and details need attention
    def callChatGPT(self, prompt: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {app.OPENAI_API_KEY}'
        }
        data = {
            'model': 'text-davinci-003',
            'prompt': prompt,
            'max_tokens': 100
        }
        response = requests.post(app.OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('choices', [{}])[0].get('text', '').strip()
        else:
            raise Exception("Failed to fetch response from OpenAI API.")

    # Function to create PDF from ChatGPT response
    # Logo needed here + visuals testing
    def chatGPTWrapper(self, response: str) -> str:
        pdf = FPDF()
        pdf.add_page()
        # Example: pdf.image('logo.png', x=10, y=8, w=33)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=response, ln=True)
        pdf_file_path = "chatgpt_response.pdf"
        pdf.output(pdf_file_path)
        
        return pdf_file_path

    # Function to send PDF to frontend
    # Front end connection w flask needed here
    def sendPdfFront(filename):
        try:
            return send_file(filename, as_attachment=False)
        except Exception as e:
            return str(e)
        
    def updateData(arr):
        whole_df = pd.read_csv(app.LOCAL_CSV_PATH)
        new_id = whole_df.iloc[-1, 1] + 1 
        df_row = {'Date' : [f"0{datetime.today().day}/{datetime.today().month}/{datetime.today().year}"],
                'ID' : [new_id]}
        for i, ele in enumerate(arr):
            df_row.update({f'Q_{i+1}' : [ele]})
        whole_df = pd.concat((whole_df, pd.DataFrame(df_row)), axis = 0).reset_index(drop=True)
        pd.to_csv(app.LOCAL_CSV_PATH, index = False)
        


        
be_obj = BackendApp()

################################################################################################################
# ENDPOINTS
################################################################################################################
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the form data from the 'career-form' input
        boxes = request.form.getlist('career-form')
        if len(boxes) >= 2:  # Ensure there are at least 2 items submitted
            app.desired_role = str(boxes[0])
            app.skills_needed = str(boxes[1])

        # Redirect to the 'survey' route after processing the form
        return redirect(url_for('survey'))
    else:
        # Render the home page with the form
        return render_template('index.html')

@app.route('/survey.html', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        try:
            answers = [
                int(request.form['q1']),
                int(request.form['q2']),
                int(request.form['q3']),
                int(request.form['q4']),
                int(request.form['q5']),
                int(request.form['q6']),
                int(request.form['q7']),
                int(request.form['q8']),
                int(request.form['q9']),
                int(request.form['q10'])
            ]
            answers_array = np.array(answers)
            answers_array[:5] = 6 - answers_array[:5]
            if be_obj.model is None:
                be_obj.loadEvalML()
                cluster = be_obj.evaluateArray(answers_array)
            else:
                cluster = be_obj.evaluateArray(answers_array)
            be_obj.updateData(answers_array)
            app.psycho_eval = app.CLUSTER_DICTIONARY[cluster]
            
        except KeyError as e:
            # Handle missing keys if any question was left unanswered
            return f"Missing answer for {str(e)}"
        
        return 
    else:
        # Handle GET request for the survey page
        return render_template('survey.html')

# Example usage
if __name__ == '__main__':
    app.run(debug=True)
