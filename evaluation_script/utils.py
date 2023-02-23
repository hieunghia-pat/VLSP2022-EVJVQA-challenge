import re
import string

def is_japanese_sentence(text: str):
    # REFERENCE UNICODE TABLES: 
    # http:#www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
    # http:#www.tamasoft.co.jp/en/general-info/unicode.html
    #
    # TEST EDITOR:
    # http:#www.gethifi.com/tools/regex
    #
    # UNICODE RANGE : DESCRIPTION
    # 
    # 3000-303F : punctuation
    # 3040-309F : hiragana
    # 30A0-30FF : katakana
    # FF00-FFEF : Full-width roman + half-width katakana
    # 4E00-9FAF : Common and uncommon kanji
    # 
    # Non-Japanese punctuation/formatting characters commonly used in Japanese text
    # 2605-2606 : Stars
    # 2190-2195 : Arrows
    # u203B     : Weird asterisk thing
    pattern = r"[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B"
    return re.search(pattern, text) is not None

def is_vietnamese_sentence(text: str):
    pattern = r"[áàảãạúùủũụýỳỷỹỵíìỉĩịóòỏõọốồổỗộớờởỡợéèẻẽẹếềểễệđ]"
    return re.search(pattern, text) is not None

def normalize_answer(s, is_japanese: False):
    if is_japanese: # if the answer is Japanese then treat each string as tokens
        return list(s)
    else: # else normalize the Vietnamese and English answer, lower text, remove punctuation and articles
        def remove_punc(text):
            exclude = set(string.punctuation)
            return ''.join(ch for ch in text if ch not in exclude)
        def lower(text):
            return text.lower()
        
        return remove_punc(lower(s)).split()