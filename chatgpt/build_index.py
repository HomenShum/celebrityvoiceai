import openai
import json
import textwrap


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\openaiapikey.txt')

def gpt3_embedding(content, engine='text-similarity-ada-001'):
    response = openai.Embedding.create(input=content,engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector

if __name__ == '__main__':
    alltext = open_file(r"C:\Users\hshum\OneDrive\Desktop\Python\CelebrityVoicesAI\chatgpt\input.txt")
    chunks = textwrap.wrap(alltext, 4000) # 4000 is the max number of tokens GPT-3 can handle
    result = list() 
    for chunk in chunks:
        embedding = gpt3_embedding(chunk.encode(encoding='ASCII',errors='ignore').decode()) # encode and decode to remove non-ascii characters, GPT-3 usually faces encoding problems 
        info = {'content': chunk, 'vector': embedding}
        print(info, '\n\n\n')
        result.append({'content': chunk, 'vector': embedding})
    with open('C:\\Users\\hshum\\OneDrive\\Desktop\\Python\\CelebrityVoicesAI\\chatgpt\\index.json', 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, indent=2) # save the index to a file
    ### next step: build unique index.json files for unique personas that the user selected to speak to
    ### take the value from the submit button and use it to name the index.json file
    ### then, use the name of the index.json file to load the correct index.json file for the persona
    