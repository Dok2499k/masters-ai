import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API key. Make sure it is set in the .env file.")


if __name__ == '__main__':

    client = OpenAI(api_key=api_key)

    try:
        # Initial conversation: Setting up the context
        initial_completion = client.chat.completions.create(
            model="gpt-4o",  # Correct model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": "Can you write a blogpost? I will provide you text directly or with .txt file."}
            ]
        )

        print("Assistant's Reply:")
        print(initial_completion.choices[0].message.content)

        file_path = "lesson-1-transcript.txt"  # Replace with actual file path
        if not os.path.exists(file_path):
            print(f"\nFile {file_path} does not exist. Please check the file path.")
        else:
            with open(file_path, 'r') as file:
                blog_text = file.read()

        # Generate the blog post based on the provided content
        second_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": "Can you write a blogpost? I will provide you text directly or with .txt file."},
                {"role": "assistant", "content": initial_completion.choices[0].message.content},
                {"role": "user", "content": f"Here is the text: {blog_text}"}
            ]
        )

        print("\nGenerated Blog Post:")
        print(second_completion.choices[0].message.content)

    except Exception as e:
        print(f"An error occurred: {e}")