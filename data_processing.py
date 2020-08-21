#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:55:49 2020

@author: lea
"""

import spacy
import csv
import re
import statistics

class ProcessData():
    """Class that process the train CSV and extracts relevant statistics.
    
    Args:
        train (str) : CSV file containing the train set
        
    Returns:
        None
        
    """
    
    def __init__(self, train):
        self.train = train
        # train set
        self.data_dict = {"HillaryClinton" : [], "DonaldTrump" : []}
        # dict that saves the raw tweet in a list as the value of an
        # author
        self.ling_inf_dict = {"HillaryClinton" : [], "DonaldTrump" : []}
        # dict that saves linguistic information (text, tag, lemma) of a
        # sentence in a nested list
        self.sen_dict = {"HillaryClinton" : [], "DonaldTrump" : []}
        # dict that saves the split sentences of a tweet
        # self.stats = {{"HillaryClinton" : {"norm_dots" : [], 
        #                                              "norm_lower" : [],
        #                                              "norm_upper" : [],
        #                                              "norm_sen_num" : [],
        #                                              "norm_sen_len" : [],
        #                                              "norm_word_len" : [],
        #                                              "norm_dots" : [],
        #                                              "norm_quest" : [],
        #                                              "norm_exc" : [] }},
        #                          {"DonaldTrump" : {"norm_dots" : [], 
        #                                           "norm_lower" : [],
        #                                           "norm_upper" : [],
        #                                           "norm_sen_num" : [],
        #                                           "norm_sen_len" : [],
        #                                           "norm_word_len" : [],
        #                                           "norm_dots" : [],
        #                                           "norm_quest" : [],
        #                                           "norm_exc" : [] }}}

    def process_data(self, author):
        """Method that processes the tweet data by segmenting, lemmatizing, 
           tagging and tokenizing it.
           Args:
               train (str) : CSV file containing the train set
        
           Returns:
               None
        
        """
        
        self._read_data(self.train)
        segments = self._segment_sentences(self.data_dict[author])
        print(segments)
        self.ling_inf_dict[author].append(self._extract_linguistic_inf(segments))  
        self.sen_dict[author].append(segments)            
   
        
    def _read_data(self, csv_file):
        """Method that extracts data from the train CSV and saves the raw
           tweets in self.data_dict.
           Args:
               train (str) : CSV file containing the train set
        
           Returns:
               None
        
        """
        
        try:
            with open(csv_file,"r") as data_file:
                csv_reader = csv.reader(data_file, delimiter = ",")
                for column in csv_reader:
                    if column[0] == "HillaryClinton":
                        self.data_dict["HillaryClinton"].append(column[1])
                    else:
                        self.data_dict["DonaldTrump"].append(column[1])      
        except FileNotFoundError:
            print("Datei nicht gefunden")
            
    def _segment_sentences(self, raw_tweet_list):
        """Method that segments a list of raw tweets into a nested list 
           Containing cleaned sentences with links removed.
           
           Args:
               raw_tweet_list (list) : List containing raw tweets as strings
        
           Returns:
               cleaned_tweets (list) : List of lists containing sentences of
                                       a tweet.
         
        """
        
        nlp = spacy.load("en_core_web_sm")
        sent_list = []
        # list of sentences (as split by spacy)
        for tweet in raw_tweet_list:
            doc = nlp(tweet)
            tweet_sents = []
            for sent in doc.sents:
                tweet_sents.append(sent.text)
            sent_list.append(tweet_sents)
        cleaned_tweets = []
        # list of cleaned tweets
        for tweet in sent_list:
            tweet_segs = []
            # list of segments in one tweet
            for seg in tweet:
            # sometimes spacy sentence segmenter treats link as sentence
                clean_seg = re.sub(r'http\S+', "", seg).rstrip("\n")
                # regex that looks for links in strings and subs them with
                # empty string
                clean_seg = clean_seg.rstrip("\n")
                # sometimes \n\n at end of tweet: remove 2nd newline
                tweet_segs.append(clean_seg)
            cleaned_tweets.append(tweet_segs)
        return cleaned_tweets
    
    def _extract_linguistic_inf(self, tweets_segmented):
        """Method that extracts linguistic information (text, tag, lemma) from
           a segmented tweet and returns it.""
           
           Args:
               tweets_segmented (list) : List containing segmented tweets
        
           Returns:
                (list) : lists of lists of lists
         
        """
        nlp = spacy.load("en_core_web_sm")
        ling_inf_list = []
        for tweet in tweets_segmented:
            inf_tuples = []
            for seg in tweet:
                doc = nlp(seg)
                seg_tokens = []
                for token in doc:
                    seg_tokens.append((token.text, token.tag_, token.lemma_))
                inf_tuples.append(seg_tokens)
            ling_inf_list.append(inf_tuples)
        return ling_inf_list 
       
    def _count_case_chars(self, author):
        char = []
        upper = []
        lower = []
        sen_nums = []
        for seg_tweet in self.sen_dict[author]:
            sen_stat_list = self.count_lower_upper_case(seg_tweet, "upper")
            char += sen_stat_list[2]
            upper += sen_stat_list[0]
            lower += sen_stat_list[1]
            sen_nums += len(seg_tweet)
            
    def _get_av_sentences_no_length(self, author):
        for seg_tweet in self.ling_inf_dict:
            pass
            # count avergae word length
            # count punctuation (.,!,?, ,)
    
    def _count_lower_upper_case(self, seg_tweet):
        try:
            lower_nums = []
            upper_nums = []
            char_lens = []
            for sen in seg_tweet:
                char_lens.append(len(sen))
                lower_nums.append(sum(map(str.islower, sen))/len(sen))
                upper_nums.append(sum(map(str.isupper, sen))/len(sen))
        except ZeroDivisionError:
            print(print("ZeroDivisionError: List of segmented tweets might" + 
                        " be empty"))
        except ZeroDivisionError:
            print("ZeroDivisionError: segmented tweet is empty.")
        finally:
            return [sum(upper_nums)/len(upper_nums),
                    sum(lower_nums)/len(lower_nums),
                    sum(char_lens)/len(char_lens)]

                
                
                
                
                
        
        
if __name__ == "__main__":
    pcd = ProcessData("train_set.csv")
    print("in process")
    #print(pcd.process_data("HillaryClinton"))
    # print(pcd.process_data("DonaldTrump"))