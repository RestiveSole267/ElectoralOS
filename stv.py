# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15AmUfmVs9AmH-J_p-fYWwr63yz5FS8H7
"""

import pandas as pd
import re

#To use import data from Google
from google.colab import auth
import gspread
from oauth2client.client import GoogleCredentials

#To visualize Sankey Diagram
import plotly
import plotly.graph_objects as go
import matplotlib.pyplot as plt

auth.authenticate_user()

import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())

#worksheet = gc.open('Your spreadsheet name').sheet1
wb = gc.open_by_url('https://docs.google.com/spreadsheets/d/1yHVsWdtoE2HgjQUWMgsLwMJ8rzrOlMLfSingiXXKVp0/edit?resourcekey#gid=2037158102')

# get_all_values gives a list of rows.
wb = wb.worksheet('Form Responses 1')
rows = wb.get_all_values()

# Convert to a DataFrame and render.
df = pd.DataFrame.from_records(rows)

new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header
df = df.iloc[:,1:] # Remove time stamp

#Convert votes to int
for col in df.columns:
  df[col] = df[col].astype(int)

df

# Convert Rows into DataFrame and clean data

# Convert to a DataFrame and render.
df = pd.DataFrame.from_records(rows)

new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header
df = df.iloc[:,1:] # Remove time stamp

#Convert votes to int
for col in df.columns:
  df[col] = pd.to_numeric(df[col])
#Change column names to candidate
votes = []
for col in df.columns: 
  name = col[37:-1]
  votes.append(name)
df.columns = votes
df = df.reset_index().iloc[:,1:]


df

#Create Data Frame where results will be stored
results = []
vote_rounds = pd.DataFrame()

df_t = df.transpose() # Change rows and columns to have voters as columns
for col in df_t.columns:
  top_choice = df_t[col].min() #Choose their Top Canidate
  top_candidate = df_t[df_t[col] == top_choice].index.tolist()[0]
  results.append(top_candidate)

vote_rounds[0] = results
vote_rounds

left_voters = []
losers = []
for r in range(1,df.shape[1]-1):
  #Stop loop when there are already two candidates
  if vote_rounds[r-1].nunique() == 2: 
    break

  #Start the new voting round
  vote_rounds[r] = vote_rounds[r-1]

  #FInd out who are the potential losers
  aggre = pd.DataFrame(vote_rounds[r-1].value_counts())
  min_vote = aggre[r-1].min()
  potential_losers = aggre[aggre[r-1] == min_vote].index.tolist()
  least_votes = df[potential_losers].sum().max()
  potential_losers_df = df[potential_losers]

  #Choose loser based on worse overall ranking (sum of ranking):
  sum_votes = pd.DataFrame(potential_losers_df.sum())
  least_ranking = sum_votes[0].max()
  loser = sum_votes[sum_votes[0] == least_ranking].index.tolist()[0]
  print(f'Loser of round {r} is {loser}')
  losers.append(loser)

  #Determining who their votes go to
  voters_non_selected = df[df[loser] == 1].index.tolist()
  for voter in voters_non_selected: 
    left_voters.append(voter)
  
  votes_to_distribute = df.iloc[list(set(left_voters)),:]
  votes_to_distribute = votes_to_distribute.loc[:, ~votes_to_distribute.columns.isin(losers)]
  votes_to_distribute_t = votes_to_distribute.transpose()
  for votr in votes_to_distribute_t.columns:
    nxt_choice = votes_to_distribute_t[votr].min()
    vote_goes_to = votes_to_distribute_t[votes_to_distribute_t[votr] == nxt_choice].index.tolist()[0]
    print(f'Vote goes to {vote_goes_to}')

    # Changing their votes
    vote_rounds.loc[votr,r] = vote_goes_to
  print('\n')

col_rounds = vote_rounds.columns.tolist()
vote_rounds['value'] = [1 for x in range(vote_rounds.shape[0])]
vote_rounds

# Selecting winner
final_count = pd.DataFrame(vote_rounds.iloc[:,-2:-1].value_counts()).reset_index()
final_count.columns = ['candidate','final_votes']
winner = final_count[final_count.final_votes == final_count.final_votes.max()]['candidate'].tolist()
if len(winner) > 1:
  print('There is a draw')
else:
  print(f'And the final winner is... {winner[0]} !')
final_count



df_sankey = vote_rounds.groupby(col_rounds).count().reset_index()
for col in col_rounds:
  df_sankey[col] = df_sankey[col] + str(col)
df_sankey

def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    
    '''
    https://gist.github.com/ken333135/09f8793fff5a6df28558b17e516f91ab
    '''
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig

sankey_title = 'Vote by Ranking'

sankey_fig = genSankey(df_sankey,cat_cols=col_rounds,value_cols='value',title=sankey_title)
#plotly.offline.plot(fig, validate=False)

fig = go.Figure(sankey_fig)
fig.update_layout(width=int(1200))

fig.add_annotation(
            x=0,
            y=1.1,
            showarrow= False,
            text="First round")

fig.add_annotation(
            x=1,
            y=1.1,
            showarrow= False,
            text="Final round")


fig.show()