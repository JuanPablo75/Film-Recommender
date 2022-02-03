import requests
import json


def get_movies_from_tastedive(movie):
    baseurl = 'https://tastedive.com/api/similar'

    params_dict = {}
    params_dict['q'] = movie
    params_dict['type'] = 'movies'
    params_dict['limit'] = 5
    this_page_cache = requests.get(baseurl, params = params_dict)#_with_caching.get(baseurl, params=params_dict)
    return json.loads(this_page_cache.text)

print(get_movies_from_tastedive('Thor'))

def extract_movie_titles(dic):
    return ([i['Name'] for i in dic['Similar']['Results']])


def get_related_titles(m_list):
    lst = []
    for i in m_list:
        lst.extend(extract_movie_titles(get_movies_from_tastedive(i)))
    return list(set(lst))


def get_movie_data(title):
    url = 'http://www.omdbapi.com/?i=tt3896198&apikey=6f013edc'
    param = {}
    param['t'] = title
    param['r'] = 'json'

    this_page_cache = requests.get(url, params=param)#_with_caching.get(url, params=param)
    print(this_page_cache.text)
    return json.loads(this_page_cache.text)

def get_movie_rating(dic):

    for i in dic['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':

            return int(i['Value'][:-1])
    return 0

thorData = get_movie_data('Thor')
print(get_movie_rating(thorData))

def get_sorted_recommendations(movie_lst):
    new_recomm_list = get_related_titles(movie_lst)
    new_dict = {}
    for i in new_recomm_list:
        rating = get_movie_rating(get_movie_data(i))
        new_dict[i] = rating
    print(new_dict)
    print(new_recomm_list)
    # print([i for i in sorted(new_dict, key=lambda x: new_dict[x], reverse=True)])
    return [i for i in sorted(new_dict, key=lambda x: new_dict[x], reverse=True)]

# get_sorted_recommendations(['Thor','Batman'])
inpt = input('Give me a list of films and I will show you back some recommended films.').split(',')

get_sorted_recommendations(inpt)
