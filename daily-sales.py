### CALLING THIS SCRIPT FROM A NODE.JS APP!  THIS MEANS THAT SOME PYTHON
### FUNCTIONS SUCH AS PRINT() THAT WRITE OUTPUT TO THE CONSOLE WILL CAUSE
### ERRORS WHEN NODE.JS TRIES TO READ THEM.

import pandas as pd
import re
import sys
import json
import os


### Data is not tabular
### Creating dataframe with way more columns than we'll need
### to avoid rows with different number of columns

bar_file = sys.argv[1]
kitchen_file = sys.argv[2]
#print(bar_file, type(bar_file))

bar_file = bar_file.replace('"', '')
kitchen_file = kitchen_file.replace('"', '')

results_filename = 'daily-sales-summary-2023-02-07-2023-02-08.csv'

bar_filepath = "uploads/" + bar_file
kitchen_filepath = "uploads/" + kitchen_file
#print(bar_filepath, type(bar_filepath))

# bar
df = pd.read_csv(bar_filepath, names = range(25))
# kitchen
k_df = pd.read_csv(kitchen_filepath, names = range(25))

pd.set_option('display.max_columns', 24)

#print(k_df.head(60))


### Get row "register" and columns "tip", "fees"
df[7] = df[7].astype('str')
df[7] = df[7].str.replace("$", "", regex=True)
df[10] = df[10].astype('str')
df[10] = df[10].str.replace("$", "", regex=True)

register = df.iloc[12, [7, 10]]
register = register.astype('float')
tip = register.iloc[0]
fees = register.iloc[1]


### Get rows "Point of Sale", "Square Online" and columns "tip", "fees"
k_df[7] = k_df[7].astype('str')
k_df[7] = k_df[7].str.replace("$", "", regex=True)
k_df[10] = k_df[10].astype('str')
k_df[10] = k_df[10].str.replace("$", "", regex=True)

point_of_sale = k_df.iloc[12, [7, 10]]
point_of_sale = point_of_sale.astype('float')
k_tip = point_of_sale.iloc[0]
k_fees = point_of_sale.iloc[1]
square_online = k_df.iloc[13, [7, 10]]
square_online = square_online.astype('float')
k_tip_online = square_online.iloc[0]
k_fees_online = square_online.iloc[1]

# Total kitchen tip and fees
k_total_tip = k_tip + k_tip_online
k_total_fees = k_fees + k_fees_online


#print(k_total_tip, k_total_fees)



### Sum Bar's "Net Total" from rows "Card - Dipped" through "Card - Other"
# There are two Net Totals, the Net Total we want is in column 9
# Rows are 18-23
card_net_total = df.iloc[18:24, [9]]

# Convert object to string, needed to include index for astype() to work 
# Remove "$" and "," from string  and convert string to float
card_net_total[9] = card_net_total[9].astype('str')
card_net_total[9] = card_net_total[9].str.replace("$", "", regex = True)
card_net_total[9] = card_net_total[9].str.replace(",", "", regex = True)
card_net_total[9] = card_net_total[9].astype('float')

card_net_total_sum = card_net_total[9].sum()
#print(card_net_total_sum)

### Kitchen "Net Total" from "Card - Dipped" through "Card - Other"
k_card_net_total = k_df.iloc[19:25, [9]]

k_card_net_total[9] = k_card_net_total[9].astype('str')
k_card_net_total[9] = k_card_net_total[9].str.replace("$", "", regex = True)
k_card_net_total[9] = k_card_net_total[9].str.replace(",", "", regex = True)
k_card_net_total[9] = k_card_net_total[9].astype('float')

k_card_net_total_sum = k_card_net_total[9].sum()
#print(k_card_net_total_sum)


### Get each bar name's cash row
### Convert columns 1 and 9 to string
### Find rows were column 1 is "Cash", column 9 has the values
df[1] = df[1].astype('str')
df[9] = df[9].astype('str')
df[9] = df[9].str.replace("$", "", regex = True)

# Just get rows where column 1 is 'Cash'
employee_cash_df = df[df[1] == 'Cash']

# Was going to sum each employees cash value, but 
# the zeitgeist - bar cash value appears to have that already
employee_cash_total = employee_cash_df.iloc[0:1,9]
employee_cash_total = employee_cash_total.astype('float')
employee_cash_total = employee_cash_total.values[0]
#print(employee_cash_total)

### Get each kitchen name's cash row
k_df[1] = k_df[1].astype('str')
k_df[9] = k_df[9].astype('str')
k_df[9] = k_df[9].str.replace("$", "", regex = True)

k_employee_cash_df = k_df[k_df[1] == 'Cash']

k_employee_cash_total = k_employee_cash_df.iloc[0:1,9]
k_employee_cash_total = k_employee_cash_total.astype('float')
k_employee_cash_total = k_employee_cash_total.values[0]


### Create new dataframe with 
### tip, fees, card_net_total_sum, employee_cash_total
bar_final = pd.DataFrame(columns=["tip", "fees", "card_net_total_sum", "employee_cash_total"], data=[[tip, fees, card_net_total_sum, employee_cash_total]], index = ["bar"])
#print(bar_final)

kitchen_final = pd.DataFrame(columns=["tip", "fees", "card_net_total_sum", "employee_cash_total"], data=[[k_total_tip, k_total_fees, k_card_net_total_sum, k_employee_cash_total]], index = ["kitchen"])
#print(kitchen_final)



### Combine into a single dataframe
both_df = [bar_final, kitchen_final]
  
final_df = pd.concat(both_df)
print(final_df)


### Write to CSV
final_df.to_csv(results_filename)  


