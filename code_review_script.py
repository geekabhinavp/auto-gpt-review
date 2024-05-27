import requests
import json
import os

# GitHub repository details
GITHUB_TOKEN = os.getenv('GIT_TOKEN')
REPO_OWNER = 'knackofabhi'
REPO_NAME = 'gpt-review'

# GPT API details
GPT_API_KEY = os.getenv('GPT_API_KEY')
GPT_API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'

# Fetch pull request files
def fetch_pr_files(pr_number):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    return response.json()

# Send code to GPT for review
def send_code_to_gpt(code):
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': f'Review the following code for best practices and potential issues:\n\n{code}',
        'max_tokens': 200,
        'temperature': 0.5
    }
    response = requests.post(GPT_API_URL, headers=headers, data=json.dumps(data))
    return response.json()

# Post review comments on GitHub
def post_review_comments(comments, file_path, pr_number):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/comments'
    for comment in comments:
        data = {
            'body': comment,
            'path': file_path,
            'position': 1  # Adjust based on where the comment should go
        }
        requests.post(url, headers=headers, data=json.dumps(data))

def main():
    pr_number = input("Enter the Pull Request number: ")
    pr_files = fetch_pr_files(pr_number)
    for file in pr_files:
        if file['status'] == 'modified':
            file_response = requests.get(file['raw_url'])
            code = file_response.text
            gpt_response = send_code_to_gpt(code)
            comments = gpt_response['choices'][0]['text'].strip().split('\n')
            post_review_comments(comments, file['filename'], pr_number)

if __name__ == "__main__":
    main()