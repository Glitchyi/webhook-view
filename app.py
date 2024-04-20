from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

# This will store the webhook data
webhook_events = []


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    data_dict = data.to_dict()
    data_dict = json.loads(data_dict["payload"])
    repo_info = data_dict.get("repository", {})
    commit_info = data_dict.get("head_commit", {})

    filtered_data = {
        "repo": repo_info["full_name"],
        "html_url": repo_info["html_url"],
        "timestamp": commit_info["timestamp"],
        "commit": commit_info["id"],
        "message": commit_info["message"],
        "author": commit_info["author"]["name"]
    }

    webhook_events.append(filtered_data)
    with open("webhooks.json", "a") as file:
        json.dump(webhook_events, file, indent=4)
    return "", 200


@app.route("/")
def index():
    return render_template("webhooks.html", webhooks=webhook_events)


if __name__ == "__main__":
    app.run(debug=True)
