#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:17:46 2020

@author: lea
"""

import csv
import os
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(filename = 'errors.log', level = logging.DEBUG)

class SplitTweetCorpus():
    """Class that splits the Hillary-Trump-Twitter-Corpus into three parts
       for later processing.
       
    Args: 
        tweet_csv (str): csv containing corpus
        
    Returns:
        None
        
    """
    def __init__(self, path_to_tweet_csv):
        self.tweet_csv = path_to_tweet_csv
        self.tweet_data = []

    def _read_csv(self):
        """Method that reads tweet.csv and extracts relevant data.
        
          Args: 
              None
          Returns: 
              None
              
        """

        if not os.path.isfile(self.tweet_csv):
            raise FileNotFoundError
            logging.error("tweet.csv not found")
        with open(self.tweet_csv,"r", encoding = "utf-8") as tweetcorp:
            csv_reader = csv.reader(tweetcorp, delimiter = ",")
            for column in csv_reader:
                if column != '\n':
                    if column[3] == "False":
                    # only want true tweets, no retweets
                        self.tweet_data.append((column[1], column[2]))

            
            
    def split_corpus(self):
        """Method that splits the corpus into 3 parts of 70/20/10 
           (train/test/validation).
        
          Args: 
              None
          Returns: 
              None
              
        """
        self._read_csv()
        train, test_val = train_test_split(self.tweet_data, test_size = 0.3)
        test, val = train_test_split(test_val, test_size = 0.333333)
        self._write_to_csv(train, os.path.join("csvs", "train_set.csv"))
        self._write_to_csv(test, os.path.join("csvs", "test_set.csv"))        
        self._write_to_csv(val, os.path.join("csvs", "val_set.csv"))          
        
    def _write_to_csv(self, data_list, filename):
        """Method that writes a data list into a csv.
        
          Args: 
              None
          Returns: 
              None
              
        """
        with open(filename, mode = "w", encoding = "utf-8", 
                  newline = "\n") as subset_file:
            subset_writer = csv.writer(subset_file, delimiter = ",", 
                                       quotechar = '"', 
                                       quoting = csv.QUOTE_MINIMAL)
            for data_tuple in data_list:
                subset_writer.writerow([data_tuple[0], data_tuple[1]])


            
