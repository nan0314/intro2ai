import math as np
import re
import math as np

class Bayes_Classifier:

    def __init__(self):
        self.good_likely = {}
        self.bad_likely = {}
        self.total_occur = {}
        self.num_class_words = [0.0,0.0]
        self.priors = [0.0,0.0]
        self.stop_words = [u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', 
                            u"she's", u'her', u'hers', u'herself', u'it', u"it's", u'its', u'itself', u'they', u'them', 
                            u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', 
                            u'that', u"that'll", u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be',
                            u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing',
                            u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until',
                            u'while', u'of', u'at'] 



    def train(self, lines):
        
        for line in lines:
            c = line[0]

            if c == '5':
                self.priors[1] += 1.0
            else:
                self.priors[0] += 1.0

            line = line.split('|')
            review = line[2].lower()
            punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

            for char in review:
                if char in punc and char != " ":
                    review = review.replace(char,"")
                    
            review = review.split()
            review = [word for word in review if not word in self.stop_words]


            for word in review:

                if c == '5':
                    self.num_class_words[1] = self.num_class_words[1] + 1.0
                    if word in self.good_likely.keys():
                        self.good_likely[word] = self.good_likely[word] + 1.0
                    else:
                        self.good_likely[word] = 1.0

                else:
                    self.num_class_words[0] = self.num_class_words[0] + 1.0
                    if word in self.bad_likely.keys():
                        self.bad_likely[word] = self.bad_likely[word] + 1.0
                    else:
                        self.bad_likely[word] = 1.0





    def classify(self, lines):
        
        prediction = []

        for line in lines:
            line = line.split('|')
            review = line[2].lower()
            punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

            for char in review:
                if char in punc and char != " ":
                    review = review.replace(char,"")
                    
            review = review.split()
            review = [word for word in review if not word in self.stop_words]


            prob_good = 0
            prob_bad = 0
            for word in review:

                if word in self.good_likely.keys():
                    prob_good = prob_good + np.log(self.good_likely[word]/self.num_class_words[1])
                    
                else:
                    prob_good = prob_good + np.log(1/(self.num_class_words[1] + sum(self.num_class_words)))

                if word in self.bad_likely.keys():
                    prob_bad = prob_bad + np.log(self.bad_likely[word]/self.num_class_words[0])
                else:
                    prob_bad = prob_bad + np.log(1/(self.num_class_words[0] + sum(self.num_class_words)))

            prob_good = prob_good + np.log(self.priors[1]/float(sum(self.priors)))
            prob_bad = prob_bad + np.log(self.priors[0]/float(sum(self.priors)))

            if prob_good > prob_bad:
                prediction.append('5')
            else:
                prediction.append('1')

        return prediction
