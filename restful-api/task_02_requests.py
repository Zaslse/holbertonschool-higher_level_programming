#!/usr/bin/python3
"""Fetch posts from JSONPlaceholder and export them to CSV."""
import csv
import requests


URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_and_print_posts():
    """Fetch posts and print the HTTP status and post titles."""
    response = requests.get(URL)
    print("Status Code: {}".format(response.status_code))
    if response.status_code == 200:
        for post in response.json():
            print(post["title"])


def fetch_and_save_posts():
    """Fetch posts and save their id, title, and body to CSV."""
    response = requests.get(URL)
    if response.status_code == 200:
        posts = [
            {"id": post["id"], "title": post["title"],
             "body": post["body"]}
            for post in response.json()
        ]
        with open("posts.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "body"])
            writer.writeheader()
            writer.writerows(posts)
