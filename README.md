# Contact Flow - Smart Assist Feature

__Overview:__

The goal of this project was to develop a data science solution to an AWS Call Center demo (for the insurance domain). We would like to recommend useful help documents to an agent depending on what the caller says, once a caller asks to speak with an agent. 

To do so, I created a content-based recommender system, where the 'content' is what the caller says (i.e. *utterance*), that will do the following:

1. Extract text data (eg. short description of articles) from an S3 bucket.
2. Extract utterance from Amazon Connect Flow (in this case a call to the API).
3. Convert the collection of raw text to a matrix of TF-IDF features.
4. Compute cosine similarities.
5. Sort results such that the *n* most similar articles are returned, based on utterance.

This will improve customer satisfaction by offering a more personalized experience than a typical call center flow. From an agent point of view, it will equip them with the most related articles to what a caller said during the contact flow. 

__Technical Components:__

- Configuration was done through Serverless.
- AWS Lambda function to run python script.
- Amazon S3 to store data.

__Notes:__

1. I've uploaded the dataset to this repository if you would like to experiment with it. I do not show how the data was extracted, but I use a similar format to (this repository)[https://github.com/escanillans/web_scraping]. 
2. You will have to edit the *serverless.yml* and *recommender.py* scripts to fit your own requirements.
