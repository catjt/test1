from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

#cargar el dataset
df = pd.read_csv('PI_ETL.csv')

@app.get("/")
def index ():
    return {"message":'Movie Recommender Project'}

# Request 1
@app.get('/get_collection_revenue/{collection}')
def get_collection_revenue(collection:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''

    movie_count = (df[df['belongs_to_collection']==collection]).shape[0]
    budget_btc = (df[df['belongs_to_collection']==collection])['budget']
    revenue_btc = (df[df['belongs_to_collection']==collection])['revenue']
    total_revenue = revenue_btc.sum() - budget_btc.sum() 
    revenue_average = total_revenue / movie_count
    return {'Collection':collection, 'Total Movies':movie_count,'Total Revenue': int(total_revenue), 'Revenue Average': int(revenue_average)}

# Request 2
@app.get('/get_country/{country}/{year}')
def get_country(year:int, country:str):
    '''Ingresas el pais y año, retornando la cantidad de peliculas producidas en ese año'''

    filtered_df = df[(df['release_year'] == year) & (df['production_countries'] == country)]
    total_movies = filtered_df.shape[0]
    return {'country':country, 'total_movies': total_movies}

# Request 3
@app.get('/company_revenue/{company}')
def company_revenue(company:str):
    '''Ingresas la productora, retornando la ganancia toal y la cantidad de peliculas que produjeron'''

    total_revenue = (df[(df['production_companies']==company)])['revenue'].sum()
    movie_count = (df[df['production_companies']==company]).shape[0]
    return {'company':str(company), 'total_revenue':int(total_revenue), 'total_movies':int(movie_count)}

# Request 4
@app.get('/min_budget/{year}')
def min_budget(year:int):
    '''Ingresas el anio, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo'''

    filtered_year = df[(df['release_year'] == year) & (df['budget'] > 0)]
    if filtered_year.empty:
            return print('No valid budget found for', year, 'year') 
    min_budget_row = filtered_year.loc[filtered_year['budget'].idxmin()]
    title = min_budget_row['title']
    budget = min_budget_row['budget']
    return {'title': title, 'year': year, 'budget': budget}

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    return {'lista recomendada': respuesta}