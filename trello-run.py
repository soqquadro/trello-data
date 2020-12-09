from src import board_data, card_dt, date_last, lst_name, get_points, card_dict, card_mov_simple

import pandas as pd

credentials = {"key":"yourkey"
               ,"token":"yourtoken"}
board = "yourboard"

input_date = str(input('please insert date ddmmyy: '))

cards_lst = board_data(board,'cards',credentials)

print('Processing cards movements...')

# Extract movements of each card
lst_all_actions = list()

for i in cards_lst:
    lst_all_actions.append(card_mov_simple(i['id'],credentials))
    
# filter only cards where movements took place
lst_actions = [i for i in lst_all_actions if len(i) > 0]

all_cards = list()
for l in lst_actions:
    all_cards.append(card_dict(l))

df_trello = pd.DataFrame(all_cards)

# Make a list of all of the columns in the df and rework it
cols = list(df_trello.columns.values) 

# Reorder also mostly important date columns
new_list_columns = cols

# Create dataframe

df_trello = df_trello[[new_list_columns]]

# Export dataframe

df_trello.to_excel('trello_'+input_date+'.xlsx')
