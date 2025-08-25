import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
import string

# Make sure NLTK resources are downloaded once
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def simple_summarize(text, max_sentences=3):
    # Tokenize sentences
    sentences = sent_tokenize(text)
    if len(sentences) <= max_sentences:
        return text  # already short enough

    # Tokenize words & compute frequency
    stop_words = set(stopwords.words("english"))
    word_freq = defaultdict(int)

    for word in word_tokenize(text.lower()):
        if word not in stop_words and word not in string.punctuation:
            word_freq[word] += 1

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]

    # Pick top N sentences
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary_sentences = ranked_sentences[:max_sentences]
    return " ".join(summary_sentences)

import random

def simple_quiz_generator(text, num_questions=3):
    words = [w for w in word_tokenize(text) if w.isalpha()]
    unique_words = list(set(words))
    if len(unique_words) < 5:
        return []

    questions = []
    for _ in range(num_questions):
        answer = random.choice(unique_words)
        question = f"What does '{answer}' mean in the context of your notes?"

        # Wrong options
        distractors = random.sample([w for w in unique_words if w != answer], 3)
        options = distractors + [answer]
        random.shuffle(options)

        questions.append({
            "question": question,
            "options": options,
            "answer": answer
        })

    return questions

import requests

# Replace with your Hugging Face API Token

import os

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("API_URL")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def ai_quiz_generator(text, num_questions=3):
    """Generate quiz questions using Hugging Face Inference API."""
    # shorten text if too long
    payload = {"inputs": "generate questions: " + text[:500]}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            data = response.json()
            questions = []
            for i, q in enumerate(data[:num_questions]):
                questions.append({
                    "question": q["generated_text"],
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Student decides"
                })
            return questions
        except Exception as e:
            return [{"question": f"Error parsing response: {e}", "options": [], "answer": ""}]
    else:
        return [{"question": f"API Error: {response.status_code}", "options": [], "answer": ""}]
