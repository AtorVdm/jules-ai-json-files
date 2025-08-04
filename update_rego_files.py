import json
import re
import random

def update_rego_files():
    # Read the scopes from the data.json file
    with open('resource_types/scope/resources/data.json', 'r') as f:
        data = json.load(f)

    # Generate the content for scopes.rego
    rego_items = []
    for item in data.values():
        rego_item = f"""\
\t{{
\t\t"id": "{item['technical_id']}",
\t\t"name": "{item['display_name']}",
\t}},"""
        rego_items.append(rego_item)

    # The last item should not have a trailing comma.
    if rego_items:
        rego_items[-1] = rego_items[-1][:-1]

    rego_content = "package scopes\n\nassignable_scopes := [\n" + "\n".join(rego_items) + "\n]"

    # Write the new content to scopes.rego
    with open('scopes.rego', 'w') as f:
        f.write(rego_content)

    # Read the roles from map.rego
    with open('map.rego', 'r') as f:
        map_rego_content = f.read()

    roles = re.findall(r'"([^"]+)":\s*\[', map_rego_content)
    scope_ids = list(data.keys())

    # Distribute scopes to roles
    role_scopes = {role: [] for role in roles}
    for scope in scope_ids:
        role = random.choice(roles)
        role_scopes[role].append(scope)

    # Generate new map.rego content
    new_map_rego_content = "package map\n\nrole_to_scope_map := {\n"
    for i, (role, scopes) in enumerate(role_scopes.items()):
        new_map_rego_content += f'\t# {role.lower().replace("_", " ")}\n'
        new_map_rego_content += f'\t"{role}": [\n'
        for scope in scopes:
            new_map_rego_content += f'\t\t"{scope}",\n'
        new_map_rego_content += '\t]'
        if i < len(role_scopes) - 1:
            new_map_rego_content += ',\n'
        else:
            new_map_rego_content += '\n'
    new_map_rego_content += "}"

    # Write the new content to map.rego
    with open('map.rego', 'w') as f:
        f.write(new_map_rego_content)

if __name__ == '__main__':
    update_rego_files()
