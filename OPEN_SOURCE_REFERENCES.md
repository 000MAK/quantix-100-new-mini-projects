# Open-Source References & Attribution

This portfolio contains original demonstration code and links to external projects and pretrained assets. Third-party code, model weights, datasets, and documentation are **not represented as my own work**. Before redistributing or adapting any upstream material, check the exact repository/model-card license, notices, and any use restrictions.

## Model used by the Hugging Face sentiment demo

### DistilBERT fine-tuned on SST-2

- Model: https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english
- Purpose: English text sentiment classification (positive/negative)
- Listed license: Apache-2.0, as shown on the model card at the time this reference was checked
- Base model: DistilBERT
- Fine-tuning dataset: SST-2
- Used by this repository in: ml-dl-lab/huggingface_sentiment.py
- Usage: the script calls the public model through the Transformers API; it does not bundle or re-upload model weights.

Review the upstream model card and applicable notices before commercial use or redistribution. This model is English-focused and is not a general-purpose moderation, truthfulness, or emotion-detection system.

## Libraries and learning references

- scikit-learn — https://github.com/scikit-learn/scikit-learn — machine-learning library; upstream repository lists the BSD-3-Clause license. Used by the lab's classification and clustering examples.
- Transformers — https://github.com/huggingface/transformers — library used to load and run the sentiment model; follow the license and notices in the upstream repository.
- LLMs-from-scratch — https://github.com/rasbt/LLMs-from-scratch — educational reference for understanding language-model implementations. Its repository includes an Apache License 2.0 file. This portfolio links to it for further study and does not copy its code.

## Attribution and change policy

- The source code in this portfolio is written as original glue code and educational examples.
- Model authorship, model weights, upstream libraries, and dataset provenance remain with their respective authors and owners.
- If a future project copies or modifies upstream code, its exact source, license, required copyright notices, and modifications must be documented in that project's files.
- A license field is useful information but is not, by itself, a substitute for reviewing the complete license, model card, dataset terms, and any applicable usage restrictions.
- No upstream model weights or third-party repositories are mirrored in this repository.

## Why this file exists

Hugging Face model cards are intended to document model details, intended use, limitations, training information, and license metadata. See https://huggingface.co/docs/hub/en/model-cards for guidance.
