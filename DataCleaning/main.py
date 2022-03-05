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


