#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 19:18:05 2020

@author: lea
"""
# Lea Wetzke
# lwetzke@uni-potsdam.de
# Universität Potsdam
# Bachelor Computerlinguistik

import unittest
import os
from source.data_processing import ProcessData


class DataProcessingTestMethods(unittest.TestCase):
    def setUp(self):
        self.dataproc = ProcessData(os.path.join("csvs", "train_set.csv"),
                                    False)
        self.tweet_list = ["Trump wants to be our Commander-in-Chief. " +
                           "Here's how he's treated veterans thus far: " +
                           "https://t.co/iquFJ676Rj"]

    def test_if_filenotfounderror_triggered(self):
        self.dataproc_error = ProcessData("blahblah.csv", False)
        with self.assertRaises(FileNotFoundError):
            self.dataproc_error._read_data("blahblah.csv")

    def test_if_segment_sentences_return_is_equal_to_num_of_raw_tweets(self):
        seg_tweet = self.dataproc._segment_sentences(self.tweet_list)
        self.assertEqual(len(self.tweet_list), len(seg_tweet))

    def test_if_extract_ling_data_return_is_equal_to_num_of_raw_tweets(self):
        ling_inf_tweet = self.dataproc._extract_linguistic_inf(self.tweet_list)
        self.assertEqual(len(self.tweet_list), len(ling_inf_tweet))

    def test_if_count_lower_upper_case_return_not_0(self):
        seg_tweet = self.dataproc._segment_sentences(self.tweet_list)
        lower_upper_char = self.dataproc._count_lower_upper_case(seg_tweet[0])
        for data in lower_upper_char:
            self.assertTrue(data != 0)

    def test_if_count_punctuation_returns_list_with_floats(self):
        punct = self.dataproc._count_punctuation(".", self.tweet_list)
        self.assertTrue(type(punct[0]) == float)

    def test_if_av_word_len_returns_list_with_ints(self):
        ling_inf_tweet = self.dataproc._extract_linguistic_inf(self.tweet_list)
        for num in self.dataproc._get_av_word_len(ling_inf_tweet):
            self.assertTrue(type(num) == int)

    def test_if_indexerror_raised_in_count_sen_stats(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  "Commander-in-Chief."]]
        with self.assertRaises(IndexError):
            self.dataproc._count_sen_stats("DonaldTrump")

    def test_if_count_sen_stats_fills_out_punct_in_stats_dict(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  "Commander-in-Chief."]]
        ling_inf = self.dataproc._extract_linguistic_inf(self.tweet_list)
        self.dataproc.ling_inf_dict["DonaldTrump"].append(ling_inf)
        self.dataproc._count_sen_stats("DonaldTrump")
        self.assertTrue(self.dataproc.stats["DonaldTrump"]["norm_."])

    def test_if_count_sen_fills_out_av_word_len(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  " Commander-in-Chief."]]
        ling_inf = self.dataproc._extract_linguistic_inf(
            self.dataproc.sen_dict["DonaldTrump"])
        self.dataproc.ling_inf_dict["DonaldTrump"].append(ling_inf)
        self.dataproc._count_sen_stats("DonaldTrump")
        self.assertTrue(
            type(self.dataproc.stats["DonaldTrump"]["av_w_len"][0]) == float)

    def test_if_count_sen_fills_out_av_sen_num(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  " Commander-in-Chief."]]
        ling_inf = self.dataproc._extract_linguistic_inf(
            self.dataproc.sen_dict["DonaldTrump"])
        self.dataproc.ling_inf_dict["DonaldTrump"].append(ling_inf)
        self.dataproc._count_sen_stats("DonaldTrump")
        self.assertTrue(
            type(self.dataproc.stats["DonaldTrump"]["sen_nums"][0] == int))

    def test_if_count_sen_fills_out_char_num(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  " Commander-in-Chief."]]
        ling_inf = self.dataproc._extract_linguistic_inf(
            self.dataproc.sen_dict["DonaldTrump"])
        self.dataproc.ling_inf_dict["DonaldTrump"].append(ling_inf)
        self.dataproc._count_sen_stats("DonaldTrump")
        self.assertTrue(
            type(self.dataproc.stats["DonaldTrump"]["char"][0] == int))

    def test_if_get_mean_stats_has_correct_len(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  " Commander-in-Chief."]]
        ling_inf = self.dataproc._extract_linguistic_inf(
            self.dataproc.sen_dict["DonaldTrump"])
        self.dataproc.ling_inf_dict["DonaldTrump"].append(ling_inf)
        self.dataproc._count_sen_stats("DonaldTrump")
        self.dataproc._get_mean_stats("DonaldTrump")
        self.assertEqual(len(self.dataproc.mean_stats_D), 10)

    def test_if_process_data_generates_stats_csv(self):
        self.dataproc.sen_dict["DonaldTrump"] = [["Trump wants to be our" +
                                                  " Commander-in-Chief."]]
        ling_inf = self.dataproc._extract_linguistic_inf(
            self.dataproc.sen_dict["DonaldTrump"])
        self.dataproc.ling_inf_dict["DonaldTrump"].append(ling_inf)
        self.dataproc._count_sen_stats("DonaldTrump")
        self.dataproc._get_mean_stats("DonaldTrump")
        self.dataproc._write_to_csv([self.dataproc.mean_stats_D],
                                    os.path.join("csvs", "stats.csv"))
        self.assertTrue(os.path.isfile(os.path.join("csvs", "stats.csv")))


if __name__ == "__main__":
    unittest.main()
