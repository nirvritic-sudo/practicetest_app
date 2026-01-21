import requests
import json
import re
import time
import os


# --- Configuration ---
API_KEY = "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"
API_URL = "https://api.openai.com/v1/chat/completions"




def fetch_questions_with_retry(url, headers, payload, max_retries=3, delay=2):
   """Internal helper to hit OpenAI API with retry logic."""
   for attempt in range(1, max_retries + 1):
       try:
           print(f"Connecting to API (Attempt {attempt}/{max_retries})...")
           response = requests.post(url, headers=headers, json=payload)
           response.raise_for_status()
           return response.json()
       except requests.exceptions.RequestException as e:
           print(f"Error on attempt {attempt}: {e}")
           if attempt < max_retries:
               time.sleep(delay)
           else:
               print("Max retries reached.")
               raise




def parse_questions(question_blocks):
   """Internal helper to parse the raw text into a list of dicts."""
   questions = []
   for block in question_blocks:
       try:
           if not block.strip() or any(x in block for x in ["Sure!", "Certainly!", "Let me know"]):
               continue


           # 1. ID
           question_match = re.search(r"Question (\d+)", block, re.IGNORECASE)
           if not question_match: continue
           question_id = question_match.group(1)


           # 2. Answer
           answer_text = ""
           answer_match = re.search(r'(?:\*\*|#)?(?:Correct\s*)?Answer:?(?:\*\*)?\s*(.*)', block, re.IGNORECASE)
           if answer_match:
               answer_text = answer_match.group(1).strip()
               answer_text = re.sub(r'\.$', '', answer_text)


           # 3. Hint
           hint = ""
           hint_match = re.search(r'(?:\*\*|#)?Hint:?(?:\*\*)?\s*(.*?)(?=\s*(?:\*\*|#)?(?:Correct\s*)?Answer:|$)',
                                  block, re.DOTALL | re.IGNORECASE)
           if hint_match:
               hint = hint_match.group(1).strip().replace('\n', ' ')


           # 4. Text Extraction
           question_start = question_match.end()
           options_start_match = re.search(r"\*\*A\.?", block, re.IGNORECASE)


           if options_start_match:
               raw_q_text = block[question_start:options_start_match.start()].strip().replace('\n', ' ')


               # --- NEW FIX: Remove leading dots/punctuation ---
               # This regex replaces any dots or whitespace at the start of the string
               question_text = re.sub(r'^[\.\s]+', '', raw_q_text)
           else:
               continue


           # 5. Options
           option_map = {"A": "", "B": "", "C": "", "D": ""}
           option_regex = r'\*\*([A-D])\.?\s*(.*?)(?=\s*\*\*[A-E]|\s*Hint:|\s*\*\*Hint|\s*(?:\*\*|#)?(?:Correct\s*)?Answer:|$)'
           option_matches = re.findall(option_regex, block, re.DOTALL | re.IGNORECASE)


           for letter, text in option_matches:
               clean_text = text.strip().replace('\n', ' ')
               if letter.upper() in option_map:
                   option_map[letter.upper()] = f"({letter.upper()}) {clean_text}"


           questions.append({
               "id": question_id,
               "question": question_text,
               "options": [option_map["A"], option_map["B"], option_map["C"], option_map["D"]],
               "Hint": hint,
               "correct_answer": answer_text
           })
       except Exception as e:
           print(f"Skipping block due to error: {e}")
           continue
   return questions




# --- PUBLIC FUNCTION TO CALL FROM APP.PY ---
def generate_questions_llm(subject, topics=None, difficulty_level=None):
   """
   Main callable function.
   Returns a Python list of question dictionaries.
   """
   headers = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {API_KEY}"
   }
   prompt_text = (
       f"Create 10 JEE mains style {difficulty_level} questions in {subject} covering these topics: {topics}. "
       "Each question should display four multiple choice options, a hint, the the correct answer. "
       "The questions should begin with ### . Example ### Question 1. Also append ** before but not after each option letter. Example **A, **B"
   )
   data_payload = {
       "model": "gpt-4",  # Ensure model name is correct (gpt-4, gpt-3.5-turbo, etc.)
       "messages": [
           {"role": "system", "content": "You are a helpful assistant that generates JEE Chemistry questions."},
           {"role": "user",
            "content": prompt_text}
       ],
       "temperature": 0.7


   }
   print("prompt=" + prompt_text)
   print("Selected topics=" + str(topics))
   try:
       api_data = fetch_questions_with_retry(API_URL, headers, data_payload)


       if 'choices' in api_data:
           extracted_text = api_data['choices'][0]['message']['content']
       else:
           return []  # Return empty list on failure


       # Split and Parse
       question_blocks = re.split(r'(?=### Question \d+)', extracted_text)
       parsed_data = parse_questions(question_blocks)


       return parsed_data


   except Exception as e:
       print(f"Error generating questions: {e}")
       return []