

import pandas as pd
import os


# In[6]:


#Merging 12 months of sales data in one file


# In[39]:


df=pd.read_csv('.\Pandas-Data-Science-Tasks-master/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv')

files=[file for file in os.listdir('.\Pandas-Data-Science-Tasks-master/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/')]

all_months_data=pd.DataFrame()

for file in files:
    df=pd.read_csv('./Pandas-Data-Science-Tasks-master/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/'+file)
    all_months_data=pd.concat([all_months_data,df])
all_months_data.to_csv('all_data.csv',index=False)        


# In[40]:


all_data=pd.read_csv('all_data.csv')
all_data.head()


# In[48]:


nan_df=all_data[all_data.isna().any(axis=1)]
nan_df.head()


# In[77]:


all_data=all_data.dropna(how='all')
all_data.head()


# In[74]:


temp_df=all_data[all_data['Order Date'].str[0:2]=='Or']
all_data=all_data[all_data['Order Date'].str[0:2]!='Or']


# Convert columns to the correct type

# In[78]:


all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered']) #Make int 
all_data['Price Each']=pd.to_numeric(all_data['Price Each']) #Make Float 


# In[70]:


def fun(num):
    if(num[len(num)-1]=='/'):
        return str(num[0:len(num)-1])
    return num


# In[75]:


#Augment data with additional column
#Add month Column
all_data['Month']=all_data['Order Date'].str[0:2]
# print(type(all_data['Month'][0]))
all_data['Month']=all_data['Month'].apply(fun)
all_data['Month']=all_data['Month'].astype('int32')
all_data.head()


# In[79]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# Adding a City Column

# In[93]:


all_data['City']=all_data['Purchase Address'].apply(lambda x: x.split(',')[1]+' ('+ x.split(',')[2].split(' ')[1] +')' )
all_data.head()


# What was the best month for sales? How much was earned that month?

# In[81]:


results=all_data.groupby('Month').sum()


# In[85]:


import matplotlib.pyplot as plt

months=range(1,13)

plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# Which City has highest number of sales

# In[95]:


results=all_data.groupby('City').sum()
results


# In[102]:


cities=[city for city, df in all_data.groupby('City')]    
print(cities)
plt.bar(cities,results['Sales'])
plt.xticks(cities, rotation='vertical', size=9)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City Name')
plt.show()


# What time should we display advertisements to maximize likelihood of customer's buying product?

# In[105]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data['Hour']=all_data['Order Date'].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute
all_data['Count']=1
all_data.head()


# In[112]:


hours=[hour for hour,df in all_data.groupby('Hour')]
all_data.groupby(['Hour']).count()
plt.xticks(hours)
plt.grid()
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.plot(hours, all_data.groupby(['Hour']).count())


# What product are most often sold together?

# In[118]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()
df.head(20)


# In[120]:


from itertools import combinations
from collections import Counter

count=Counter()

for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))
print(count)    


# what product sold the most and the reason for it

# In[128]:


product_group=all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']

products=[product for product, df in product_group]

plt.bar(products,quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Products')
plt.xticks(products,rotation='vertical',size='9')

plt.show()


# In[138]:


prices=all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered)
ax2.plot(products, prices, 'g-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='b')
ax2.set_ylabel('Price($)', color='g')
ax1.set_xticklabels(products,rotation='vertical',size=8)

plt.show()


# In[ ]:




