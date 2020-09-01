This project was written on Linux Manjaro KDE Plasma 20.0.3 with Python 3.7.6.

DESCRIPTION
The following project consists of an authorship attribution classifier of tweets made either by Hillary Clinton or Donald Trump. By extracting the mean statistics for various linguistic features from a dedicated training set, 
a mean value can be derived for each feature, forming a unique feature vector for both authors. The same linguisitc features can then be extracted from a test set. By applying a set of calculations, a minimum distance between the
feature vector of a single test set tweet and the feature vectors of both authors can be derived. This way, the test tweet is classified with the author with the minimal distance.
The project uses the "Hillary Clinton and Donald Trump Tweets"  corpus, containing around 6400 tweets from both politicians, mainly from the 2016 election.
The corpus can be found here: https://www.kaggle.com/benhamner/clinton-trump-tweets

REQUIREMENTS
The requirements can be found in the requirements.txt

HOW TO USE
1) Download the Hillary Clinton and Donald Trump Tweet corpus from kaggle.
2) Place it in the root directory of the project.
3) Run the following command: python main.py

Runtime is around 2 minutes.
