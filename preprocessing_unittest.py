#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 18:15:31 2020

@author: lea
"""


import unittest
from source.preprocessing import SplitTweetCorpus


class PreprocessingTestMethods(unittest.TestCase):
    def setUp(self):
        self.stc = SplitTweetCorpus("tweets.csv")
        self.stc.split_corpus()
        
    def test_if_tweet_data_list_with_tuples(self):
        self.assertTrue(type(self.stc.tweet_data) == list)
    
    def test_if_tweet_data_elements_are_tuples(self):
        for element in self.stc.tweet_data:
            self.assertTrue(type(element) == tuple)
            
    def test_if_filenotfounderror_triggered(self):
        self.stc_error = SplitTweetCorpus("blahblah.csv")
        with self.assertRaises(FileNotFoundError):
            self.stc_error.split_corpus()
 
            
if __name__ == "__main__":
    unittest.main()