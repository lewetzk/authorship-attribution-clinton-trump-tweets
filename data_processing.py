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
import logging

logging.basicConfig(filename = 'processing.log', level = logging.DEBUG)

class ProcessData():
    """Class that process the train CSV and extracts relevant statistics, 
       storing the mean values of the features in a CSV.
    
    Args:
        train (str) : CSV file containing the train set
        
    Returns:
        None
        
    """
    
    def __init__(self, train, is_test):
        self.is_test = is_test
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
        self.stats = {"HillaryClinton" : {"char" : [], "upper" : [], 
                                          "lower" : [], "sen_nums" : [],
                                          "norm_!" : [], "norm_." : [], 
                                          "norm_?" : [],  "norm_," : [],    
                                          "av_w_len" : []},
                      "DonaldTrump" : {"char" : [], "upper" : [], 
                                          "lower" : [], "sen_nums" : [],
                                          "norm_!" : [], "norm_." : [], 
                                          "norm_?" : [],  "norm_," : [],    
                                          "av_w_len" : []}}
        self.test_stats = []
        self.test_tweets = []
        self.test_authors = []
        # dict that stores certain statistics for all tweets
        self.mean_stats_H = ["HillaryClinton"]
        self.mean_stats_D = ["DonaldTrump"]
        # lists for both authors containing the mean value of each 
        # feature (for exporting to csv)
        # indices:
        # 0 : author, 
        # 1 : Number of chars, 2 : number of uppercase letters,
        # 3 : number of lowercase letters,
        # 4 : average number of sentences per tweet,
        # 5 : average number of ! per tweet,
        # 6 : average number of . per tweet,
        # 7 : average number of ? per tweet,
        # 8 : average number of , per tweet,   
        # 9 : average word length
        self.bad_indices = []
        # In rare cases, a tweet is only a link, which is removed by a regex
        # later. Used for later processing to avoid index errors


    def process_data(self):
        """Method that processes the tweet data by applying various linguistc
           methods and calculating certain statistics which are exported
           to a csv.
           
           Args:
               None
        
           Returns:
               None
        
        """
        for author in ["DonaldTrump", "HillaryClinton"]:
            self._read_data(self.train)
            segments = self._segment_sentences(self.data_dict[author])
            self.ling_inf_dict[author].append(
                                        self._extract_linguistic_inf(segments))  
            self.sen_dict[author].append(segments)  
            self._get_mean_stats(author) 
        self._write_to_csv([self.mean_stats_H, self.mean_stats_D], "stats.csv")
        
   
        
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
                    if self.is_test == False:
                        if column[0] == "HillaryClinton":
                            self.data_dict["HillaryClinton"].append(column[1])
                        else:
                            self.data_dict["DonaldTrump"].append(column[1])  
                    else:
                        self.test_tweets.append(column[1])
                        self.test_authors.append(column[0])
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
        for raw_tweet in raw_tweet_list:
            doc = nlp(raw_tweet)
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
                ling_inf_list (list) : list of three valued tuples 
         
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
       
    def _get_mean_stats(self, author):
        """Method that extracts the mean value of all features in a feature
           dict of an author.
           
           Args:
               author (str) : Either HillaryClinton or DonaldTrump
        
           Returns:
               None
         
        """
        try:
            self._count_sen_stats(author)
            for key, value in self.stats[author].items():
                if author == "HillaryClinton":
                    self.mean_stats_H.append(statistics.mean(value))
                if author == "DonaldTrump":
                    self.mean_stats_D.append(statistics.mean(value))
        except TypeError:
            logging.error("TypeError : Dict values might be empty (NoneType).")
                
    def _count_sen_stats(self, author):
        """Method that calculates linguistic features and deposits them in the
           feature dict.
           
           Args:
               author (str) : Either HillaryClinton or DonaldTrump
        
           Returns:
               None
         
        """
        try:
            for seg_tweet in self.sen_dict[author][0]:
                stat_list = self._count_lower_upper_case(seg_tweet)
                self.stats[author]["char"].append(stat_list[2])
                self.stats[author]["upper"].append(stat_list[0])
                self.stats[author]["lower"].append(stat_list[1])
                self.stats[author]["sen_nums"].append(len(seg_tweet))
            self.stats[author]["av_w_len"] = self._get_av_word_len(
                                                 self.ling_inf_dict[author][0])
            self.stats[author]["norm_!"] = self._count_punctuation("!", 
                                                      self.sen_dict[author][0])
            self.stats[author]["norm_?"] = self._count_punctuation("?", 
                                                      self.sen_dict[author][0])
            self.stats[author]["norm_."] = self._count_punctuation(".", 
                                                      self.sen_dict[author][0])
            self.stats[author]["norm_,"] = self._count_punctuation(",", 
                                                      self.sen_dict[author][0])
        except IndexError:
            logging.error("IndexError: self.sen_dict values might be empty.")
            
    def _get_av_word_len(self, tagged_tweets):
        """Method that calculates the average word length per tweet.""
           
           Args:
               tagged_tweets (list) : A list that contains three-valued tuples
                                      (text, tag, lemma)
        
           Returns:
                av_word_len_all (list) : list of ints representing the average
                                         word length per tweet
         
        """
        
        punct_list = [".", "!", ",", "?", "”", "-", "–", "'", '"', ":", "#", 
                      "..."]
        av_word_len_all = []
        for tweet_segs in tagged_tweets:
            if tweet_segs != [[]]:
                # due to some unclean data list containing empty list sneaks in
                # as a seg around 2 times: Ignore it to avoid zero division
                av_word_lens = []
                for sen in tweet_segs:
                    if sen != '':
                        # Same for empty string as segment: also ignored
                        for inf_tuple in sen:
                           if inf_tuple[0] not in punct_list:
                               # If word not punctuation: consider as candidate
                               # for word length
                               av_word_lens.append(len(inf_tuple[0]))
                av_word_len_all.append(statistics.mean(av_word_lens))
                # get mean word length per tweet
        return av_word_len_all

    
    def _count_punctuation(self, punct, segmented_tweets):
        """Method that calculates the normalized amount of a certain 
           punctuation char per tweet.""
           
           Args:
               punct (str) : A punctuation character
               segmented_tweets (str) : List of segmented tweets
        
           Returns:
                total_punct (list) : List of ints representing the normalized
                                     amount of the character per tweet
        """
        try:
            total_punct = []
            for seg_tweet in segmented_tweets:
                if seg_tweet == ['']:
                    if self.is_test == True:
                        self.bad_indices.append(segmented_tweets.index(seg_tweet))
                if seg_tweet != ['']:
                    # empty string might sneak in: avoid
                    punct_amount = 0
                    tweet_len = 0
                    for sen in seg_tweet:
                        if sen != ['']:
                            # same as above
                            tweet_len += len(sen)
                            for char in sen:
                                if char == punct:
                                    punct_amount += 1
                    total_punct.append(punct_amount/tweet_len)
                    # normalize amount of punct by tweet
            return total_punct
        except ZeroDivisionError:
            logging.error("ZeroDivisonError: is the sen_dict value empty or" +
                          " is the data corrupted?")
        
                    
    def _count_lower_upper_case(self, seg_tweet):
        """Method that calculates the normalized amount of upper- and lowercase
           letters and the relative amount of chars per tweet.""
           
           Args:
               seg_tweet (list) : A segmented tweet.
               
           Returns:
               [sum(upper_nums),
                sum(lower_nums),
                sum(char_lens)] (list) : List of the sums of normalized
                                         upper- and lowercase appearances as
                                         well as relative amount of chars per
                                         tweet
        """
        try:
            lower_nums = []
            upper_nums = []
            char_lens = []
            for sen in seg_tweet:
                if sen != '':
                    char_lens.append(len(sen))
                    lower_nums.append(sum(map(str.islower, sen))/len(sen))
                    # Normalize: divide sum of lower and upper letters by 
                    # length of the sentence
                    upper_nums.append(sum(map(str.isupper, sen))/len(sen))
        except ZeroDivisionError:
            logging.error("ZeroDivisionError: empty string might be in "+
                  "following tweet: ", seg_tweet)
        finally:
            return [sum(upper_nums),
                    sum(lower_nums),
                    sum(char_lens)]
        
    def _write_to_csv(self, stat_lists, filename):
        """Method that writes a data list into a csv.
           Args:
               stat_list (list) : List of statistics of features
               filename (str) : Name of the file
        
           Returns:
                total_punct (list) : List of ints representing the normalized
                                     amount of the character per tweet
                                     
        """
        try:
            with open(filename, mode = "w") as stat_file:
                stat_writer = csv.writer(stat_file, delimiter = ",", 
                                             quotechar = '"', 
                                             quoting = csv.QUOTE_MINIMAL)
                for stat_list in stat_lists:
                    stat_writer.writerow([stat_list[0], stat_list[1],
                                          stat_list[2], stat_list[3],
                                          stat_list[4], stat_list[5],
                                          stat_list[6], stat_list[7],
                                          stat_list[8], stat_list[9]])
                    # 0 : author, 
                    # 1 : Number of chars, 2 : number of uppercase letters,
                    # 3 : number of lowercase letters,
                    # 4 : average number of sentences per tweet,
                    # 5 : average number of ! per tweet,
                    # 6 : average number of . per tweet,
                    # 7 : average number of ? per tweet,
                    # 8 : average number of , per tweet,   
                    # 9 : average word length
        except FileNotFoundError:
            logging.error("File not found")
        
                
                
                
                
        