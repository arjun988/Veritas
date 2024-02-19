import pandas as pd
import numpy as np
import joblib
#import gradio as gr
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('anomaly.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract the date and time components
df['date'] = df['timestamp'].dt.date
df['time'] = df['timestamp'].dt.time

lab = LabelEncoder()
df['target1'] = lab.fit_transform(df['target1'])
df['target2'] = lab.fit_transform(df['target2'])
df['target3'] = lab.fit_transform(df['target3'])
df['target4'] = lab.fit_transform(df['target4'])

# Drop unnecessary columns
df.drop(columns=['timestamp', 'date', 'time', '_id'], inplace=True)

# Define features (X) and target variables (Y)
X = df[['insert', 'delete', 'update', 'access', 'invalid_access', 'corruption_file', 'sensitive_data_masking']]
Y1 = df['target1']
Y2 = df['target2']
Y3 = df['target3']
Y4 = df['target4']

# Train Decision Tree Classifier for each target variable
clf1 = DecisionTreeClassifier()
clf1.fit(X, Y1)

clf2 = DecisionTreeClassifier()
clf2.fit(X, Y2)

clf3 = DecisionTreeClassifier()
clf3.fit(X, Y3)

clf4 = DecisionTreeClassifier()
clf4.fit(X, Y4)

# Save the trained models to files
joblib.dump(clf1, 'decision_tree_model1.joblib')
joblib.dump(clf2, 'decision_tree_model2.joblib')
joblib.dump(clf3, 'decision_tree_model3.joblib')
joblib.dump(clf4, 'decision_tree_model4.joblib')