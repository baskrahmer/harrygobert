import logging
import re

import os
import torch


def preprocess(query: str) -> str:
    # Fix HTML encoding
    query = query.replace('&amp;', '&')
    query = query.replace('&ndash;', '-')
    query = query.replace('&#39;', "'")
    query = query.replace('&#8211;', "-")
    query = query.replace('&lt;', "<")
    query = query.replace('&gt;', ">")
    query = query.replace('&#226;', "â")

    # Remove data inbetween parentheses
    query = re.sub(r" ? \([^)]+\)", "", query)
    query = re.sub(r" ?<[^>]+>", "", query)
    query = re.sub(r" ?\[[^>]+\]", "", query)

    # Remove percentages
    query = re.sub(r'[ -.\d]*%', "", query)

    # Remove leading/trailing whitespace
    query = query.strip()

    return query.lower()


def get_model_function(path):
    logging.info("trying to load model...")
    model = torch.load(os.path.join(path, "model.pt"))
    tokenizer = torch.load(os.path.join(path, "tokenizer.pt"))
    logging.info("model loaded")
    return model, tokenizer