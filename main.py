#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:35:36 2020

@author: lea
"""

from preprocessing import SplitTweetCorpus
from data_processing import ProcessData
import numpy


if __name__ == "__main__":
    print("Splitting corpus...")
    stc = SplitTweetCorpus("tweets.csv")
    stc.split_corpus()
    pcd = ProcessData("train_set.csv")
    print("Feature analysis...")
    pcd.process_data()
    print("Aggregated features exported as csv.")