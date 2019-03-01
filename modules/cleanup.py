import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

# make a class such that we can use sklearn gridsearchCV and pipeline

class cleanup(object):
    def __init__(self,stem_on=False):
        self.stem_on=stem_on
    
    @classmethod
    def cancelmath(cls, test_str):
        regex = r"(\$+)(?:(?!\1)[\s\S])*\1"
        
        subst = ""
        
        test_str=re.sub(r"\n", " ", test_str, 0, re.MULTILINE)
        
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)
        
        return result
    
    @classmethod
    def delete_stopword_mathsymbols(cls, text):
        temp = []
        stop = stopwords.words('english')
        for x in text.split(" "):
            if x.lower() in stop or len(x) <3 or x.isdigit() or ("\\" in x) or ("^" in x) or ("[" in x) or ("]" in x):
                continue
            x=x.lower()
            x=re.sub(r"[!@#$%^&*()_+=-`~'\-\d.]", "", x, 0, re.MULTILINE)
            if x not in stop:
                temp += [x]
    
    
        return " ".join(temp)
    
    
    @classmethod
    def stem_words(cls, text):
        tokens=word_tokenize(text)
        stemmer = PorterStemmer()
        #pat = re.compile(r'[\\\!\@\#\$\%\^\&\*\(\)\_\=\+]')
        empty = []
        for x in tokens:
            #if len(pat.findall(x)) == 0:
            empty += [stemmer.stem(x)]
        # text=pat.sub("",text)
        # tokensss=word_tokenize(text)
        return empty
    

    
    
    def fit(self, text1, text2):
        return self
    
    def transform(self, text):
        text = cleanup.cancelmath(text)
        
        text = cleanup.delete_stopword_mathsymbols(text)
        
        if self.stem_on:
            tokens = cleanup.stem_words(text)
    
            text=" ".join(tokens)
        return text
