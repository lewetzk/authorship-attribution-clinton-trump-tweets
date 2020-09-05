#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:35:36 2020

@author: lea
"""

from source.preprocessing import SplitTweetCorpus
from source.data_processing import ProcessData
from source.feature_analysis import FeatureAnalysis
import sys
import os

if __name__ == "__main__":
    print("Splitting corpus...")
    stc = SplitTweetCorpus("tweets.csv")
    stc.split_corpus()
    train_path = os.path.join("csvs", "train_set.csv")
    pcd = ProcessData(train_path, False)
    print("Feature analysis...")
    pcd.process_data()
    print("Aggregated features exported as stats.csv.")
    fa = FeatureAnalysis(os.path.join("csvs", "stats.csv"), train_path, True)
    print("Classifying test tweets...")
    fa.classify_tweet(os.path.join("csvs", "val_set.csv"))
    print("Exported predictions, gold standard and accuracy in a csv.")
