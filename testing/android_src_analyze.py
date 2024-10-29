import os
import re

# Predefined search patterns for easy use
def get_predefined_patterns():
    return {
        'Class Declarations': r'\bclass\b',  # Pattern for 'class' keyword
        'Method Declarations': r'\b(public|private|protected)\s+\w+\s+\w+\(',  # Pattern for method declarations
        'TODO Comments': r'//\s*TODO',  # Pattern for finding TODO comments
        'System.out.println': r'System\.out\.println',  # Pattern for System.out.println
        'Main Method': r'\bpublic\s+static\s+void\s+main\b',  # Pattern for main method
    }

def get_patterns():
    return {
        'GetIntent': r'\.getIntent\(',
        'GetParcelable': r'\.getParcelable\(',
        'GetParcelableExtra': r'\.getParcelableExtra\(',
        'startActivity': r'\.startActivity\(',
        # Additional Vulnerable Patterns
        'startService': r'\.startService\(',  # Can start services, check for permission
        'bindService': r'\.bindService\(',    # Can bind services, check for permission
        'startForegroundService': r'\.startForegroundService\(',  # Permission-sensitive
        'startActivityForResult': r'\.startActivityForResult\(',  # Can leak unfiltered data
        'startIntentSenderForResult': r'\.startIntentSenderForResult\(',  # Can be hijacked
        'PendingIntent.getActivity': r'PendingIntent\.getActivity\(',  # Potential for hijacking
        'PendingIntent.getService': r'PendingIntent\.getService\(',
        'PendingIntent.getBroadcast': r'PendingIntent\.getBroadcast\(',
        'setComponent': r'\.setComponent\(',  # Can set the component target, check for hijacking
        'addJavascriptInterface': r'\.addJavascriptInterface\(',  # Exposes methods to JavaScript
        'WebView.loadUrl': r'WebView\.loadUrl\(',  # Risk of untrusted content injection
        'getExternalStorageDirectory': r'Environment\.getExternalStorageDirectory\(',  # Sensitive data risk
        'openFileOutput': r'\.openFileOutput\(',  # Check for secure storage
        'execute': r'\.execute\(',  # Common in AsyncTask, check for encrypted data
        'onReceivedSslError': r'\.onReceivedSslError\(',  # Must handle SSL errors securely
        'getSystemService': r'\.getSystemService\(',  # Exposes sensitive APIs, check for permission validation
        'query': r'\.query\(',  # For content querying, ensure permission and input validation
        'insert': r'\.insert\(',
        'update': r'\.update\(',
        'delete': r'\.delete\(',
        'loadLibrary': r'System\.loadLibrary\(',  # Check for untrusted library loading
        'MODE_WORLD_READABLE': r'MODE_WORLD_READABLE',  # Insecure file mode
        'MODE_WORLD_WRITEABLE': r'MODE_WORLD_WRITEABLE',  # Insecure file mode
    }



def Run(source_directory, patterns, output_file):
    # Function to recursively get all Java files
    def get_java_files(directory):
        java_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        return java_files

    # Function to search for specific patterns in a file
    def search_code_in_file(file_path, patterns):
        file_results = {pattern_name: [] for pattern_name in patterns}
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, start=1):
                for pattern_name, pattern_regex in patterns.items():
                    if re.search(pattern_regex, line):
                        file_results[pattern_name].append((line_num, line.strip()))
        return file_results

    # Function to write analysis results to an output file in a structured format
    def write_analysis_results(results, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            for pattern_name, file_matches in results.items():
                f.write(f"======== {pattern_name} ========\n")
                for file_path, matches in file_matches.items():
                    if matches:
                        f.write(f"\nFile: {file_path}\n")
                        for line_num, line in matches:
                            f.write(f"  Line {line_num}: {line}\n")
                f.write("\n")  # Blank line between different patterns

    # Main analysis function
    def analyze_java_code(directory, patterns, output_file):
        java_files = get_java_files(directory)
        overall_results = {pattern_name: {} for pattern_name in patterns}

        for java_file in java_files:
            file_results = search_code_in_file(java_file, patterns)
            for pattern_name, matches in file_results.items():
                if matches:
                    overall_results[pattern_name][java_file] = matches

        write_analysis_results(overall_results, output_file)
        print(f"Analysis complete. Results written to {output_file}")

    analyze_java_code(source_directory, patterns, output_file)
