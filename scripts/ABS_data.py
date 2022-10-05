#!/usr/bin/env python
# coding: utf-8

# In[77]:


import pandas as pd
from urllib.request import urlretrieve
import os
import matplotlib.pyplot as plt


# In[78]:


urls = ['https://www.abs.gov.au/statistics/people/population/regional-population-age-and-sex/2021/32350DS0001_2021.xlsx',        'https://www.abs.gov.au/statistics/people/population/deaths-australia/2020/33020DO005_2020.xlsx',        'https://www.abs.gov.au/statistics/people/education/schools/2021/Table%2035b%20Counts%20of%20all%20Schools%2C%202010-2021.xlsx']

names = ['age_sex', 'pop_deaths', 'education']


# In[79]:


# Setting PATH for downloads

output_relative_dir = '../data/raw/'
if not os.path.exists(output_relative_dir):
    os.makedirs(output_relative_dir)
    
# Creates abs_data folder within raw_data
if not os.path.exists(output_relative_dir + 'abs_data'):
    os.makedirs(output_relative_dir + 'abs_data')
    
abs_output_dir = output_relative_dir + 'abs_data'


# In[80]:


# Downloading the .xlsx files

i = 0
for url in urls:
    output_dir = f"{abs_output_dir}/{names[i]}.xlsx"
    print(f'File {i+1} started.')
    urlretrieve(url, output_dir)
    print(f'File {i+1} finished.')
    i += 1


# ## Reading in pop_deaths -
# 
# - `pop_deaths` contains information about the estimated resident population, recorded deaths and standardised death rate across each LGA
# - Sheet 2 contains VIC info

# In[81]:


df = pd.read_excel('../data/raw/abs_data/pop_deaths.xlsx', sheet_name = 2, skiprows = 4, header = [0,1], nrows = 129)[1:]
df = df.drop([(y, 'Standardised death rate.1') for y in range(2012, 2020)], axis=1)
df = df.drop([(y, 'Standardised death rate') for y in range(2012, 2021)], axis=1)
df.columns = [('LGA Code'), ('LGA Name')] + [','.join([str(c) for c in x]) for x in df.columns[2:]]
df2 = df.melt(id_vars=["LGA Code", "LGA Name"])
df2 = df2.dropna()
df2['value'] = df2.value.astype('int')
df2[['year','var']] = df2['variable'].str.split(',').tolist()
df2 = df2.sort_values('year')


# # How to make graph less noisy?
# 
# - Could sample 30-50 rows, show 3 visualisations + map 
# - Could only select areas (suburbs) of interest
# - Could show upper, middle and lower areas + map

# In[82]:


import seaborn as sns

df3 = df2.loc[df2['var'] == 'Estimated resident population']

sns.scatterplot(data = df3, x='year', y='value', hue='LGA Name')


# In[83]:


# Forecasting population

df3.groupby(['LGA Code', 'LGA Name'])['value'].apply(pd.Series.pct_change)


# # DF2 -
# 
# ### Contains:
# - Seperated by LGA
# - Data over 9 years [2012 - 2020] for estimated resident population and death count

# In[84]:


df2['variable'].unique()


# In[85]:


df3 = df2.loc[df2['var'] == 'Deaths']

sns.scatterplot(data = df3, x='year', y='value', hue='LGA Name')


# In[86]:


df2.to_csv('../data/curated/abs_data/pop_deaths_lga.csv')


# # age_sex (2021) -
# 
# - Contains information about the estimated resident population, binned by ages
# - 1st sheet males
# - 2nd sheet females
# - 3rd sheet combined
# - Seperated by SA2, not LGA
# - Sheets are not seperated by state, so will need to read all of them in and retain only VIC

# In[87]:


df = pd.read_excel('../data/raw/abs_data/pop_deaths.xlsx', sheet_name = 2, skiprows = 4, header = [0,1], nrows = 129)[1:]


# In[88]:


male_age = pd.read_excel('../data/raw/abs_data/age_sex.xlsx', sheet_name = 1, skiprows = 4, header = [0,1], nrows = 18692)[1:]
female_age = pd.read_excel('../data/raw/abs_data/age_sex.xlsx', sheet_name = 2, skiprows = 4, header = [0,1], nrows = 18692)[1:]
total_age = pd.read_excel('../data/raw/abs_data/age_sex.xlsx', sheet_name = 3, skiprows = 4, header = [0,1], nrows = 18692)[1:]


# In[89]:


male_columns = ['S/T code', 'S/T name', 'GCCSA code', 'GCCSA name', 'SA4 code', 'SA4 name', 'SA3 code', 'SA3 name', 'SA2 code', 'SA2 name',           '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',           '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85 and over', 'Total males']

female_columns = ['S/T code', 'S/T name', 'GCCSA code', 'GCCSA name', 'SA4 code', 'SA4 name', 'SA3 code', 'SA3 name', 'SA2 code', 'SA2 name',           '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',           '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85 and over', 'Total females']

total_columns = ['S/T code', 'S/T name', 'GCCSA code', 'GCCSA name', 'SA4 code', 'SA4 name', 'SA3 code', 'SA3 name', 'SA2 code', 'SA2 name',           '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',           '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85 and over', 'Total persons']


# In[90]:


male_age.columns = male_columns
male_age.drop(male_age.index[[0,1]], inplace = True)
#male_age.dropna(inplace = True)

female_age.columns = female_columns
female_age.drop(female_age.index[[0,1]], inplace = True)
#female_age.dropna(inplace = True)

total_age.columns = total_columns
total_age.drop(total_age.index[[0,1]], inplace = True)
#total_age.dropna(inplace = True)


# In[91]:


male_vic = male_age.loc[male_age['S/T name'] == 'Victoria']
female_vic = female_age.loc[female_age['S/T name'] == 'Victoria']
total_vic = total_age.loc[total_age['S/T name'] == 'Victoria']


# In[92]:


total_vic.columns


# In[93]:


total_vic.head()


# In[94]:


# male_vic.to_csv('../data/curated/abs_data/male_vic_pop_sa2.csv')


# # education

# In[95]:


df = pd.read_excel('../data/raw/abs_data/education.xlsx', sheet_name = 3, skiprows = 4)


# In[96]:


vic_education = df.loc[df['State/Territory'] == 'b Vic.']


# In[97]:


plt.plot(vic_education.groupby('Year')['School Count'].sum())
plt.xlabel('Year')
plt.ylabel('# of Active Schools in Victoria')
plt.show()


# In[98]:


vic_education.groupby('Year')['School Count'].sum()


# In[99]:


vic_education.head(25)


# In[100]:


vic_education.tail(25)


# In[101]:


years = []

for i in list(range(2010, 2022)):
    years.append(i)
    years.append(i)
    years.append(i)
    i += 1

years.reverse()


# In[ ]:





# In[102]:


affiliations = ['Government', 'Catholic', 'Independent']
school_aff = []
for year in years:
    for affiliation in affiliations:
        school_aff.append(affiliation)
    
school_aff = school_aff[:36]


# In[ ]:





# In[103]:


counts = []
school_counts = vic_education['School Count']

i = 0
for i in len(range(school_counts)):
    total = 0
    total += school_counts[i]
    i += 1
    


# In[ ]:





# In[ ]:


test = pd.DataFrame()


# In[ ]:


test['Year'] = years


# In[ ]:





# In[ ]:





# ## Have change in school (type) distribution over 11 years
# 
# - Compare to median house price over the 11 years
# - Can establish trend for schooling demographic + forecasting future median house price (based on schools) for 3 years as required
# - Could create regression model: y = median house price, X = [# of government, catholic, indept, etc schools]

# # The number of schools in Victoria has remained fairly constant over the 11 years
# 
# - Explore why

# In[ ]:


vic_education.groupby(by = 'Year').mean()


# In[ ]:





# In[ ]:





# # Naive approach - 
# ## Most liveable suburb == most expensive 

# In[ ]:


properties = pd.read_csv('../data/curated/2022-09-18 12_34_18.198964.csv')


# In[ ]:


properties.columns


# In[ ]:


properties


# ## Finding the most expensive suburbs -

# In[ ]:


properties.loc[properties['suburb'] == 'Sawmill Settlement']['address']


# In[ ]:


#df = properties[['sold_price', 'suburb']]
test = properties.groupby('suburb').mean().sort_values(by = 'sold_price')
test


# In[ ]:


expensive_10 = test[:10].index


# In[ ]:


expensive_10


# In[ ]:


# Change this when suburb conversion is available

lga = ['Kenebri', ]


# In[ ]:


df2.loc[df2['LGA Name']== 'Alpine (S)']


# In[ ]:


df2


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




