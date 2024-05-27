import requests
import json
import os

# GitHub repository details
GIT_TOKEN = os.getenv('GIT_TOKEN')
REPO_OWNER = 'geekabhinavp'
REPO_NAME = 'auto-gpt-review'

# GPT API details
GPT_API_KEY = os.getenv('GPT_API_KEY')
GPT_API_URL = 'https://api.openai.com/v1/chat/completions'

# Fetch pull request files
def fetch_pr_files(pr_number):
    headers = {
        'Authorization': f'token {GIT_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files'
    print(f"Requesting URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR files: {response.json()}")
        return None
    return response.json()

# Send code to GPT for review
def send_code_to_gpt(code):
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': code}
        ],
        'max_tokens': 200,
        'temperature': 0.7
    }
    response = requests.post(GPT_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Error from GPT API: {response.json()}")
        return None
    return response.json()

# Post review comments on GitHub
def post_review_comments(comments, file_path, pr_number):
    headers = {
        'Authorization': f'token {GIT_TOKEN}',
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
    # Debugging: Print environment variables
    print(f"GIT_TOKEN: {GIT_TOKEN}")
    print(f"GPT_API_KEY: {GPT_API_KEY}")
    print(f"PR_NUMBER: {os.getenv('PR_NUMBER')}")
    
    pr_number = os.getenv('PR_NUMBER')
    if not pr_number:
        raise ValueError("Pull Request number is not set in the environment variables.")
    
    pr_files = fetch_pr_files(pr_number)
    if pr_files is None:
        print("Failed to fetch PR files. Exiting.")
        return

    # Debugging: Print the fetched pull request files
    print(f"Fetched PR files: {pr_files}")

    for file in pr_files:
        # Debugging: Print each file object
        print(f"Processing file: {file}")
        if file.get('status') == 'modified':
            file_response = requests.get(file['raw_url'])
            code = file_response.text
            gpt_response = send_code_to_gpt(code)
            if gpt_response is None or 'choices' not in gpt_response:
                print(f"Error: Unexpected GPT API response: {gpt_response}")
                continue
            comments = gpt_response['choices'][0]['message']['content'].strip().split('\n')
            post_review_comments(comments, file['filename'], pr_number)

if __name__ == "__main__":
    main()
