"""Run local English sentiment inference with a licensed Hugging Face model.

This is an original CLI wrapper around Transformers' pipeline API; it does
not copy the upstream model's source code or redistribute model weights.
On first run, Transformers downloads the model from the Hub and caches it.
"""
from __future__ import annotations

import argparse

from transformers import pipeline

MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Classify a short English text as positive or negative using "
            "the publicly hosted DistilBERT SST-2 model."
        )
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="English text to classify; quote it if it contains spaces.",
    )
    args = parser.parse_args()
    text = " ".join(args.text)

    classifier = pipeline(
        task="text-classification",
        model=MODEL_ID,
    )
    result = classifier(text, truncation=True)[0]

    print(f"Model: {MODEL_ID}")
    print(f"Label: {result['label']}")
    print(f"Score: {result['score']:.4f}")
    print(
        "Note: this score is the model's output score, not a calibrated "
        "real-world probability. This model is intended for English sentiment "
        "classification and may perform poorly on other languages, sarcasm, "
        "mixed sentiment, or out-of-domain text."
    )


if __name__ == "__main__":
    main()
