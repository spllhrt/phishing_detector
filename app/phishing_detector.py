import logging
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

nltk.download('stopwords')
nltk.download('punkt')

phishing_keywords = [
    "urgent", "click here", "verify your account", "congratulations", "you have won", 
    "password", "account locked", "important message", "update your information", 
    "limited time offer", "security alert", "login required", "suspicious activity", "act now"
]

blacklisted_domains = ["example-phish.com", "suspicious-domain.com", "secure-banking.com"]

def is_similar_domain(domain):
    legitimate_domains = ["yahoo.com", "gmail.com", "tup.edu.com"]
    for legit_domain in legitimate_domains:
        similarity_ratio = SequenceMatcher(None, domain, legit_domain).ratio()
        if similarity_ratio > 0.8:
            return True
    return False

def perform_phishing_detection(data):
    try:
        logger.info(f"Analyzing data: {data}")
        subject = data.get('subject', '').lower()
        content = data.get('content', '').lower()
        sender = data.get('sender', '').lower()
        
        stop_words = set(stopwords.words('english'))
        content_tokens = word_tokenize(content)
        filtered_content = [word for word in content_tokens if word not in stop_words]
        
        confidence_score = 0
        
        subject_keywords_detected = sum(keyword in subject for keyword in phishing_keywords)
        content_keywords_detected = sum(
            keyword in " ".join(filtered_content) for keyword in phishing_keywords
        )
        
        confidence_score += subject_keywords_detected * 10
        confidence_score += content_keywords_detected * 10

        sender_domain = sender.split("@")[-1]
        if sender_domain in blacklisted_domains:
            logger.info("Detected sender from blacklisted domain.")
            confidence_score += 25
        elif is_similar_domain(sender_domain):
            logger.info("Detected domain similarity to known legitimate domains.")
            confidence_score += 20

        links = re.findall(r'http[s]?://\S+', content)
        for link in links:
            domain = re.findall(r'://([^/]+)', link)
            if domain and domain[0] != sender_domain:
                logger.info("Detected suspicious link to external domain.")
                confidence_score += 20

        if len(re.findall(r'[^a-zA-Z0-9\s.,]', content)) > 5:
            logger.info("Detected unusual formatting or characters.")
            confidence_score += 15

        urgency_patterns = ["immediately", "act now", "asap", "today only"]
        if any(pattern in content for pattern in urgency_patterns):
            logger.info("Detected urgent language.")
            confidence_score += 10

        if "attachment" in content or "attached file" in content:
            logger.info("Detected mention of attachment in content.")
            confidence_score += 15

        confidence_score = min(confidence_score, 100)

        result = {
            "is_phishing": confidence_score >= 50,
            "confidence_score": confidence_score
        }

        logger.info(f"Detection result: {result}")
        return result

    except KeyError as e:
        logger.error(f"KeyError: Missing expected key {str(e)} in data: {data}")
        return {"is_phishing": False, "confidence_score": 0}
    except Exception as e:
        logger.error(f"An error occurred while detecting phishing: {str(e)}")
        return {"is_phishing": False, "confidence_score": 0}
