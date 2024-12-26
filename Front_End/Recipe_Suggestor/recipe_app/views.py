from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage
from . import predict as p
from .models import content
from  .models import rating as rating_model
import shutil
import pandas as pd
import pickle
from sklearn import preprocessing
from difflib import get_close_matches
from sklearn.neighbors import KNeighborsClassifier
import os
def train():
    data=pd.read_csv('Data/data.csv')
    ingredients=data['ingredients']
    cuisine=data['cuisine']
    #clusters=len(ingredients)
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
            print(b)
            if(b!=""):
                data_model.append([b,cuisine[i]])
    data_model = pd.DataFrame(data_model, columns=['Ingredient', 'Cuisine'])
    le = preprocessing.LabelEncoder()
    le.fit(data_model.Ingredient)
    data_model['Ingredient']=le.transform(data_model['Ingredient'])
    a=KNeighborsClassifier(n_neighbors=50,weights='distance',metric='manhattan')
    model=a.fit(pd.DataFrame(data_model['Ingredient']),data_model['Cuisine'])
    pickle.dump(model,open('Data/KNN.pkl','wb'))
    pickle.dump(le,open('Data/I_transformer.pkl','wb'))
def ratings(requests,username):
    if requests.method == 'POST':
        user=requests.user.username
        rating=requests.POST.get('group3',False)
        if(rating_model.objects.filter(username=user,cuisine=username).exists()):
            value=rating_model.objects.get(username=user,cuisine=username)
            value.ratings=rating
            value.save()
        else:
            value=rating_model.objects.create(username=user,cuisine=username,ratings=rating)
            value.save()
        return redirect('/recipe/'+username)
    else:
        return  redirect('/recipe/'+username)
def register(requests):
    if requests.method == 'POST':
        name1 = requests.POST.get('name', False)
        username1 = requests.POST.get('username', False)
        email_id1 = requests.POST.get('emailid', False)
        password1 = requests.POST.get('password', False)
        cpassword1 = requests.POST.get('cpassword', False)
        if password1 == cpassword1:
            if User.objects.filter(username=username1).exists():
                messages.info(requests, "Username  Already Taken")
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username1, email=email_id1, password=password1,
                                                first_name=name1)
                user.save()
                return redirect('/')
        else:
            messages.info(requests, "Password dosen't match")
            return redirect('/register')
    else:
        if (requests.user.is_authenticated):
            if(requests.user.username=='admin'):
                return render(requests, 'home.html')
            else:
                return redirect('/')
        else:
            return render(requests, 'register.html')
# Create your views here.
def add(requests):
    if(requests.user.is_authenticated and requests.user.username=='admin'):
        if (requests.method == 'POST'):
            name = requests.POST.get('name', False)
            data = pd.read_csv('Data/data.csv')
            if (len(data.cuisine[data['cuisine'] == name]) > 0):
                return edit(requests, name)
            ingredient = requests.POST.get('ingredient', False)
            serves = requests.POST.get('serves', False)
            print(serves)
            calories = requests.POST.get('calories', False)
            print(calories)
            carbohydrates = requests.POST.get('carbohydrates', False)
            print(carbohydrates)
            fats = requests.POST.get('fats', False)
            print(fats)
            protein = requests.POST.get('proteins', False)
            print(protein)
            url = requests.POST.get('url', False)
            nutrition = "{serves:" + serves + ",calories:" + calories + ",carbohydrates:" + carbohydrates + ",fats:" + fats + ",proteins:" + protein + "}"
            ingredient = '[' + ingredient + ']'
            upload_file = requests.FILES['document']
            fs = FileSystemStorage()
            if ('.' in upload_file.name):
                fs.save(upload_file.name, upload_file)
                shutil.copyfile('media/' + upload_file.name, 'static/images/' + upload_file.name)
            else:
                messages.info(requests, "Not A Image File")
                return redirect('/add')
            data1 = pd.DataFrame([[0, name, ingredient, url, nutrition, upload_file.name]], columns=data.columns)
            data = pd.concat([data, data1])
            print(data[data['id'] == 0])
            data.to_csv('Data/data.csv', index=False)
            train()
            return redirect('/add')
        else:
                return render(requests, 'add.html')
    else:
        return redirect('/login')


def edit(requests, username):
    if (requests.user.is_authenticated and requests.user.username=='admin'):
        if (requests.method == 'POST'):
            ingredient = requests.POST.get('ingredient', False)
            serves = requests.POST.get('serves', False)
            print(serves)
            calories = requests.POST.get('calories', False)
            print(calories)
            carbohydrates = requests.POST.get('carbohydrates', False)
            print(carbohydrates)
            fats = requests.POST.get('fats', False)
            print(fats)
            protein = requests.POST.get('proteins', False)
            print(protein)
            url = requests.POST.get('url', False)
            nutrition = "{serves:" + serves + ",calories:" + calories + ",carbohydrates:" + carbohydrates + ",fats:" + fats + ",proteins:" + protein + "}"
            ingredient = '[' + ingredient + ']'
            data = pd.read_csv('Data/data.csv')
            data.ingredients[data['cuisine'] == username] = ingredient
            data.url[data['cuisine'] == username] = url
            data.nutrition[data['cuisine'] == username] = nutrition
            data.to_csv('Data/data.csv', index=False)
            train()
            return redirect('/home')
        else:
            data = pd.read_csv('Data/data.csv')
            data = data[data['cuisine'] == username].iloc[0]
            nutrition = data['nutrition'][1:-1]
            nutrition = nutrition.split(',')
            nut = []
            for i in nutrition:
                j = i.split(':')
                j[0] = j[0].strip('\'')
                print(j[1])
                nut.append(j)
            return render(requests, 'edit.html',
                          {'url': data['url'], 'calories': nut[1][1], 'carbohydrate': nut[2][1], 'fats': nut[3][1],
                           'proteins': nut[4][1], 'name': username, 'ingredient': data['ingredients'][1:-1],
                           'images': data['images'], 'serves': nut[0][1]})
    else:
        redirect('/login')


def admin(requests):
    if (requests.method == 'POST'):
        username1 = requests.POST.get('username', False)
        password1 = requests.POST.get('password', False)
        user = auth.authenticate(username=username1, password=password1)
        if user is not None:
            auth.login(requests, user)
            return redirect('/home')
        else:
            messages.info(requests, 'Invalid credentials')
            return redirect('/login')
    else:
        if (requests.user.is_authenticated):
            if(requests.user.username == 'admin'):
                return redirect('/home')
            else:
                return redirect('/')
        else:
            return render(requests, 'admin.html')


def logout(requests):
    auth.logout(requests)
    return redirect('/login')


def home(requests):
    if (requests.user.is_authenticated):
        if(requests.user.username=='admin'):
            data = pd.read_csv('Data/data.csv')
            data = data.drop(['url', 'ingredients', 'nutrition', 'id'], axis=1)
            k = []
            for i in range(len(data)):
                k.append(content(data.iloc[i]))
            return render(requests, 'home.html', {'data': k})
        else:
            return redirect('/')
    else:
        messages.info(requests, 'Login First')
        redirect('/login')


def detail(requests, username):
    rating_message='No Ratings'
    if (requests.user.is_authenticated):
        data = pd.read_csv('Data/data.csv')
        data = data[data['cuisine'] == username]
        print(data['cuisine'])
        print(data.columns)
        ingredient = list(data['ingredients'])[0][1:-1].split(',')
        for i in range(len(ingredient)):
            ingredient[i] = ingredient[i].replace('\'', '')
        nutrition = list(data['nutrition'])[0][1:-1].split(',')
        nutritions = dict()
        for i in nutrition:
            j = i.split(':')
            j[0] = j[0].strip(' ').strip('\'').strip('\'')
            print(j)
            nutritions[j[0]] = j[1]
        link = data.url[data['cuisine'] == username].iloc[0]
        rating=rating_model.objects.all().values()
        user=requests.user.username
        rates_user=0
        rates=0
        count=0
        for i in rating:
            if(i['cuisine']==username):
                rates+=i['ratings']
                count+=1
            if (i['cuisine'] == username and i['username']==user):
                rates_user=i['ratings']
        if(count>0):
            rating_message=str(rates/count)+"/5 ("+str(count)+")"
        images = '/static/images/' + data.images[data['cuisine'] == username].iloc[0]
        return render(requests, 'detail.html',{'range':[1,2,3,4,5],'user_rating':rates_user,'rating':rating_message,'name': username, 'ingredient': ingredient, 'nutrition': nutritions, 'link': link, 'images': images})
    else:
        return '/login'


def predict(requests, ingredient, name):
    message = ''
    n = len(ingredient)
    le = pickle.load(open('Data/I_transformer.pkl', 'rb'))
    model = pickle.load(open('Data/KNN.pkl', 'rb'))
    le_ingredient = le.classes_
    print(le_ingredient)
    labels = model.classes_
    for i in range(n):
        print(ingredient[i])
        ingredient[i] = ingredient[i].lower()
        if ingredient[i].lower() not in le_ingredient:
            print('True')
            c = get_close_matches(ingredient[i], le_ingredient)
            print(c)
            if len(c) == 0:
                message = ingredient[i] + ' not found'
                ingredient[i] = ''
            else:
                # print(c[0])
                message = message + c[0] + ' instead of ' + ingredient[i]
                ingredient[i] = c[0]
    recipes = dict()
    for i in ingredient:
        # print(i)
        # print(le.transform([i]))
        if (i != ''):
            prob_a = model.predict_proba([le.transform([i])])[0]
            predicted = []
            for j in range(len(prob_a)):
                if (prob_a[j] > 0.0):
                    if (labels[j] in recipes.keys()):
                        recipes[labels[j]] += 1
                    else:
                        recipes[labels[j]] = 1
    ab = []
    for i in recipes.keys():
        ab.append([recipes[i], i])
    ab.sort(reverse=True)
    recipes = dict()
    for i in ab:
        recipes[i[1]] = i[0]
    data = pd.read_csv('Data/data.csv')
    transfer = []
    # messages.info(requests,message)
    print(len(recipes))
    if len(recipes) == 0:
        print('True')
        print(message)
        messages.info(requests, message)
        return redirect('/')
    for recipe in recipes.keys():
        name = recipe
        rating = rating_model.objects.all().values()
        image = '/static/images/' + data.images[data['cuisine'] == recipe].iloc[0]
        link = '/recipe/' + recipe
        a = dict()
        a['name'] = name
        a['image'] = image
        a['link'] = link
        count=0
        rates=0
        for i in rating:
            if(i['cuisine']==name):
                rates+=i['ratings']
                count+=1
        if(count>0):
            a['ratings']=str(rates/count)+"/5 ("+str(count)+")"
        else:
            a['ratings']='No Ratings'
        transfer.append(a)
    return render(requests, 'recipe.html', {'recipes': transfer, 'message': message, 'ingredient': ingredient})
    # return HttpResponse((transfer,message))


def index(requests):
    if (requests.user.is_authenticated):
        return render(requests, 'index.html')
    else:
        return redirect('/login')


def byingredient(requests):
    if requests.user.is_authenticated:
        if requests.method == 'POST':
            ingredients = requests.POST.get('ingredient', False)
            ingredients = ingredients.split(',')
            print(ingredients)
            return predict(requests, ingredients, 'byingrdient')
        else:
            return redirect('/')
    else:
        return redirect('/login')


def upload(requests):
    if requests.user.is_authenticated:
        if requests.method == "POST":
            upload_file = requests.FILES['document']
            fs = FileSystemStorage()
            if '.' in upload_file.name:
                fs.save(upload_file.name, upload_file)
                return byimage(requests, upload_file.name)
            else:
                messages.info(requests, "Not A Image File")
                return redirect('/')
                # upload_file.name
    else:
        messages.info(requests, 'Please Login')
        return redirect('/')


def byimage(requests, filename):
    a = p.predictor(filename)
    return predict(requests, [a], 'byimage')
