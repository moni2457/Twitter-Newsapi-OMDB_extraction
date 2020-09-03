import re

# cleaning the emoticons
# Regex reference from https://stackoverflow.com/questions/51784964/remove-emojis-from-multilingual-unicode-text
def clean_emoticons(text):
    if text is None:
        return text
    else:
        pattern = re.compile("\["
                         u"\U0001F600-\U0001F64F"  # emoticons
                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                         u"\U00002702-\U000027B0"
                         u"\U000024C2-\U0001F251"
                         "\]+", flags=re.UNICODE)
        return pattern.sub(r'', text)

# Regex reference from https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# cleaning the special characters
def clean_special_characters(text):
    if text is None:
        return text
    else:
        clean_text = re.sub(r'[^a-zA-Z0-9\s\.]+', '', text)
        return clean_text

# cleaning URLs
# Regex reference from https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
def clean_URL(text):
    if text:
        clean_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        return clean_text

# cleaning special tags
def clean_special_tags(text):
    if text:
        clean_text = re.sub(r'[^a-zA-Z0-9\s\.]+', '', text)
        return clean_text