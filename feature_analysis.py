 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:04:41 2020

@author: lea
"""

from data_processing import ProcessData
import csv

class FeatureAnalysis(ProcessData):
    def __init__(self, stats_csv, train, is_test):
        super().__init__(train, is_test)
        self.stats_csv = stats_csv
        self.is_test = True
        self.H_stats = []
        self.D_stats = []
        self.test_ling_inf = []
        self.test_seg_tweets = []
        self.test_tweet_stats = []
        self.removed_links = False
    
    def _read_agg_stats_csv(self):
        """Method that extracts data from the stats CSV and saves the
           statistics .
           Args:
               stats_csv (str) : CSV file containing the previously extracted
                                 statistics
        
           Returns:
               None
        
        """
        
        try:
            with open(self.stats_csv,"r") as stats_file:
                csv_reader = csv.reader(stats_file, delimiter = ",")
                for line in csv_reader:
                    if line[0] == "HillaryClinton":
                        self.H_stats = line
                    else:
                        self.D_stats = line
        except FileNotFoundError:
            print("Datei nicht gefunden")

    def classify_tweet(self, test_csv):
        self._read_data(test_csv)
        self._read_agg_stats_csv()
        self._get_test_stats()
        return self._calc_min_distance()
    
    def _get_test_stats(self):
        if self.bad_indices != []:
            if self.removed_links == False:
                self._remove_links(self.test_tweets)
                self._remove_links(self.test_authors)
                self.removed_links = True
            # remove "bad" tweets (aka tweets that only contain link and 
            # nothing else) to ensure that both self.test_tweets and the 
            # punctuation and word feature indices match
        print(len(self.test_tweets))
        test_segmented = self._segment_sentences(self.test_tweets)
        test_ling_inf = self._extract_linguistic_inf(test_segmented)
        test_punct_1 = self._count_punctuation("!", test_segmented)
        print(len(test_punct_1))
        test_punct_2 = self._count_punctuation(".", test_segmented)
        test_punct_3 = self._count_punctuation("?", test_segmented)
        test_punct_4 = self._count_punctuation(",", test_segmented)
        word_len = self._get_av_word_len(test_ling_inf)
        for i in range(len(test_segmented)):
            low_up_char = self._count_lower_upper_case(test_segmented[i])
            self.test_stats.append((self.test_tweets[i], low_up_char[2], 
                                    low_up_char[0], low_up_char[1], 
                                    len(test_segmented[i]), test_punct_1[i],
                                    test_punct_2[i], test_punct_3[i], 
                                    test_punct_4[i], word_len[i]))
            # save stats per tweet in a tuple
        return self.test_stats
    
    def _calc_min_distance(self):
        classified_tweets = []
        for stat_tuple in self.test_stats:
            distance_H = 0
            distance_D = 0
            for i in range(1,len(stat_tuple)):
                distance_H += abs(stat_tuple[i] - float(self.H_stats[i]))
                distance_D += abs(stat_tuple[i] - float(self.D_stats[i]))
            if distance_H > distance_D:
                classified_tweets.append([stat_tuple[0], "HillaryClinton"])
            elif distance_D > distance_H:
                classified_tweets.append([stat_tuple[0], "DonaldTrump"])
        return classified_tweets
    
    def _remove_links(self, data_list):
        if len(self.bad_indices) == 1:
            del data_list[self.bad_indices[0]]
            # If only one bad index: simply delete it (no consequences)
        if len(self.bad_indices) > 1:
            index_c = 0
            # Counter for how many elements have been removed: with every
            # element removed, the placement of other bad indices later on 
            # shifts by -c
            # Else: non-link tweets removed
            for i in self.bad_indices:
                del data_list[i-index_c]
                index_c+= 1
                
    def _get_accuracy(self, class_tweet_list):
        counter = 0
        for i in range(len(class_tweet_list)):
            if class_tweet_list[i][1] == self.test_authors[i]:
                counter += 1
        return counter/len(class_tweet_list)                