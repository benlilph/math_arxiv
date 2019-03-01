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
        
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)
        
        return result
    
    @classmethod
    def delete_stopword_mathsymbols(cls, text):
        temp = []
        stop = stopwords.words('english')
        for x in word_tokenize(text):
            if x.lower() in stop or len(x) == 1 or x.isdigit() or ("\\" in x) or ("^" in x):
                continue
            
            temp += [x.lower()]
        return temp
    
    @classmethod
    def delete_double_digit(cls, tokens):
        # given a token , if it contains more than 2 numbers , then probably it is useless
        empty = []
        num_pat = re.compile(r'[0-9][0-9]')
        for x in tokens:
            if len(num_pat.findall(x)) == 0:
                empty += [x]
        return empty
    
    @classmethod
    def stem_words(cls, tokens):
        stemmer = PorterStemmer()
        #pat = re.compile(r'[\\\!\@\#\$\%\^\&\*\(\)\_\=\+]')
        empty = []
        for x in tokens:
            #if len(pat.findall(x)) == 0:
            empty += [stemmer.stem(x)]
        # text=pat.sub("",text)
        # tokensss=word_tokenize(text)
        return empty
    
    @classmethod
    def delete_all_symbol(cls, tokens):
        ###don't delete "-", we have something like 3-form
        empty=[]
        pat = re.compile(r'[\\\!\@\#\$\%\^\&\*\(\)\_\=\+]')
        for x in tokens:
            if len(pat.findall(x)) == 0:
                empty += [x.lower()]
        return empty
    
    def fit(self, text1, text2):
        return self
    
    def transform(self, text):
        text = cleanup.cancelmath(text)
        tokens = cleanup.delete_stopword_mathsymbols(text)
        tokens = cleanup.delete_double_digit(tokens)
        if self.stem_on:
            tokens = cleanup.stem_words(tokens)
        tokens = cleanup.delete_all_symbol(tokens)
        text=" ".join(tokens)
        return text
