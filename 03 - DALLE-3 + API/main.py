import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API key. Make sure it is set in the .env file.")


if __name__ == '__main__':

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Predefined styles
    styles = [
        "in the style of a watercolor painting",
        "in a futuristic sci-fi style",
        "in the style of impressionist art",
        "in the style of surrealism",
        "as a comic book illustration",
        "as a pencil sketch",
        "in a pixel art style",
        "in a minimalist abstract art style",
        "in a hyper-realistic digital painting style"
    ]

    # New, interesting base prompt
    base_prompt = "A majestic dragon soaring over a futuristic city at sunset"

    # List to store generated image metadata
    generated_images = []

    # Loop through each style and generate an image
    for style in styles:
        prompt = f"{base_prompt}, {style}"
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,  # Generate one image per style
            size="1024x1024"
        )
        # Store the response for each style
        generated_images.append({
            "style": style,
            "response": response
        })

    # Display the generated images and styles
    for idx, img_data in enumerate(generated_images, 1):
        print(f"Image {idx} ({img_data['style']}): {img_data['response']}")
