import requests
import pandas as pd
import sqlite3

def extract_data():
    e_data=requests.get("https://dummyjson.com/users").json()
    return e_data

def transform_data(data):
    df=pd.DataFrame(data)
    df['id']=df['users'].apply(lambda x : x['id'])
    df['firstName']=df['users'].apply(lambda x : x['firstName'])
    df['lastName']=df['users'].apply(lambda x : x['lastName'])
    df['age']=df['users'].apply(lambda x : x['age'])
    df['gender']=df['users'].apply(lambda x : x['gender'])
    df['email']=df['users'].apply(lambda x : x['email'])
    df['city']=df['users'].apply(lambda x : x['address']).apply(lambda x : x['city'])
    df['state']=df['users'].apply(lambda x : x['address']).apply(lambda x : x['state'])
    df['company_name'] = df['users'].apply(lambda x : x['company']).apply(lambda x: x['name'])
    final_df=df[['id','firstName','lastName','age','gender','email','city',
                 'state','company_name']]
    return final_df

def load_data(final_df):
    conn = sqlite3.connect("users.db")
    final_df.to_sql("users",
                            conn,
                            if_exists='replace',
                            index=False)
    return conn

def analyze_data(conn):

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
                                    firstName,lastName,age
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
    conn=load_data(df)
    queries = analyze_data(conn)
    results={}

    for name,query in queries.items():
        read_df=pd.read_sql(query,conn)
        print(f"{name}")
        print(read_df)
        results[name]=read_df
    results['gender_distribution'].to_csv("gender_distribution.csv",index=False)
    results['average_age_by_gender'].to_csv("average_age_by_gender.csv",index=False)
    results['top_10_oldest_users'].to_csv("top_10_oldest_users.csv",index=False)
    results['users_by_state'].to_csv("users_by_state.csv",index=False)
    conn.close()
main()





    

