import xml.etree.ElementTree as ET

# Function to parse AndroidManifest.xml
def Run(file_path, output_file):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Android XML namespaces
        namespace = {'android': 'http://schemas.android.com/apk/res/android'}

        exported_components = {
            'activities': [],
            'services': [],
            'receivers': []
        }

        permissions = []

        # Analyze components
        for component_type in ['activity', 'service', 'receiver']:
            for component in root.findall(f".//{component_type}"):
                exported = component.get(f"{{{namespace['android']}}}exported")
                if exported == 'true':
                    component_name = component.get(f"{{{namespace['android']}}}name")
                    if component_name:
                        exported_components[component_type + 's'].append(component_name)

        # Get all permissions in readable format
        for permission in root.findall('uses-permission'):
            permission_name = permission.get(f"{{{namespace['android']}}}name")
            if permission_name:
                permissions.append(permission_name)

        # Write the results to a file
        with open(output_file, 'w') as f:
            f.write("=== Exported Components ===\n")
            
            f.write("\nActivities (exported=true):\n")
            if exported_components['activities']:
                f.writelines(f"- {activity}\n" for activity in exported_components['activities'])
            else:
                f.write("No exported activities found.\n")
            
            f.write("\nServices (exported=true):\n")
            if exported_components['services']:
                f.writelines(f"- {service}\n" for service in exported_components['services'])
            else:
                f.write("No exported services found.\n")

            f.write("\nReceivers (exported=true):\n")
            if exported_components['receivers']:
                f.writelines(f"- {receiver}\n" for receiver in exported_components['receivers'])
            else:
                f.write("No exported receivers found.\n")

            f.write("\n=== Permissions ===\n")
            if permissions:
                f.writelines(f"- {permission}\n" for permission in permissions)
            else:
                f.write("No permissions found.\n")

        print(f"Analysis saved to {output_file}")

    except Exception as e:
        print(f"Error analyzing manifest file: {e}")