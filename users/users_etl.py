import requests 
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Prakash%40123@localhost:5432/demo_db"
    )

def extract_data():
    url = "https://dummyjson.com/users"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['users']
    except Exception as e:
        print(f"API Error: {e}")
        return []
    
def transform_data(data):
    df= pd.DataFrame(data)
    df['city']=df['address'].apply(lambda x : x['city'])
    df['state']=df['address'].apply(lambda x : x['state'])
    df['company_name'] = df['company'].apply(lambda x: x['name'])
    df=df.rename(columns ={'firstName' : 'firstname','lastName':'lastname'})
    final_df=df[['id','firstname','lastname','age','gender','email','city',
                 'state','company_name']]
    return final_df

def load_data(final_df):
     final_df.to_sql("users",
                    engine,
                    if_exists="replace",
                    index=False) 
     print("data loaded into postgresql")

    

def analyze_data():

    queries = {
            'gender_distribution':'''
                                select
                                gender,count(*) as total
                                from users
                                group by gender
                                ''',
            'average_age_by_gender': '''
                                select
                                gender,avg(age) as average_age
                                from users
                                group by gender
                                ''',
            'top_10_oldest_users': '''
                                    select 
                                    firstname,lastname,age
                                    from users
                                    order by age desc
                                    limit 10
                                    ''',
            'users_by_state':'''
                            select 
                            count(*) as total_users,state
                            from users
                            group by state
                            '''

    }
    return queries


def main():
    data = extract_data()
    df=transform_data(data)
    load_data(df)
    queries = analyze_data()
    results={}

    for name,query in queries.items():
        read_df=pd.read_sql(query,engine)
        print(f"{name}")
        print(read_df)
        results[name]=read_df
    for name,df in results.items():
        df.to_csv(f"users/{name}.csv",index=False)
    engine.dispose()
main()