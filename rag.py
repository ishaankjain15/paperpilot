
from pathlib import Path

import pandas as pd

BANK_PATH = Path(__file__).with_name("question_bank.csv")


def retrieve_questions(
    class_name,
    subject,
    chapters=None,
    limit=8,
):
    """Retrieve matching questions from the local question bank."""

    if not BANK_PATH.exists():
        return []

    bank = pd.read_csv(BANK_PATH)

    required = {
        "class", "subject", "chapter", "marks", "question"
    }
    if not required.issubset(bank.columns):
        raise ValueError(
            "question_bank.csv must contain: "
            + ", ".join(sorted(required))
        )

    # Normalize values to make matching more reliable.
    bank["class"] = bank["class"].astype(str).str.strip()
    bank["subject"] = bank["subject"].astype(str).str.strip().str.lower()
    bank["chapter"] = bank["chapter"].astype(str).str.strip().str.lower()

    results = bank[
        (bank["class"] == str(class_name).strip())
        & (bank["subject"] == str(subject).strip().lower())
    ]

    if chapters:
        wanted = {str(ch).strip().lower() for ch in chapters}
        results = results[results["chapter"].isin(wanted)]

    limit = max(0, int(limit))
    return results.head(limit)["question"].dropna().tolist()
