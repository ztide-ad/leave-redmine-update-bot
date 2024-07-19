from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

form_structure = {
    "formId_url": "https://docs.google.com/forms/d/e/1FAIpQLSepBTbfwHsFCHOa4-p7wsbwC5WOTJaRBp32joacBIFwyPlCxw/formResponse",
    "form_data": {
        "entry.737578346": "days",
        "entry.726687366": "reason",
        "entry.89965788": "type"
    }
}

@app.route('/form', methods=['GET'])
def get_form():
    return jsonify(form_structure)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    form_data = form_structure["form_data"]
    mapped_data = {
        key: data[value] for key, value in form_data.items()
    }
    response = requests.post(form_structure["formId_url"], data=mapped_data)
    if response.status_code == 200:
        return jsonify({"message": "Form submitted successfully"}), 200
    else:
        return jsonify({"message": f"Error submitting form: {response.content}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

