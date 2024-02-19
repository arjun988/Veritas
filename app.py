import numpy as np
import joblib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request
import gradio as gr

# Reverse mapping dictionaries
reverse_mapping_target1 = {
    0: 'bulk_deletion',
    1: 'clean_data',
    2: 'corruption_file',
    3: 'credential_misuse',
    4: 'sensitive_data_masking'
}

reverse_mapping_target2 = {
    0: 'clean_data',
    1: 'corruption_file',
    2: 'credential_misuse',
    3: 'sensitive_data_masking'
}

reverse_mapping_target3 = {
    0: 'clean_data',
    1: 'corruption_file',
    2: 'sensitive_data_masking'
}

reverse_mapping_target4 = {
    0: 'clean_data',
    1: 'sensitive_data_masking'
}

# Load the trained models
model1 = joblib.load('decision_tree_model1.joblib')
model2 = joblib.load('decision_tree_model2.joblib')
model3 = joblib.load('decision_tree_model3.joblib')
model4 = joblib.load('decision_tree_model4.joblib')

# Email configuration
EMAIL_ADDRESS = "arjunwork85@gmail.com"
EMAIL_PASSWORD = "Arjun@123"  # Update with your email password

def send_email(subject, message, recipient_email):
    try:
        # Setup the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Update with your SMTP server and port
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
        return True
    except Exception as e:
        print("Email sending failed:", str(e))
        return False

def predict_anomaly(insert, delete, update, access, invalid_access, corruption_file, sensitive_data_masking, recipient_email):
    # Create input array
    input_data = np.array([[insert, delete, update, access, invalid_access, corruption_file, sensitive_data_masking]])
    
    # Make predictions using each model and apply reverse mapping
    prediction1 = reverse_mapping_target1[model1.predict(input_data)[0]]
    prediction2 = reverse_mapping_target2[model2.predict(input_data)[0]]
    prediction3 = reverse_mapping_target3[model3.predict(input_data)[0]]
    prediction4 = reverse_mapping_target4[model4.predict(input_data)[0]]
    
    # Send email notification
    subject = "Anomaly Prediction Results"
    message = f"Target 1: {prediction1}\nTarget 2: {prediction2}\nTarget 3: {prediction3}\nTarget 4: {prediction4}"
    email_sent = send_email(subject, message, recipient_email)
    
    return prediction1, prediction2, prediction3, prediction4, email_sent

# Create Gradio interface
iface = gr.Interface(
    fn=predict_anomaly,
    inputs=[
        gr.Number(label="Insert"),
        gr.Number(label="Delete"),
        gr.Number(label="Update"),
        gr.Number(label="Access"),
        gr.Number(label="Invalid Access"),
        gr.Number(label="Corruption File"),
        gr.Number(label="Sensitive Data Masking"),
        gr.Textbox(label="Recipient Email", lines=1)
    ],
    outputs=[
        gr.Text(label="Target 1"),
        gr.Text(label="Target 2"),
        gr.Text(label="Target 3"),
        gr.Text(label="Target 4"),
        gr.Text(label="Email Sent")
    ],
    title="Anomaly Prediction",
    description="Enter the values for different features to predict anomalies and your email address to receive the results."
)

# Launch the interface
iface.launch(share=True)
