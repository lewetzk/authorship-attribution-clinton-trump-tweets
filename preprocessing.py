#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:17:46 2020

@author: lea
"""

import csv
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(filename = 'processing.log', level = logging.DEBUG)

class SplitTweetCorpus():
    """Class that splits the Hillary-Trump-Twitter-Corpus into three parts
       for later processing.
       
    Args: 
        tweet_csv (str): csv containing corpus
        
    Returns:
        None
        
    """
    def __init__(self, tweet_csv):
        self.tweet_csv = tweet_csv
        self.tweet_data = []
    
    def _read_csv(self):
        """Method that reads tweet.csv and extracts relevant data"""
        try:
            with open(self.tweet_csv,"r") as tweetcorp:
                csv_reader = csv.reader(tweetcorp, delimiter = ",")
                for column in csv_reader:
                    if column[3] == "False":
                    # only want true tweets, no retweets
                        self.tweet_data.append((column[1], column[2]))
        except FileNotFoundError:
            # Durch logging ersetzen
            logging.error("File not found")
            
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
        self._write_to_csv(train, "train_set.csv")
        self._write_to_csv(test, "test_set.csv")        
        self._write_to_csv(val, "val_set.csv")          
        
    def _write_to_csv(self, data_list, filename):
        """Method that writes a data list into a csv."""
        try:
            with open(filename, mode = "w") as subset_file:
                subset_writer = csv.writer(subset_file, delimiter = ",", 
                                             quotechar = '"', 
                                             quoting = csv.QUOTE_MINIMAL)
                for data_tuple in data_list:
                    subset_writer.writerow([data_tuple[0], data_tuple[1]])
        except FileNotFoundError:
            logging.error("File not found")

            