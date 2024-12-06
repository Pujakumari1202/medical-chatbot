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

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_AP

#download the embeddings
embeddings=download_hugging_face_embeddings()

#Initializing the Pinecone
pinecone.init(api_key=PINECONE_API_KEY,
              environment=PINECONE_API_ENV)

#give index name
index_name="medichatbot"


# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})


llm = OpenAI(temperature=0.4, max_tokens=500)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')   #it will open the chat.html file


#final route
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"] #when user  will give msg . msg is taking in backedn
    input = msg #set the msg inninput variable
    print(input)  #print the msg
    response = rag_chain.invoke({"input": msg})   #sending the msg to qa object which we defind
    print("Response : ", response["answer"])  #give the response
    return str(response["answer"])  #response print in my terminal as well as send to my UI




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)