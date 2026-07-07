def main():
    print("Hello from mcp-gradio-tutor!")


if __name__ == "__main__":
    main()
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = "gpt-4o-mini"

EXPLANATION_LEVELS= {
1:"like I'm 5 years old",
2:"like I'm 10 years old",
3:"like a high school student",
4:"like a college student",
5:"like an expert in the field",
}

def explain_concept(question: str, level: int):
    """
    Stream an explanation of a concept based on
    the student's learning level.
    """

    # Check if the user entered a question
    if not question.strip():
        yield "Error: Question cannot be blank."
        return

    # Convert number into description
    level_desc = EXPLANATION_LEVELS.get(
        level,
        "clearly and concisely"
    )

    # System Prompt
    system_prompt = (
        f"You are a helpful AI Tutor. "
        f"Explain the following concept {level_desc}."
    )

    # Call OpenAI
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        stream=True,
        temperature=0.7,
    )

    partial = ""

    for chunk in stream:

        delta = getattr(
            chunk.choices[0].delta,
            "content",
            None,
        )

        if delta:

            partial += delta

            yield partial

if __name__ == "__main__":
    example_question = "What is photosynthesis?"
    example_level = 3
    explanation_generator = explain_concept(example_question, example_level)
    for explanation in explanation_generator:
        print(explanation)

