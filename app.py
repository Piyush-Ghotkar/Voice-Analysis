#!/usr/bin/env python
# coding: utf-8

# In[16]:


from flask import Flask, jsonify, request
import os as os


# In[1]:


obj=__import__("my-voice-analysis")


# In[ ]:


from flask import Flask, jsonify, request
import pickle


# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])

def predict():
    # get data
    data = request.get_json(force=True)

    path=os.getcwd()

    # predictions
    #result = model.predict(data_df)

    # send back to browser
    #output = {'results': int(result[0])}
    output = {'results': path}
    
    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000, debug=True,use_reloader=False)


# In[ ]:




