import boto3, json, os

import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
from nltk.stem.porter import PorterStemmer

import warnings
warnings.filterwarnings("ignore", message ="numpy.dtype size changed")

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

### Helper functions ###
# this function returns the title of a row that matches an id
def item(df, id):
    return(df.loc[df['ID'] == id]['title'].tolist()[0])

# this function returns the text of a row that matches an id
def itemDescription(df, id):
    return(df.loc[df['ID'] == id]['text'].tolist()[0])

# this function returns the link of a row that matches an id
def itemLink(df, id):
    return(df.loc[df['ID'] == id]['link'].tolist()[0])

'''
This function gets the stem of each word, for each title/description
input: column containing titles/descriptions
output: stem for each title/description
'''
def getStem(col):
    ps = PorterStemmer()
    stems = [ps.stem(word) for word in col]
    
    return(stems)

'''
This function computes the similarity of your input and documents in a db
input: column of data used to determine similarity
output: matrix of cosine similarities
'''
def computeSimilarities(col):
    print('Computing similarities...')
    # create object to convert collection of raw text docs to a matrix of TF-IDF features
    tf = TfidfVectorizer(analyzer = 'word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
    
    # learn vocab and idf, return term-doc matrix
    tfidf_matrix = tf.fit_transform(col)
    print('Successfully computed similarities.')
    # compute similarities
    return(cosine_similarity(tfidf_matrix, tfidf_matrix))

'''
This function organizes the output of computeSimilarities
input: original dataframe, cosine similarity matrix
output: a dictionary of all the documents and the top 20 ranked documents for each one
'''
def rankDocuments(df, cos_sim_matrix):
    results = {}
    print('Ranking documents...')
    print(df.iterrows())
    for idx, row in df.iterrows():
        # store similar ids based on cosine similarity, then sort in ascending order
        similar_indices = cos_sim_matrix[idx].argsort(kind='quicksort')[:-22:-1]    
        similar_items = [(cos_sim_matrix[idx][i], df['ID'][i]) for i in similar_indices]
        results[row['ID']] = similar_items[1:] 
    print('Documents are ranked.')
    return(results)
    
'''
This function returns the most similar articles to your input
input: the input index, dictionary of ranked documents, number of articles to return (default = 3)
output: 
'''
def recommend(df, id, ranked_docs, num = 3):
    print('Recommending articles...')

    records = ranked_docs[id][:num]
    result = []
    count = 1
    for record in records:
        complete_record = {'Rank': count, 'Title': item(df, record[1]), 'Link': itemLink(df, record[1]), 'score': record[0]}
        result.append(complete_record)
        count = count + 1

    print('Records ranked; Returned top 3 documents.')
    return(result)

### ---MAIN--- ###
def handler(event, context):
    # AWS SDK for python
    s3 = boto3.client('s3')
    resource = boto3.resource('s3')

    # get bucket
    bucket_name = 'recommendersystemdata'
    my_bucket = resource.Bucket(bucket_name)

    # read in input data and article data
    data_name = 'insurance_help_article_data_final.csv'
    data_obj = s3.get_object(Bucket = bucket_name, Key = data_name)

    user_input = event["queryStringParameters"]['query']
    print('User input: ' , user_input)

    # if nothing is said (i.e. '') then return a query for 'general insurance topics'
    if(user_input.strip() == "''"):
        user_input = 'general insurance topics'

    df = pd.read_csv(data_obj['Body'])
    print('Successfully downloaded dataset')
    
    result_by_title = {}

    new_input = [df.shape[0]+1, user_input, '','']
    df.loc[df.shape[0]] = new_input

    df['stemmed_title'] = getStem(df['title'])
    cos_sim_matrix = computeSimilarities(df['stemmed_title'])
    ranked_docs = rankDocuments(df, cos_sim_matrix)
    recommendation = recommend(df, df.shape[0], ranked_docs)

    # save to dictionary
    result_by_title['utterance'] = user_input
    result_by_title['articles'] = recommendation
        
    # remove current query from dataframe
    df = df.drop(df.index[len(df)-1])
    df = df.drop('stemmed_title', 1)
    # print('Here are the results: ', result_by_title)

    # for doc in result_by_title:
    #     print('Query:', user_input)
    #     for num in result_by_title[doc]:
    #         for r in result_by_title[doc][num]:
    #             print(result_by_title[doc][num][r])
    #         print()
    #     print()

    # need to make sure you return a dictionary to json.dumps
    return({'statusCode': 200, 'body': json.dumps({'result': result_by_title})})

# test locally
if __name__ == "__handler__":
  handler('health insurance', '')