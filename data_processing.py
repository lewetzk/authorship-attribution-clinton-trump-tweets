#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 12:55:49 2020

@author: lea
"""

import spacy
import csv

class ProcessData():
    def __init__(self, train, test, val):
        self.test = test
        self.train = train
        self.val = val
    
    def _read_data(self, csv_file):
        try:
            with open(csv_file,"r") as data_file:
                csv_reader = csv.reader(data_file, delimiter = ",")
                data_dict = {"HillaryClinton" : [], "DonaldTrump" : []}
                for column in csv_reader:
                    if column[0] == "HillaryClinton":
                        data_dict["HillaryClinton"].append(column[1])
                    else:
                        data_dict["DonaldTrump"].append(column[1])
                return data_dict      
        except FileNotFoundError:
            print("Datei nicht gefunden")
    
    def _segment_sentences(self, tweet_data_list):
        pass
        
    

if __name__ == "__main__":
    pcd = ProcessData("train_set.csv","test_set.csv", "val_set.csv")
    print(pcd._read_data(pcd.test)["DonaldTrump"])
    