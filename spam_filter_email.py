import re
import math
import os

def train_spam_filter(ham_dir, spam_dir):
    """Trains the spam filter on ham and spam email directories."""
    words = {}
    total_ham = 0
    total_spam = 0

    for label, directory in [("ham", ham_dir), ("spam", spam_dir)]:
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename), 'r', encoding='latin-1') as f:
                email_text = f.read()
                total = total_ham if label == "ham" else total_spam
                for word in re.findall(r'\w+', email_text):
                    words.setdefault(word, [0, 0])[0 if label == "ham" else 1] += 1
                total += 1

    # Calculate probabilities (with smoothing)
    for word, (ham_count, spam_count) in words.items():
        words[word] = [
            (ham_count + 1) / (total_ham + 2),
            (spam_count + 1) / (total_spam + 2)
        ]

    return words, total_ham, total_spam

def classify_email(email, words, total_ham, total_spam):
    """Classifies an email as spam or ham using Bayesian filtering."""
    prob_spam = math.log(total_spam / (total_ham + total_spam))
    prob_ham = math.log(total_ham / (total_ham + total_spam))

    for word in re.findall(r'\w+', email["body"]):
        if word in words:
            prob_spam += math.log(words[word][1])
            prob_ham += math.log(words[word][0])

    return prob_spam > prob_ham

def rule_based_filter(email):
    """Applies rule-based filtering on an email."""
    rules = {
        "subject": ["free", "money", "urgent", "viagra"],
        "body": ["click here", "limited time offer", "Nigerian prince"],
        "sender": ["spammer@domain.com"],
    }
    for key, values in rules.items():
        for value in values:
            if value.lower() in email.get(key, "").lower():
                return True
    return False

# Main program
if __name__ == "__main__":
    # Train the filter (replace with your actual directories)
    ham_directory = "/path/to/ham/emails"
    spam_directory = "/path/to/spam/emails"
    words, total_ham, total_spam = train_spam_filter(ham_directory, spam_directory)

    # Classify a new email (replace with your actual email)
    new_email = {
        "subject": "FREE MONEY NOW!!!",
        "body": "Click here for millions...",
        "sender": "spammer@domain.com",
    }

    if rule_based_filter(new_email) or classify_email(new_email, words, total_ham, total_spam):
        print("Spam detected!")
    else:
        print("Not spam.")