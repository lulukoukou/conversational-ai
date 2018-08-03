"""This contains verification functions.
"""
import sys

sys.path.append("verification/verification1/")

from gensim.models import KeyedVectors
import urllib
import urllib2
import json
from contextlib import closing

class Verification(object):
    
    def __init__ (self, word, input_syn, input1, input2, inputs=None):
        """
        input1: user prompt (sentence)
        input2: list of synonmy/antonym/definition/sample
        """
        self.word = word
        self.input1 = input1
        self.input2 = input2
        self.list_syn = input_syn
        self.threshold_syn = 0.8
        self.threshold_def = 0.75
        self.threshold_exa = 50
        self.key_grammer = "XLAWqKxdNCOhmnxp"
        self.key_similarity = "78229e5e0264417581fdcd80f76bed44"
        #self.score1 = self.str_list(input1) 
        #self.score2 = self.str_list(input2)
            
    def synonym(self):
        """check whether it is a correct synonmy
        """
        '''
        check2 = False
        
        try:
            for item in self.input1.split():
                similarity_score = self.word_vectors.similarity(self.word, item)
                if similarity_score > self.threshold_syn:
                    check2 = True
        except:
            check2 = False
            
        if self.check():
            return True
        elif check2:
            return True
        else:
            return False
        '''
        return (self.check())
    
    def definition(self):
        """similarity
        """
        return (self.evaluate_definition())
    
    def sample(self):
        """similarity
        """
        return (self.evaluate_sample())

    def check(self):
        """ check whether is synonmy or antonym
            key-word match for the prepared lists
        """
        for item in self.input1.split():
            if (item in self.input2):
                return True
        return False

    def str_list(self,inputs):
        """ calculate the similarity score
            normalize the word embedding vector
        """
        i = 1
        j = 1
        tmp = []
        word = []
        string = inputs
        for item in string.split():
            #if item in self.word_vectors:
            if i == 1:
                for char in item:
                    if j == 1:
                        word.append(char.upper())
                        j += 1
                    else:
                        word.append(char)
                item = ''.join(word)
            tmp.append(item)
            i += 1
        
        return tmp

    def evaluate_definition(self):
        """ evaluate whether it is correct definition or sample sentence
            through distance between normalized scores
        """
        tmp_list = self.input1.split()
        flag_syn = False
        for item in tmp_list:
            if item in self.list_syn:
                flag_syn = True
                return True
        print (tmp_list)
        if len(tmp_list) <= 3:
            if not flag_syn:
                return False
        try:
            answer = self.CallSimilarity()
            print (answer)
            flag = True
            if answer:
                if answer['similarity'] <= self.threshold_def:
                    return False
            return flag
        except:
            return True
        
    def evaluate_sample(self):
        """ evaluate whether it is meaningful sentence
        """
        '''
        score = self.model.n_similarity(self.score1,self.score2)
        if (score >= self.threshold):
            return True
        else:
            return False
        '''
        tmp_list = self.input1.split()
        flag1 = False
        flag_property = False
        if self.word in tmp_list:
            flag1 = True
        if not flag1:
            return False
        
        try:
            return_input1 = self.CallWikifier(self.input1)
            return_input2 = self.CallWikifier(self.input2[0])
            if return_input1 == return_input2:
                flag_property = True
            answer = self.CallGrammerChecker()
            for key,value in answer.iteritems():
                if key == "result":
                    flag1 = flag1 and value
                if key == "score":
                    if value >= self.threshold_exa:
                        return (flag1 and True and flag_property)
            
            return (flag1 and flag_property)
        except:
            return True

    def CallGrammerChecker(self):
        self.score1 = self.str_list(input1)
        data = urllib.urlencode([("text", ''.join(self.score1)), ("key",self.key_grammer)])
        url = "https://api.textgears.com/check.php"
        req = urllib2.Request(url, data=data.encode("utf8"))
        answer = {}
        with closing(urllib2.urlopen(req)) as f:
            response = f.read()
            response = json.loads(response.decode("utf8"))
            for key,value in response.iteritems():
                if key == 'result':
                    answer[key] = value
                if key == 'score':
                    answer[key] = value
                if key == 'better':
                    answer[key] = value[0]
        return answer
    
    def CallSimilarity(self):

        flag_ground = False
        tmp_list = self.input1.split()
        if self.word in tmp_list:
            flag_ground = True

        if flag_ground:
            self.score1 = self.str_list(input1)
            
        else:
            tmp = self.str_list(self.word)
            tmp.extend(self.input1.split())
            self.score1 = tmp

        answer = {'similarity':0.0}
        tmp2 = []
        i = 1
        j = 1
        for item_input2 in self.input2:
            if i == 1:
                tmp2 = self.str_list(self.word)
                tmp2.append("means")
                i += 1
            tmp2.extend(item_input2.split())
            self.score2 = tmp2
            #print (' '.join(self.score1))
            #print (' '.join(self.score2))
            data = urllib.urlencode([("text1", ' '.join(self.score1)),("text2",' '.join(self.score2)),("token",self.key_similarity)])
            url = "https://api.dandelion.eu/datatxt/sim/v1/"
            req = urllib2.Request(url, data=data.encode("utf8"))
            with closing(urllib2.urlopen(req)) as f:
                response = f.read()
                response = json.loads(response.decode("utf8"))
                for key,value in response.iteritems():
                    if j == 1:
                        if key == 'similarity':
                            answer[key] = value
                            j += 1
                    elif key == 'similarity' and value < answer[key]:
                        answer[key] = value

        return answer

    def CallWikifier(self, inputs):
        return_key = 'adjectives'
        l = {'verbs':[],'nouns':[],'adjectives':[],'adverbs':[]}
        data = urllib.urlencode([("userKey","ibjywjedmtslyjidefvkcsktttxxrq"),("text", inputs), ("lang", "en"),("pageRankSqThreshold", 0.8), ("applyPageRankSqThreshold", "true"),("nTopDfValuesToIgnore", "200"),("wikiDataClasses", "false"), ("wikiDataClassIds", "false"),("support","false"), ("ranges", "false"),("includeCosines", "false"), ("maxMentionEntropy", "3"),("partsOfSpeech","true")])
        url = "http://www.wikifier.org/annotate-article"
        req = urllib2.Request(url, data=data.encode("utf8"))
        with closing(urllib2.urlopen(req)) as f:
            response = f.read()
            response = json.loads(response.decode("utf8"))
            
            for key,value in response.iteritems():
                if key == 'verbs':
                    for item in response[key]:
                        l[key].append(item['normForm'])
                if key == 'nouns':
                    for item in response[key]:
                        l[key].append(item['normForm'])
                if key == 'adjectives':
                    for item in response[key]:
                        l[key].append(item['normForm'])
                if key == 'adverbs':
                    for item in response[key]:
                        l[key].append(item['normForm'])
        
        for key,value in l.iteritems():
            if self.word in value:
                return_key = key

        print (return_key)
        return return_key
        
                
if __name__ == "__main__":
    
    word = 'supplant'
    input1 = "the new iPhone will supplant last year's model."
    input2 = ["to take the place of something else"]
    
    syn = ['']
    i = Verification(word,syn,input1,input2)
    print (i.definition())


