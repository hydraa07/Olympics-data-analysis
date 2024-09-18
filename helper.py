import pandas as pd
import numpy as np
import plotly

def medall_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Gold',
                                                                                             ascending=False).reset_index()

    medal_tally['TOtal'] = medal_tally['Bronze'] + medal_tally['Gold'] + medal_tally['Silver']

    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'All')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'All')

    return year,country




def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'All' and country == 'All':
        temp_df = medal_df

    if year == "All" and country != 'All':
        temp_df = medal_df[medal_df['region'] == country]
        flag = 1

    if year != 'All' and country == 'All':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'All' and country != 'All':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['TOtal'] = x['Bronze'] + x['Gold'] + x['Silver']
    return x


def data_over_time(df,col):
    nations_count = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_count.rename(columns={'count': col}, inplace=True)
    return nations_count


def most_successful(df, Sport):
    temp_df = df.dropna(subset=['Medal'])

    if Sport != 'All':
        temp_df = temp_df[temp_df['Sport'] == Sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x


def yearwise_medal_tally(df,Country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == Country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    # final_df
    return final_df

def Country_even_heatmap(df,Country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == Country]
    pt = new_df.pivot_table(index = 'Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)

    return pt


def most_successful_country(df, Country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == Country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

def men_women_comparison(df):
    a_df = df.drop_duplicates(subset = ['Name','region'])

    men = a_df[a_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    Women = a_df[a_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(Women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0,inplace=True)

    return final