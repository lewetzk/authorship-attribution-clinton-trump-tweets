#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:35:36 2020

@author: lea
"""

from preprocessing import SplitTweetCorpus
from data_processing import ProcessData
from feature_analysis import FeatureAnalysis


if __name__ == "__main__":
    print("Splitting corpus...")
    stc = SplitTweetCorpus("tweets.csv")
    stc.split_corpus()
    pcd = ProcessData("train_set.csv", False)
    print("Feature analysis...")
    pcd.process_data()
    print("Aggregated features exported as csv.")
    fa = FeatureAnalysis("stats.csv", "train_set.csv", True)
    fa.classify_tweet("train_set.csv")
    # fa.test_tweets
    # fa._get_test_stats()
    