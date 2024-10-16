import os
from pathlib import Path
import logging   #inbuild module inside python

#logging string usually follow
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

#(forword path/) for mac and linux and (\)backward pass for window
list_of_files=[
    "src/__init__.py",     
    "src/helper.py",
    "src/prompt/py",
    ".env",
    "setup.py",
    "research/trials.ipynb",
    "app.py",
    "store_index.py",
    "static/.gitkeep",#for flask
    "templates/chat.html",
    "test.py"

]

#how to create all this files -->shown below
#writing the code for that
for filepath in list_of_files:
    filepath=Path(filepath) #convert filepath into path

     # separate folder and file
    filedir,filename=os.path.split(filepath)
    

    #if file directory is not empty then create file directory
    if filedir !="":
       os.makedirs(filedir,exist_ok=True)  #exits_ok if we give then if dir is exist then if will not replace it or create it

        #log the information
    logging.info(f"Creating directory ;{filedir} for the file {filename}")
     
     #now create the file inside folder
     #if not created then create it and also check the size
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
         with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file:{filepath}")

    #if created then it will show this
    else:
       logging.info(f"{filename} is already created")
