import requests
import pandas as pd
import sqlite3

data = requests.get("https://fakestoreapi.com/products").json()

df= pd.DataFrame(data)

df['product_rating'] = df['rating'].apply(lambda x: x['rate'])
df['product_count'] = df['rating'].apply(lambda x: x['count'])

final_df=df[['id','title','price','description','category','image','product_rating','product_count']]
conn = sqlite3.connect("products.db")

final_df.to_sql("products",
                conn,
                if_exists="replace",
                index=False)

tot_prod =  ''' 
            select count(*) from products
            '''
total_products = pd.read_sql(tot_prod,conn)
print(f"total products  {total_products}")

mep =   ''' 
        select * 
        from products
        where 
        price = (select max(price) from products)
        '''
most_expensive_product= pd.read_sql(mep,conn)
print(most_expensive_product)

apc =   '''
        select category,avg(price)
        from products
        group by category
        '''
average_price_per_category= pd.read_sql(apc,conn)
print(average_price_per_category)

report = average_price_per_category.to_csv("category_report.csv",index=False)
conn.close()

