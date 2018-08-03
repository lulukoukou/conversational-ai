"""This contains verification functions.
"""
from gensim.models.doc2vec import Doc2Vec

class Verification(object):
    
    def __init__ (self,input1,input2, inputs=None):
        """
        input1: user prompt (sentence)
        input2: list of synonmy/antonym/definition/sample
        """
        self.model = Doc2Vec.load('./model.d2v')
        self.threshold = 0.0 
        self.flag = True
        
        if isinstance(input2,str):
            self.score1 = self.str_list(input1) 
            self.score2 = self.str_list(input2)
            
    def synonym(self):
        """check whether it is a correct synonmy
        """
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
            through search inside the prepared lists
        """
        for item in input1.split():
            if (item in input2):
                return True
        return False

    def str_list(self,inputs):
        """ calculate the similarity score
            normalize the word embedding vector
        """
        tmp = []
        for item in inputs.split():
            if item in self.model.wv:
                tmp.append(item)
        return tmp

    def evaluate_definition(self):
        """ evaluate whether it is correct definition or sample sentence
            through distance between normalized scores
        """
        score = self.model.n_similarity(self.score1,self.score2)
        if (score >= self.threshold):
            return True
        else:
            return False

    def evaluate_sample(self):
        """ evaluate whether it is meaningful sentence
        """
        score = self.model.n_similarity(self.score1,self.score2)
        if (score >= self.threshold):
            return True
        else:
            return False


if __name__ == "__main__":

    input1 = 'he is good'
    input2 = 'she is not good'

    i = Verification(input1,input2)
    print (i.sample())

""" improvement: 1. normalization term, probabilistic distribution
                 2. classification natural/unnatural for sample sententce
                 """
