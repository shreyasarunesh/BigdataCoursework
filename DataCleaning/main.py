import pandas as pd
import numpy as np
from unidecode import unidecode
import re
import os

"""Load original CSV files """
actors = pd.read_csv(os.getcwd()+"/imdb/actors.csv", delimiter=';')
directors = pd.read_csv(os.getcwd()+ "/imdb/directors.csv", delimiter=';')
moviestodirectors = pd.read_csv(os.getcwd()+ "/imdb/moviestodirectors.csv", delimiter=';')
ratings = pd.read_csv(os.getcwd()+ "/imdb/ratings.csv", delimiter=';')
writers = pd.read_csv(os.getcwd()+ "/imdb/writers.csv", delimiter=';')
movies = pd.read_csv(os.getcwd()+ "/imdb/movies.csv", delimiter=';')
moviestoactors = pd.read_csv(os.getcwd()+ "/imdb/moviestoactors.csv", delimiter=';')
moviestowriters =  pd.read_csv(os.getcwd()+ "/imdb/moviestowriters.csv", delimiter=';')
runningtimes = pd.read_csv(os.getcwd()+ "/imdb/runningtimes.csv", delimiter=';')


# cleanig actors table
#unidecode data
actors["name"] = actors["name"].apply(unidecode)
# remove patterns and special charecters
def remove_special_charecter(item):
    item = re.sub(r'[-]',r' ',item)
    item = re.sub(r'[^a-zA-Z0-9 ]',r'',item)
    item = item.replace("Jr","")
    return item

#split name into first name and last name
def split_name(name):
    f_name = name
    l_name = ""
    if(',' in f_name):
        l_name, f_name = f_name.split(', ')
        if( ' ' in f_name):
            f_name = f_name.split(' ')[0]
        elif(' ' in l_name):
            l_name = l_name.split(' ')[1]
    elif( ' (' in f_name):
        f_name = f_name.split(' (')[0]

    f_name = remove_special_charecter(f_name)
    l_name = remove_special_charecter(l_name)
    if(f_name == ""):
        return [l_name,f_name]
    else:
        return [f_name,l_name]


actors_names = (actors.drop_duplicates(keep= "first")).name.apply(split_name)
# add column fname to store first name
actors['fname'] = np.array([i[0] for i in actors_names]).T
# add column lname to store last name
actors['lname'] = np.array([i[1] for i in actors_names]).T
# export the data to csv
actors.to_csv(os.getcwd()+ "/Cleaned_Dataset/actors.csv",index=False)


# Director data cleaning
director_names = (directors.drop_duplicates(keep= "first")).name.apply(split_name)
# add column fname to store first name
directors['fname'] = np.array([i[0] for i in director_names]).T
# add column lname to store last name
directors['lname'] = np.array([i[1] for i in director_names]).T
# export the data to csv
directors.to_csv(os.getcwd()+ "/Cleaned_Dataset/directors.csv",index=False)


# Movie data cleaning

#unidecode data
movies["title"] = (movies.drop_duplicates(keep= "first"))["title"].apply(unidecode)
# extract only title
movies["title"] = movies["title"].apply(lambda each_title: each_title.split(" (")[0])
# remove ' in the title
movies["title"] = movies["title"].apply(lambda each_title: each_title.replace("'","") if each_title.count("'") == 2 else each_title)
# export the data to csv
movies.to_csv(os.getcwd()+"/Cleaned_Dataset/movies.csv",index=False)


# cleaning writers
# extract only fname and lname from name
def splitName(name):
    name = unidecode(name)
    f_name = l_name = ""
    if "," in name :
        f_name, l_name = name.split(",")
    l_name = re.sub(r"[.']",r' ',l_name.split(' (')[0])
    f_name = f_name.replace("Jr.","")
    return [f_name,l_name]

names = (writers.drop_duplicates(keep= "first")).name.apply(splitName)
# add column fname to store first name
writers['fname'] = np.array([i[0] for i in names]).T
# add column fname to store last name
writers['lname'] = np.array([i[1] for i in names]).T
# export the data to csv
writers.to_csv(os.getcwd()+"/Cleaned_Dataset/writers.csv",index=False)



# cleaning movie-to-writers
# remove special charecters and unwanted data
def remove_special_charecters(item):
    item = unidecode(str(item))
    if "(" in item : item = (item.split("(")[1]).split(')')[0]
    if '" ' in item : item = item.split('" ')[1]
    if ' "' in item : item = item.split(' "')[0]
    if ': ' in item : item = item.split(': ')[0]
    if ',' in item : item = item.split(',')[0]
    if "as " in item or item == 'by' or item == 'nan' : item = ""
    if re.search(r'^<',item) : item = ""
    item = re.sub(r'[^a-zA-Z ]',r'',item)
    return item

moviestowriters["additions"] = moviestowriters.addition.apply(remove_special_charecters)
# export the data to csv
moviestowriters.to_csv(os.getcwd()+"/Cleaned_Dataset/moviestowriters.csv",index=False)





# cleaning movie-to-directors
# export the data to csv
moviestodirectors.to_csv(os.getcwd()+"/Cleaned_Dataset/moviestodirectors.csv",index=False)


# cleaning runningtimes
# remove special characters form time column
runningtimes.time = runningtimes.time.apply(lambda item: re.sub(r'[A-Za-z:]',r'',item))
# remove special characters form addition1 column and store it in a new column "addition1"
runningtimes['addition1'] = runningtimes.addition.apply(lambda item: unidecode(re.sub(r'[):(]',r'',item)) if str(item) != 'nan' else
"")
# export the data to csv
runningtimes.to_csv(os.getcwd()+"/Cleaned_Dataset/runningtimes.csv",index=False)


# cleaning rating
# remove special charecters and preceeding numbers
def formatNumber(num):
    if len(str(num)) != 0 and str(num) != 'nan':
        num = int(re.sub(r'[.]', r'', str(num)))
    else: num =0
    return  num


ratings['distributionNumber'] = ratings.distribution.apply(formatNumber)
# export the data to csv
ratings.to_csv(os.getcwd()+"/Cleaned_Dataset/ratings.csv",index=False)