import requests
import json
import re




# Retrieve the API key from an environment variable
#api_key = os.getenv("OPENAI_API_KEY")
api_key = "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"




# Define the API endpoint URL
url = "https://api.openai.com/v1/responses"


# Set up the headers for the request
headers = {
   "Content-Type": "application/json",
   "Authorization": f"Bearer {api_key}"
}


# Define the data payload for the request
data = {
   "model": "gpt-4.1",
   "input": "Create 5 JEE mains style questions in math which is a combination of one or more topics Binomial Theorem, Trigonometric Identities, Permutations and Combinations, Set theory, Sequence and Series. Each question should display four multiple choice options, and a hint. The questions should begin with ### . Example ### Question 1, ### Question 2. Also append **before but not after each option letter.Example **A, **B"
}


# Make the POST request


response = requests.post(url, headers=headers, json=data)


# Raise an exception for bad status codes (4xx or 5xx)
response.raise_for_status()
gpt_response = json.loads(response.text)
extracted_text = gpt_response['output'][0]['content'][0]['text']


print("\n showing individual questions below\n")


question_blocks = extracted_text.strip().split('\n---\n')


for question_block in question_blocks:
   print(question_block)
   print("individual question printed")
   question_pattern = r"### Question (\d+)"
   question_match = re.search(question_pattern, question_block,re.IGNORECASE)
   print("id", question_match.group(1))
   print("text", question_block)












