OFF_TOPIC_KEYWORDS = [
    "weather",
    "cricket",
    "football",
    "movie",
    "song",
    "restaurant",
    "python tutorial",
    "java code",
    "legal",
    "medical"
]


def is_off_topic(query: str):

    query = query.lower()

    return any(word in query for word in OFF_TOPIC_KEYWORDS)


def refusal_message():

    return (
        "I'm designed to assist only with SHL assessments and "
        "assessment selection."
    )