from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['a1']
collection = db['a1_logs']

# Function to generate random operation data
def generate_operation_data():
    operations = ['insert', 'delete', 'update', 'access', 'invalid_access']
    targets = ['bulk_deletion', 'sensitive_data_masking', 'credential_misuse', 
               'datafile_corruption', 'clean_data']

    operation_data = []
    current_time = datetime.now()

    for _ in range(10000):
        # Generate random values for operations
        insert = random.randint(0, 100)
        delete = random.randint(0, 100)
        update = random.randint(0, 100)
        access = random.randint(0, 100)
        invalid_access = random.randint(0, 100)
        corruption_file = random.randint(0, 100)
        sensitive_data_masking = random.randint(0, 100)

        # Thresholds for deletion, invalid access, corruption file, and sensitive data masking operations
        deletion_threshold = 30
        invalid_access_threshold = 10
        corruption_file_threshold = 5
        sensitive_data_masking_threshold = 10

        # Determine the target values based on the values of the remaining fields and thresholds
        target1 = 'bulk_deletion' if delete > deletion_threshold else ''
        target2 = 'credential_misuse' if invalid_access > invalid_access_threshold else ''
        target3 = 'corruption_file' if corruption_file > corruption_file_threshold else ''
        target4 = 'sensitive_data_masking' if sensitive_data_masking > sensitive_data_masking_threshold else ''

        # Assign the values to the target columns based on their priority
        target_values = [target1, target2, target3, target4]

        # Remove empty strings from target_values list
        target_values = [target for target in target_values if target]

        # If all values are below their thresholds, assign clean_data to the first target
        if not target_values:
            target_values.append('clean_data')

        # Fill the remaining target columns with clean_data
        while len(target_values) < 4:
            target_values.append('clean_data')

        operation_data.append({
            "timestamp": current_time,
            "insert": insert,
            "delete": delete,
            "update": update,
            "access": access,
            "invalid_access": invalid_access,
            "corruption_file": corruption_file,
            "sensitive_data_masking": sensitive_data_masking,
            "target1": target_values[0],
            "target2": target_values[1],
            "target3": target_values[2],
            "target4": target_values[3],
        })

        # Increment current_time for next entry
        current_time += timedelta(minutes=1)  # Assuming each entry is one minute apart

    return operation_data

# Generate operation data
operation_data = generate_operation_data()

# Insert operation data into the MongoDB collection
collection.insert_many(operation_data)

# Close MongoDB connection
client.close()
