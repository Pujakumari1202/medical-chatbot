from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os

#initializing the flask
app=Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV=os.environ.get('PINECONE_API_ENV')


#download the embeddings
embeddings=download_hugging_face_embeddings()

#Initializing the Pinecone
pinecone.init(api_key=PINECONE_API_KEY,
              environment=PINECONE_API_ENV)

#give index name
index_name="medical--chatbot"


#loading the index
docsearch=Pinecone.from_existing_index(index_name,embeddings)

# creating the prompt template
PROMPT=PromptTemplate(template=prompt_template,input_variables=["context","question"])
chain_type_kwargs={"prompt":PROMPT}

#load my llama model and give the path
llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin"
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8
                          })


#create my qustion answer object amd it will give 2 answer
qa=RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k':2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs

)

@app.route("/")
def index():
    return render_template('chat.html')   #it will open the chat.html file

#final route
app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]  #when user  will give msg . msg is taking in backedn
    input = msg  #set the msg inninput variable
    print(input)  #print the msg
    result=qa({"query": input})  #sending the msg to qa object which we defind
    print("Response : ", result["result"])  #give the response
    return str(result["result"]) #response print in my terminal as well as send to my UI



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)