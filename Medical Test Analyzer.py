import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import re

# Simulated medical knowledge database for common test types
medical_knowledge = {
    "Glucose": {
        "low_threshold": 70,
        "high_threshold": 100,
        "recommendation_low": "Your glucose level is low. Consider consuming more sugars and carbs.",
        "recommendation_normal": "Your glucose level is normal. Maintain a balanced diet.",
        "recommendation_high": "Your glucose level is high. Reduce sugar intake and monitor your health."
    },
    "Cholesterol": {
        "low_threshold": 120,
        "high_threshold": 200,
        "recommendation_low": "Cholesterol is low. Consult your doctor for diet recommendations.",
        "recommendation_normal": "Cholesterol level is normal. Maintain a healthy diet.",
        "recommendation_high": "Cholesterol is high. Avoid fatty foods and consult a doctor."
    },
    # Add more test types here like Blood Pressure, Hemoglobin, etc.
}

# Function to extract text from a PDF medical report
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)  # Convert PDF to images (for OCR)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)  # Use OCR to extract text
    return text

# Function to process medical test data
def analyze_test_results(text, medical_knowledge):
    extracted_data = {}
    
    # Extract test values using regular expressions
    glucose_match = re.search(r'Glucose\s*:\s*(\d+)', text)
    cholesterol_match = re.search(r'Cholesterol\s*:\s*(\d+)', text)
    
    if glucose_match:
        glucose_value = int(glucose_match.group(1))
        extracted_data['Glucose'] = glucose_value
    if cholesterol_match:
        cholesterol_value = int(cholesterol_match.group(1))
        extracted_data['Cholesterol'] = cholesterol_value

    # Generate recommendations based on the test results
    recommendations = []
    for test_name, value in extracted_data.items():
        if test_name in medical_knowledge:
            test_info = medical_knowledge[test_name]
            if value < test_info['low_threshold']:
                recommendations.append(test_info['recommendation_low'])
            elif test_info['low_threshold'] <= value <= test_info['high_threshold']:
                recommendations.append(test_info['recommendation_normal'])
            else:
                recommendations.append(test_info['recommendation_high'])
    
    return extracted_data, recommendations

# Example usage of the system
def medical_test_analyzer(pdf_path):
    # Step 1: Extract text from the report
    report_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Analyze test results and generate recommendations
    test_results, recommendations = analyze_test_results(report_text, medical_knowledge)
    
    # Step 3: Display the results
    print("Medical Test Results:")
    for test, result in test_results.items():
        print(f"{test}: {result}")
    
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec}")

# Provide the path to the PDF report for analysis
pdf_path = "path_to_medical_report.pdf"
medical_test_analyzer(pdf_path)
