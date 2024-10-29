import openai

def Run(file_path, follow_up_question):
    # Initialize OpenAI API with your key
    openai.api_key = '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'

    # Step 1: Read the contents of the file
    def read_file(file_path):
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
            return file_contents
        except FileNotFoundError:
            return "File not found."

    # Step 2: Send file contents and a follow-up question to OpenAI's GPT-4 using the correct API format
    def send_to_gpt4(file_contents, follow_up_question):
        prompt = f"Here is the content of a file:\n\n{file_contents}\n\nFollow-up question: {follow_up_question}"

        try:
            # Using the 'openai.completions.create' with prompt instead of messages
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # Use GPT-4 here
                prompt=prompt,  # Pass the full prompt (file content + follow-up question)
                max_tokens=2000,  # Limit response length
                temperature=0.7  # Adjust the creativity level of the response
            )
            
            return response['choices'][0]['text']  # Access the response text
        
        except Exception as e:
            return f"Error: {e}"

    # Step 3: Run the script
    file_contents = read_file(file_path)

    if file_contents != "File not found.":
        gpt4_response = send_to_gpt4(file_contents, follow_up_question)
        print(f"GPT-4 Response:\n{gpt4_response}")
    else:
        print(file_contents)
