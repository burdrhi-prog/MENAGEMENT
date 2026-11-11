"""MENAGEMENT v0.1: local-only, human-reviewed message triage."""
from dataclasses import asdict, dataclass
import argparse
import json
import re

@dataclass
class Result:
    level: int
    category: str
    reason: str
    suggestions: list[str]
    review_required: bool = True

RESPONSES = {
    0: ["I'm not comfortable with that. Please respect my boundaries.", "I'd rather not continue this conversation.", "I'm going to end this conversation here."],
    1: ["Hey! How's your day going?", "Hi! Tell me something interesting about yourself.", "Hey, what caught your attention on my profile?"],
    2: ["That's a good question! What about you?", "I appreciate you asking. What made you curious?", "Interesting! I'd like to hear your take first."],
    3: ["I appreciate the thoughtful message. I'd love to hear more.", "You made an interesting point. What led you to that?", "Thanks for taking the time to write that. Here's what I think…"],
}

def classify(message: str) -> Result:
    """Heuristic triage, not a judgment about a person or their intentions."""
    msg = message.strip()
    if not msg:
        raise ValueError("Please provide a message to review.")
    lower = msg.lower()
    if re.search(r"\b(send (me )?(nudes|pics)|you owe me|stupid bitch|shut up bitch)\b", lower):
        level, category, reason = 0, "boundary review", "Potential boundary concern in the wording; check context yourself."
    elif len(msg.split()) >= 24 and ("?" in msg or any(w in lower for w in ("because", "noticed", "appreciate"))):
        level, category, reason = 3, "thoughtful", "Longer message with detail or a question."
    elif "?" in msg or len(msg.split()) >= 10:
        level, category, reason = 2, "conversational", "Question or substantive opening."
    else:
        level, category, reason = 1, "brief", "Short opening with limited detail."
    return Result(level, category, reason, RESPONSES[level].copy())

def main() -> None:
    parser = argparse.ArgumentParser(description="MENAGEMENT local message triage")
    parser.add_argument("message", nargs="?", help="Message to classify (or enter when prompted)")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    message = args.message if args.message is not None else input("Paste a message: ")
    try:
        result = classify(message)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Level {result.level} — {result.category}\n{result.reason}\n")
        for i, reply in enumerate(result.suggestions, 1):
            print(f"{i}. {reply}")
        print("\nHuman review required. Nothing has been sent or saved.")

if __name__ == "__main__":
    main()
