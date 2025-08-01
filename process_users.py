import json
import uuid
import os

def collect_and_generate_uuids():
    # Define the list of data.json files to process
    data_files = [
        "app_roles/role_assignments/data.json",
        "resource_types/developer_account/resource_assignments/data.json",
        "resource_types/merchant/resource_assignments/data.json",
        "resource_types/merchant_account/resource_assignments/data.json",
        "resource_types/scope/resource_assignments/data.json"
    ]

    # Initialize a set to store all unique human UUIDs
    human_uuids = set()

    # Load existing users from users.json
    try:
        with open("users.json", 'r') as f:
            users_data = json.load(f)
            if "humans" in users_data and isinstance(users_data["humans"], list):
                human_uuids.update(users_data["humans"])
    except (FileNotFoundError, json.JSONDecodeError):
        users_data = {"humans": []}

    # Process each data file
    for file_path in data_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for key in data:
                    if "humans" in data[key] and isinstance(data[key]["humans"], dict):
                        human_uuids.update(data[key]["humans"].keys())
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading or parsing {file_path}: {e}")

    # Generate new UUIDs until the total count is 5000
    while len(human_uuids) < 5000:
        human_uuids.add(str(uuid.uuid4()))

    # Update the users.json file
    users_data["humans"] = sorted(list(human_uuids))
    with open("users.json", 'w') as f:
        json.dump(users_data, f, indent=2)

    print(f"Total number of users in users.json: {len(users_data['humans'])}")

if __name__ == "__main__":
    collect_and_generate_uuids()
