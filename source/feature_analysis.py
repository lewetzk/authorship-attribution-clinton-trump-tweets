 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:04:41 2020

@author: lea
"""

from source.data_processing import ProcessData
import csv
import logging
import os

logging.basicConfig(filename = 'errors.log', level = logging.DEBUG)

class FeatureAnalysis(ProcessData):
    """Class that uses the previously calculated models for both authors to
       classify the raw tweets in a csv by extracting the same linguistic
       features as the train set. By calculating the minimal distance 
       between a tweet vector and both models, it can be decided which author
       is most likely. 
    csv
    Args:
        train (str) : CSV file containing the train set
        is_test (bool) : boolean value whether or not the csv that is going 
                         to be analyzed is either the test set (True) or the
                         train set (False)
        stats_csv (str) : CSV file containing the models for Hillary Clinton
                          and Donald Trump
                         
    Returns:
        None
        
    """
    def __init__(self, stats_csv, train, is_test):
        super().__init__(train, is_test)
        self.stats_csv = stats_csv
        self.is_test = True
        # instances to be analyzed are part of the test set
        self.H_stats = []
        # mean statistics for the features of Hillary Clinton's tweets
        self.D_stats = []
        # mean statistics for the features of Donald Trump's tweets
        self.test_ling_inf = []
        # linguist information stored in three-valued tuples (text, tag, lemma)
        self.test_seg_tweets = []
        # segmented tweets of the test set
        self.test_tweet_stats = []
        # statistics for every tweet of the test set stored in tuples
        self.removed_links = False
        # Were dead tweets (aka links only containing a link) removed?
        self.classified_tweets = []
        # List containing lists with a raw tweet and the suspected author
        self.bad_indices = []
        # In rare cases, a tweet is only a link, which is removed by a regex,
        # leading to problems down the line. The indices of those "bad tweets"
        # is saved

    
    def classify_tweet(self, test_csv):
        """Method that classifies a test set of tweets by author, either
           Donald Trump or Hillary Clinton, depending on the minimum feature
           distance.
           Args:
               test_csv (str) : Name of a csv containing the test set
        
           Returns:
               None
        
        """
        self._read_data(test_csv)
        # read data from test_set.csv
        self._read_agg_stats_csv()
        # read models from stats.csv
        self._get_test_stats()
        # get all stats from the test set
        self.classified_tweets = self._calc_likely_author()
        # classify the tweets with the most likely author
        self._write_results_csv(self.classified_tweets, 
                                os.path.join("csvs", "results.csv"))
        # write results to csv
    
    def _read_agg_stats_csv(self):
        """Method that extracts data from the stats CSV and saves the
           statistics in an attribute.
           Args:
               None
        
           Returns:
               None
        
        """
        
        if not os.path.isfile(self.stats_csv):
            raise FileNotFoundError
            logging.error("stats.csv not found.")
        with open(self.stats_csv, "r", encoding = "utf-8") as stats_file:
            csv_reader = csv.reader(stats_file, delimiter = ",")
            for line in csv_reader:
                if line:
                    if line[0] == "HillaryClinton":
                        self.H_stats = line
                    else:
                        self.D_stats = line
    
    def _get_test_stats(self):
        """Method that calculates the feature statistics for every tweet in
           the test set, saving said statistics in an attribute.
           
           Args:
               None
        
           Returns:
               None
        
        """
        test_segmented_unclean = self._segment_sentences(self.test_tweets)
        # make "unclean" segments containing empty tweet (previously link)
        self.bad_indices = [i for i, value in enumerate(test_segmented_unclean) 
                            if value == ['']]
        # get indices of [''], aka prior link only tweet
        if self.removed_links == False:
            self._remove_links(self.test_tweets)
            self._remove_links(self.test_authors)
                # remove "bad" tweets (aka tweets that only contain link and 
                # nothing else) to ensure that both self.test_tweets and the 
                # punctuation and word feature indices match
        test_segmented = self._segment_sentences(self.test_tweets)
        test_ling_inf = self._extract_linguistic_inf(test_segmented)
        test_punct_1 = self._count_punctuation("!", test_segmented)
        test_punct_2 = self._count_punctuation(".", test_segmented)
        test_punct_3 = self._count_punctuation("?", test_segmented)
        test_punct_4 = self._count_punctuation(",", test_segmented)
        # get punctuation stats
        word_len = self._get_av_word_len(test_ling_inf)
        for i in range(len(test_segmented)):
            low_up_char = self._count_lower_upper_case(test_segmented[i])
            self.test_stats.append((self.test_tweets[i], low_up_char[2], 
                                    low_up_char[0], low_up_char[1], 
                                    len(test_segmented[i]), test_punct_1[i],
                                    test_punct_2[i], test_punct_3[i], 
                                    test_punct_4[i], word_len[i]))
            # save stats per tweet in a tuple
    
    def _calc_likely_author(self):
        """Method that calculates the minimum distance between the features
           of all test tweets and one of the authors.
           
           Args:
               None
        
           Returns:
               classified_tweets (list) : List containing lists with a raw 
                                          tweet and the suspected author
        
        """
        classified_tweets = []
        for stat_tuple in self.test_stats:
            distance_H = 0
            distance_D = 0
            for i in range(1,len(stat_tuple)):
                distance_H += abs(stat_tuple[i] - float(self.H_stats[i]))
                distance_D += abs(stat_tuple[i] - float(self.D_stats[i]))
            if distance_H > distance_D:
                classified_tweets.append([stat_tuple[0], "realDonaldTrump"])
            elif distance_D > distance_H:
                classified_tweets.append([stat_tuple[0], "HillaryClinton"])
            elif distance_D == distance_H: 
                classified_tweets.append([stat_tuple[0], "unclear"])
                # very unlikely case but still good to have
        return classified_tweets
    
    def _write_results_csv(self, classified_tweets, filename):
        with open(filename, mode = "w", encoding = "utf-8") as stat_file:
            result_writer = csv.writer(stat_file, delimiter = ",", 
                                     quotechar = '"', 
                                     quoting = csv.QUOTE_MINIMAL) 
            for i in range(len(classified_tweets)):
                # First row: tweet, second row: suspected author, third row:
                # actual author
                result_writer.writerow([classified_tweets[i][0], 
                                       classified_tweets[i][1],
                                       self.test_authors[i]])


        
    
    def _remove_links(self, data_list):
        """Method that removes 'dead' indices correlating to a tweet that
           only consists of a single tweet (which is removed by a regex 
           earlier, making the tweet or author entry obsolete).
           
           Args:
               data_list (list) : a list containing data correlating to tweets
                                  (either the raw tweet or the author)
        
           Returns:
               None
        
        """
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
        self.removed_links = True
        
    
                
    def _get_accuracy(self, class_tweet_list):
        """Method that calculates the accuracy of the classifier.
           
           Args:
               class_tweet_list (list) : a list containing lists with a raw 
                                         tweet and the suspected author
        
           Returns:
               counter/len(class_tweet_list) (float) : a float describing
                                                       the accuracy of the
                                                       classifier
        
        """
        counter = 0
        for i in range(len(class_tweet_list)):
            if class_tweet_list[i][1] == self.test_authors[i]:
                counter += 1
        return counter/len(class_tweet_list)                