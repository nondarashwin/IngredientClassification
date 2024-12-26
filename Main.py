#!/usr/bin/env python
# coding: utf-8

# # Header Files

# In[1]:


import pandas as pd
import pickle
from sklearn import preprocessing
from difflib import get_close_matches
from sklearn.neighbors import KNeighborsClassifier


# ### Preprocessing

# In[2]:


data=pd.read_csv('data.csv')
ingredients=data['ingredients']
cuisine=data['cuisine']
clusters=len(ingredients)
data_model=[]
for i in range(len(cuisine)):  
    a=data['ingredients'][i]
    a=a[1:-1]
    c=a.split(',')
    #c_strip=[]
    for j in c:
        b=j.replace(" ","")
        b=b.strip('\'')
        b=b.lower()
        #print(b)
        if(b!=""):
            data_model.append([b,cuisine[i]])


# In[3]:


data_model=pd.DataFrame(data_model,columns=['Ingredient','Cuisine'])
data_model


# below cell is to just check spelling mistakes in Ingredient

# In[4]:


from difflib import get_close_matches
types=list(set(data_model['Ingredient']))
for i in types:
    print(get_close_matches(i,types))


# In[5]:


le = preprocessing.LabelEncoder()
le.fit(data_model.Ingredient)
data_model['Ingredient']=le.transform(data_model['Ingredient'])


# In[6]:


data_model


# ### Classifier

# In[7]:


a=KNeighborsClassifier(n_neighbors=50,weights='distance',metric='manhattan')
model=a.fit(pd.DataFrame(data_model['Ingredient']),data_model['Cuisine'])
pickle.dump(model,open('KNN.pkl','wb'))
pickle.dump(le,open('I_transformer.pkl','wb'))


# In[8]:


count=0
n=len(data_model)
labels=model.classes_
for i in range(n):
    #k=le.inverse_transform(['banana'])
    prob_a=model.predict_proba([[data_model['Ingredient'][i]]])[0]
    predicted=[]
    for j in range(len(prob_a)):
        if(prob_a[j]>0.0):
            predicted.append(labels[j])
    nearer=set(data_model.Cuisine[data_model['Cuisine']==data_model['Cuisine'][i]])
    print(nearer & set(predicted))
    print('****')
    if(len(nearer&set(predicted))>0):
        count+=1   


# In[9]:


count*100/n


# In[64]:


from difflib import get_close_matches
def predict(ingredient):
    message=''
    n=len(ingredient)
    le=pickle.load(open('I_transformer.pkl', 'rb'))
    model=pickle.load(open('KNN.pkl', 'rb'))
    le_ingredient=le.classes_
    labels=model.classes_
    for i in range(n):
        print(ingredient[i])
        ingredient[i]=ingredient[i].lower()
        if(ingredient[i].lower() not in le_ingredient):
            print('True')
            c=get_close_matches(ingredient[i],le_ingredient)
            if(len(c)==0):
                messages=ingredient[i]+' not found'
                ingredient[i]=''
            else:
                #print(c[0])
                message=c[0]+' instead of '+ingredient[i]
                ingredient[i]=c[0]
    recipes=dict()
    for i in ingredient:
        #print(i)
        #print(le.transform([i]))
        if(i !=''):
            prob_a=model.predict_proba([le.transform([i])])[0]
            predicted=[]
            for j in range(len(prob_a)):
                if(prob_a[j]>0.0):
                    if(labels[j] in recipes.keys()):
                        recipes[labels[j]]+=1
                    else:
                        recipes[labels[j]]=1
    return recipes,message


# In[65]:


predict(['mint','cashw'])


# In[9]:


set(list(data.ingredients))


# In[11]:


def train():
    data=pd.read_csv('data.csv')
    ingredients=data['ingredients']
    cuisine=data['cuisine']
    clusters=len(ingredients)
    data_model=[]
    for i in range(len(cuisine)):  
        a=data['ingredients'][i]
        a=a[1:-1]
        c=a.split(',')
        #c_strip=[]
        for j in c:
            b=j.replace(" ","")
            b=b.strip('\'')
            b=b.lower()
            #print(b)
            if(b!=""):
                data_model.append([b,cuisine[i]])
    data_model=pd.DataFrame(data_model,columns=['Ingredient','Cuisine'])
    le = preprocessing.LabelEncoder()
    print(data_model)
    le.fit(data_model.Ingredient)
    print(le.classes_)
    data_model['Ingredient']=le.transform(data_model['Ingredient'])
    a=KNeighborsClassifier(n_neighbors=50,weights='distance',metric='manhattan')
    model=a.fit(pd.DataFrame(data_model['Ingredient']),data_model['Cuisine'])
    pickle.dump(model,open('KNN.pkl','wb'))
    pickle.dump(le,open('I_transformer.pkl','wb'))


# In[12]:


train()


# In[ ]:




