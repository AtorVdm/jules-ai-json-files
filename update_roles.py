import json
import uuid
import random

# Load roles
with open('app_roles/roles/data.json', 'r') as f:
    roles_data = json.load(f)
role_ids = list(roles_data.keys())

# Load role assignments
with open('app_roles/role_assignments/data.json', 'r') as f:
    assignments_data = json.load(f)

# Add 99 new human assignments
for _ in range(99):
    new_uuid = str(uuid.uuid4())
    random_role_id = random.choice(role_ids)

    # If role is not in assignments, add it
    if random_role_id not in assignments_data:
        assignments_data[random_role_id] = {"humans": {}}

    # Add human to role
    assignments_data[random_role_id]["humans"][new_uuid] = {}

# Write updated assignments back to file
with open('app_roles/role_assignments/data.json', 'w') as f:
    json.dump(assignments_data, f, indent=2)

print("Successfully added 99 new human role assignments.")
