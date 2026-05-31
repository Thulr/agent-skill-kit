"""Phase 3 mock workspace file: a Level 0 hardcoded prompt for support-
ticket classification. TEST_PLAN.md Phase 3 copies this into
test-sandbox/src/classifier.py, then the skill is invoked to scaffold an
ai-ops/ directory containing a Level 2 DSPy compiler loop.

Not skill code. Used by evals/integration-test.sh.
"""
import openai


def classify_ticket(ticket_text):
    prompt = f"Classify this support ticket as BUG, FEATURE, or BILLING: {ticket_text}"
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(classify_ticket("My credit card was charged twice for the same order."))
