This project was written on Linux Manjaro KDE Plasma 20.0.3 with Python 3.7.6.

DESCRIPTION
The following project consists of an authorship attribution classifier of tweets made either by Hillary Clinton or Donald Trump. By extracting the mean statistics for various linguistic features from a dedicated training set, 
a mean value can be derived for each feature, forming a unique feature vector for both authors. The same linguisitc features can then be extracted from a test set. By applying a set of calculations, a minimum distance between the
feature vector of a single test set tweet and the feature vectors of both authors can be derived. This way, the test tweet is classified with the author with the minimal distance - aka the author "closest" to the linguistic features of the tweet.
For the extraction of said linguistic features, spacy is used. The features are sentence-, word-, and characterbased.
The project uses the "Hillary Clinton and Donald Trump Tweets"  corpus, containing around 6400 tweets from both politicians, mainly from the 2016 election.
The corpus can be found here: https://www.kaggle.com/benhamner/clinton-trump-tweets.

REQUIREMENTS
The requirements can be found in the requirements.txt.

HOW TO USE
1) Download the Hillary Clinton and Donald Trump Tweet corpus from kaggle.
2) Place it in the root directory of the project.
3) Install the dependencies with the following command: python -m pip install -r requirements.txt.
4) Install spacy's pretrained statistic model: python -m spacy download en_core_web_sm
5) Run the following command in your terminal: python main.py.

The classified tweets are stored in the csvs directory under results.csv with each column containing the raw tweet, the suspected author and the actual author. The accuracy is displayed in the terminal after finishing.
Runtime may vary on hardware. It is generally around 2-3 minutes. Information about which step is currently being completed will be shown.

INFO:
Lea Wetzke
797451
PRO-2 SoSe 2020
lwetzke@uni-potsdam.de
