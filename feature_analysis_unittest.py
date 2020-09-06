#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 18:23:37 2020

@author: lea
"""
# Lea Wetzke
# lwetzke@uni-potsdam.de
# Universität Potsdam
# Bachelor Computerlinguistik


import unittest
import os
from source.feature_analysis import FeatureAnalysis


class FeatureAnalysisTestMethods(unittest.TestCase):
    def setUp(self):
        train_path = os.path.join("csvs", "train_set.csv")
        self.fa = FeatureAnalysis(os.path.join("csvs", "stats.csv"),
                                  train_path, True)
        self.fa.test_tweets = ["Only one had a real answer. " +
                               "https://t.co/sjnEokckis", "Barack Obama was "
                               + "born in America, plain and simple."]
        self.fa.test_authors = ["HillaryClinton", "HillaryClinton"]
        self.fa._read_agg_stats_csv()
        self.fa._get_test_stats()
        self.fa.classified_tweets = self.fa._calc_likely_author()

    def test_if_get_accuracy_returns_float_smaller_equal_1(self):
        self.assertTrue(self.fa._get_accuracy(self.fa.classified_tweets) <= 1)

    def test_if_author_stats_attribute_filled_out(self):
        for entry in self.fa.H_stats:
            self.assertTrue(type(entry) == str)

    def test_if_second_entry_in_classified_tweets_is_H_or_D(self):
        for entry in self.fa.classified_tweets:
            self.assertTrue(entry[1] == "HillaryClinton" or
                            entry[1] == "DonaldTrump")

    def test_if_get_test_stats_checks_for_bad_indices(self):
        self.assertTrue(self.fa.removed_links)

    def test_if_test_stats_is_filled_with_tuple_of_correct_len(self):
        self.assertEqual(len(self.fa.test_stats[0]), 10)

    def test_if_remove_link_removes_bad_indices(self):
        self.fa.test_tweets = ["Only one had a real answer.",
                               "https://t.co/sjnEokckis"]
        self.fa.test_authors = ["HillaryCLinton", "DonaldTrump"]
        self.fa.bad_indices = [1]
        self.fa._remove_links(self.fa.test_tweets)
        self.fa._remove_links(self.fa.test_authors)
        self.assertTrue(len(self.fa.test_authors) == 1 and
                        len(self.fa.test_tweets) == 1)

    def test_if_write_to_csv_writes_results_csv(self):
        self.fa._write_results_csv(self.fa.classified_tweets,
                                   os.path.join("csvs", "res_test.csv"))
        self.assertTrue(os.path.isfile(os.path.join("csvs", "res_test.csv")))

    def test_if_get_test_stats_indexerror_triggered(self):
        self.fa.test_tweets = ["https://t.co/sjnEokckis"]
        with self.assertRaises(IndexError):
            self.fa._get_test_stats()


if __name__ == "__main__":
    unittest.main()
