"""Phase 2 mock workspace file: a Level 0 hardcoded prompt with zero
validation, tests, or logging. The eval-flywheel skill should diagnose
this as Level 0 and recommend a Level 2 (Subroutine Compilation) scaffold.

Not skill code. Used by evals/phase2-grader.py as input to the agent.
"""
import openai


def translate_to_spanish(text):
    prompt = f"Translate this text to Spanish: {text}"
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(translate_to_spanish("Hello, world!"))
