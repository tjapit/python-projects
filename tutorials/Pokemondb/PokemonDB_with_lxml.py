import requests             # Web page requester
import lxml.html as lh      # HTML Parser
import openpyxl             # Excel shit
import pandas as pd
import time

#Initialize URL to scrape
url = 'https://pokemondb.net/pokedex/all'

###CHECK IF INFORMATION IS ONLY FROM TABLE

#Create a handle, page, to handle the contents of the website
page = requests.get(url)

#Store the contents of the website under doc
doc = lh.fromstring(page.content)

#Parse data that are stored between <tr>..</tr> of the site's HTML code
tr_elements = doc.xpath('//tr')

#Check the length of the first 12 rows to see if information is only from table
print([len(row) for row in tr_elements[:12]])

###FIRST ROW AS HEADER

#Create empty list
col = []
i = 0

#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name = t.text_content()
    print('%d   : "%s"' % (i, name))
    col.append((name, []))      #col is a list of tuples that in itself contains a header and an empty list
    time.sleep(.25)

###POPULATING THE LISTS INSIDE THE TUPLES WITH DATA

#Since our first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    #T is our j'th row
    T = tr_elements[j]

    #If row is not of size 10, the //tr data is not from our table
    if len(T) != 10:
        break

    #i is the index of our column
    i = 0

    #Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        #Skipping the first cells/column (dex entry number) from being turned into integers
        if i>0:
        #Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

#Checking length of each column. Ideally, they should all be the same.
print([len(C) for (title,C) in col])

# ###Picking out a Total Stat from a specific pokemon in the list in the tuples within the giant list
#
# #Row at which the desired data resides
# cond = 'Fairy'                 # Condition
# wanted = []                    # Results with desired Condition
#
# for j in range(len(col[0][1])):
#     poke_type = col[2][1][j]
#     poke_entry = col[0][1][j]
#     if poke_type==cond:
#         wanted.append(poke_entry)

###DATA FRAME WITH PANDAS

# Converting data to a dictionary that can be understood by panda
Dict = {title:column for (title,column) in col}

# Converting dictionary to a table using pandas
df = pd.DataFrame(Dict)


## CLEANING DATA (Name and Type)
def str_bracket(word):
    '''Add brackets around second term'''
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = ' ' + list[char_ind]
    fin_list = ''.join(list).split(' ')
    length = len(fin_list)
    if length>1:
        fin_list.insert(1, '(')
        fin_list.append(')')
    return ' '.join(fin_list)

def str_break(word):
    '''Break strings at upper case'''
    list = [x for x in word]
    for i in range(1, len(list)):
        if list[i].isupper():
            list[i] = ' ' + list[i]
    fin_list = ''.join(list).split(' ')
    return fin_list

# Testing functions
test_word = 'ILovePokemon'
print(str_bracket(test_word))
print(str_break(test_word))

# Apply functions to Name and Type in the data frame
df['Name'] = df['Name'].apply(str_bracket)
df['Type'] = df['Type'].apply(str_break)


## STORING DATA
# Backing up Data Frame to a .JSON file
df.to_json('PokemonData.json')

# Checking if data is properly backed up by opening the .json file
df = pd.read_json('PokemonData.json')
df = df.set_index(['#'])
df.head()


## STATISTICAL ANALYSIS





