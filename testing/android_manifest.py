import xml.etree.ElementTree as ET

# Function to parse AndroidManifest.xml and analyze it
def Run(file_path, output_file):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Android namespace
        namespace = {'android': 'http://schemas.android.com/apk/res/android'}

        # Dictionary to store the exported components
        exported_components = {
            'activities': [],
            'services': [],
            'receivers': []
        }

        # List to store permissions
        permissions = []

        # Helper function to get the value of an attribute from the Android namespace
        def get_android_attribute(element, attribute):
            return element.get(f"{{{namespace['android']}}}{attribute}")

        # Analyze the exported components (activities, services, receivers)
        for component_type in ['activity', 'service', 'receiver']:
            for component in root.findall(f".//{component_type}"):
                exported = get_android_attribute(component, 'exported')
                if exported == 'true':
                    component_name = get_android_attribute(component, 'name')
                    if component_name:
                        if component_type == 'activity':
                            exported_components['activities'].append(component_name)
                        else:
                            exported_components[component_type + 's'].append(component_name)

        # Analyze permissions
        for permission in root.findall('uses-permission'):
            permission_name = get_android_attribute(permission, 'name')
            if permission_name:
                permissions.append(permission_name)

        # Write the analysis to the output file
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

    except ET.ParseError as parse_err:
        print(f"Error parsing XML: {parse_err}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"Unexpected error: {e}")
