#Answer complex questions from an arbitrarily large sets of documents with vector search and GPT-3
#Summarize will lose a lot of information and is not recommended for long documents
#The more documents you have, the better the results will be

import openai
import json
import numpy as np
import textwrap
import re
from time import time, sleep
from numpy.linalg import norm 


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = open_file('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\openaiapikey.txt')

def gpt3_embedding(content, engine='text-embedding-ada-002'):
    content = content.encode(encoding='ASCII',errors='ignore').decode() #encode to ASCII then decode to prevent chatgpt errors
    response = openai.Embedding.create(input=content,engine=engine) # generate embedding data for documents/questions/user input
    vector = response['data'][0]['embedding']  # creates a vector containing the embedding data 
    return vector

def similarity(v1, v2):  # return dot product of two vectors
    return np.dot(v1, v2)/(norm(v1)*norm(v2)) #dot product is a measure of similarity between two vectors

def search_index(text, data, count=5):
    vector = gpt3_embedding(text) #get vector data for the question
    scores = list()
    for i in data:
        score = similarity(vector, i['vector']) #compare vector data for the question versus vector data for each document used to generate persona
        scores.append({'content': i['content'], 'score': score}) #create similarity scores for each document
    ordered = sorted(scores, key=lambda d: d['score'], reverse=True) #in scores list, sort 0th "score" data -to- last "score" data by highest to lowest
    return ordered[0:count] #return top 20 documents

    #database is longer than 10, if we have 10 chunks of 4000 characters long
    #then that is 40000 characters = 10000 tokens
    #problem: what if after searching, we have a larger corpus than we can feed gpt3 in one go?
    #solution: top 20 similar score chunks of text to answer the question; more specific the question, better the results
    
    #with that, we not have to create answer question function 
    #this requires prompt engineering 
    ###"use the following passage to give a detailed answer to the question; QUESTION; PASSAGE; DETAILED ANSWER"
    #after extracting info from larger doc, pair it down to the top 20 chunks
    #if answer is 200 tokens, 20 times 200 = 4000 tokens
    #for all 20 top chunk results, ask the same question, accumulate the answers, summarize into a single best answer
    #then use finetuned model to answer with celebrity persona's voice

def gpt3_completion(prompt, engine='text-davinci-003', temp=0.6, top_p=1.0, tokens=1600, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop) #generate response for the prompt
            text = response['choices'][0]['text'].strip()  # get the 0th choice of the text, strip whitespace
            text = re.sub('\s+', ' ', text) # replace multiple spaces with single space 
            filename = '%s_gpt3.txt' % time() #create a file with the time stamp
            with open('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\gpt3_logs/%s' % filename, 'w') as outfile: #create a file with the time stamp in the gpt3_logs folder
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text) #write the prompt and response to a file
            return text 
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

if __name__ == '__main__':
    with open('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\index.json', 'r') as infile:
        data = json.load(infile)
    # print(data)
    while True:
        query = input('Enter your question: ')
        # print(query)
        results = search_index(query, data)
        ##search broken - bug check
        ##print(results)
        ##exit(0)
        answers = list()
        #answer the same question for all returned chunks
        for result in results:
            prompt = open_file('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\prompt_answer.txt').replace('<<PASSAGE>>', result['content']).replace('<<QUERY>>', query)
            answer = gpt3_completion(prompt)
            print('\n\n', answer)
            answers.append(answer)
        # 4000 tokens limit, we can get up to 16000 characters answer after summarizing top 20 chunk answers
        # summarize the answers
        all_answers = '\n\n'.join(answers)
        chunks = textwrap.wrap(all_answers, 10000)
        final = list()
        for chunk in chunks:
            prompt = open_file('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\prompt_summary.txt').replace('<<SUMMARY>>', chunk)
            summary = gpt3_completion(prompt)
            final.append(summary)
        print('\n\n==========\n\n', '\n\n'.join(final))