from app.conversation import (
    extract_state,
    need_clarification,
)

messages = [
    {
        "role": "user",
        "content": "Hiring Java developer"
    },
    {
        "role": "assistant",
        "content": "Experience?"
    },
    {
        "role": "user",
        "content": "Mid level with personality assessment"
    }
]

state = extract_state(messages)

print(state)

print()

print(need_clarification(state))