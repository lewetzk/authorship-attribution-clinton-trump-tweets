#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:55:49 2020

@author: lea
"""

import spacy
import csv
import re

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
        
    def process_data(self, author):
        """Method that processes the tweet data by segmenting, lemmatizing, tagging
           tagging and tokenizing it.
           Args:
               train (str) : CSV file containing the train set
        
           Returns:
               None
        
        """
        
        self._read_data(self.train)
        segments = self._segment_sentences(self.data_dict[author])
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
        for tweet in raw_tweet_list:
            doc = nlp(tweet)
            tweet_sents = []
            for sent in doc.sents:
                tweet_sents.append(sent.text)
            sent_list.append(tweet_sents)
        cleaned_tweets = []
        for tweet in sent_list:
            tweet_segs = []
            for seg in tweet:
            # sometimes spacy sentence segmenter treats link as sentence
                clean_seg = re.sub(r'http\S+', "", seg).rstrip("\n")
                clean_seg = clean_seg.rstrip("\n")
                tweet_segs.append(clean_seg)
            cleaned_tweets.append(tweet_segs)
        # regex that looks for] links in strings that aren't treated as
        # own segment
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
        liste = []
        for tweet in tweets_segmented:
            inf_tuples = []
            for seg in tweet:
                doc = nlp(seg)
                seg_tokens = []
                for token in doc:
                    seg_tokens.append((token.text, token.tag_, token.lemma_))
                inf_tuples.append(seg_tokens)
            liste.append(inf_tuples)
        return liste  
       
   
if __name__ == "__main__":
    pcd = ProcessData("train_set.csv")
    print("in process")
    print(pcd.process_data("HillaryClinton"))
    # print(pcd.process_data("DonaldTrump"))