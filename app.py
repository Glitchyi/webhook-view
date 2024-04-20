from itertools import groupby
from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)

# This will store the webhook data
webhook_events = []

# Load data from JSON file on startup
if os.path.exists('webhooks.json'):
    with open('webhooks.json', 'r') as file:
        webhook_events = json.load(file)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    data_dict = data.to_dict()
    data_dict = json.loads(data_dict["payload"])
    repo_info = data_dict.get("repository", {})
    commit_info = data_dict.get("head_commit", {})

    filtered_data = {
        "repo": repo_info.get("full_name", ""),
        "html_url": repo_info.get("html_url", ""),
        "timestamp": commit_info.get("timestamp", ""),
        "commit": commit_info.get("id", ""),
        "message": commit_info.get("message", ""),
        "author": commit_info.get("author", {}).get("name", "")
    }

    webhook_events.append(filtered_data)
    with open("webhooks.json", "a") as file:
        json.dump(webhook_events, file, indent=4)
    return "", 200


@app.route("/")
def index():
        webhook_events.sort(key=lambda x: x['repo'])
        grouped_data = {k: list(v) for k, v in groupby(webhook_events, key=lambda x: x['repo'])}
        return render_template("webhooks.html", webhooks=grouped_data)

if __name__ == "__main__":
    app.run(debug=True)
