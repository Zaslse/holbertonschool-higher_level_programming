#!/usr/bin/env python3
"""Serialize and deserialize Python dictionaries using JSON."""

import json


def serialize_and_save_to_file(data, filename):
    """Save a dictionary to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_and_deserialize(filename):
    """Load a dictionary from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
