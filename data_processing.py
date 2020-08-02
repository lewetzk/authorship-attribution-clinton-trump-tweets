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
    def __init__(self, train, test, val):
        self.test = test
        self.train = train
        self.val = val
        self.data_dict = {"HillaryClinton" : [], "DonaldTrump" : []}
    
    def _read_data(self, csv_file):
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
    
    def _segment_sentences(self, tweet_list):
        nlp = spacy.load("en_core_web_sm")
        sent_list = []
        for tweet in tweet_list:
            doc = nlp(tweet)
            for sent in doc.sents:
                sent_list.append(sent.text)
        rm_links_list = []
        for seg in sent_list:
            # sometimes spacy sentence segmenter treats link as sentence
            clean_seg = re.sub(r'http\S+', "", seg).rstrip("\n")
            clean_seg = clean_seg.rstrip("\n")
            rm_links_list.append(clean_seg)
        # regex that looks for links in strings that aren't treated as
        # own segment
        return rm_links_list
     
        
        
    

if __name__ == "__main__":
    pcd = ProcessData("train_set.csv","test_set.csv", "val_set.csv")
    pcd._read_data(pcd.test)
    print("\n\n\n")
    segs = pcd._segment_sentences(pcd.data_dict["HillaryClinton"])
    print(segs)
    test = ['—Erica Smegielski https://t.co/WVhAk7POo5']
    print(pcd._remove_links(test))
    