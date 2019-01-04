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

1. I've uploaded the dataset to this repository if you would like to experiment with it. I do not show how the data was extracted, but I use a similar format to [this repository](https://github.com/escanillans/web_scraping). 
2. You will have to edit the *serverless.yml* and *recommender.py* scripts to fit your own requirements.

__Example:__
Try out a working solution (https://ghguq2g52j.execute-api.us-east-1.amazonaws.com/dev/?query=), where you type your query after '?query='. 

For example, if I was interested in updating my beneficiaries, then I would make the following request: `https://ghguq2g52j.execute-api.us-east-1.amazonaws.com/dev/?query=update my beneficiary`.

Doing so will output the following:
`{
result: {
utterance: "update my beneficiary",
articles: [
{
Rank: 1,
Title: "The Basics Of A Beneficiary",
Link: "https://tristarins.com/life-insurance-plano-tx/",
score: 0.29831249039627694
},
{
Rank: 2,
Title: "Choosing a Life Insurance Beneficiary",
Link: "https://www.amfam.com/resources/articles/navigating-life-insurance/choosing-a-beneficiary",
score: 0.19850879067617114
},
{
Rank: 3,
Title: "Everything You Need to Know About Designating a Beneficiary",
Link: "https://www.rjonesinsurance.com/designating-a-beneficiary/",
score: 0.17387246417071017
}
]
}
}` 

Notice the output is in JSON format, which makes it easier to parse. The original utterance is returned as well as the top three articles along with their link and cosine similarity score (**not** a probability score). The number of articles returned can be changed. By default we set it to three. 
