import pandas as pd
import sqlite3

def load_and_preprocess_csv(csv_url):
    df = pd.read_csv(csv_url, skiprows=8, skipfooter=5, engine='python', encoding='latin1', on_bad_lines='skip', delimiter=';')
    df.columns = df.columns.str.strip()
    columns_to_select = ['2024', 'Januar', 'NST7-011', 'Getreide', 'Schleswig-Holstein', '278', '278.1']
    df = df[columns_to_select]
    df.columns = ['year', 'month', 'goods_id', 'goods_name', 'goods_source', 'abroad', 'total']    
    return df

def clean_data(df):
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    df['abroad'] = pd.to_numeric(df['abroad'], errors='coerce').astype('Int64')
    df['total'] = pd.to_numeric(df['total'], errors='coerce').astype('Int64')

    german_months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    df['month'] = df['month'].apply(lambda x: x if x in german_months else None)

    df['goods_id'] = df['goods_id'].apply(lambda x: x if pd.notnull(x) and x.startswith('NST7-') else None)
    df.dropna(inplace=True)
    return df

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS goods (
        year INTEGER,
        month TEXT,
        goods_id TEXT,
        goods_name TEXT,
        goods_source TEXT,
        abroad INTEGER,
        total INTEGER
    )
    ''')
    
    return conn, cur

def insert_data_to_db(df, conn):
    df.to_sql('goods', conn, if_exists='replace', index=False, dtype={
        'year': 'BIGINT',
        'month': 'TEXT',
        'goods_id': 'TEXT',
        'goods_name': 'TEXT',
        'goods_source': 'TEXT',
        'abroad': 'BIGINT',
        'total': 'BIGINT'
    })
    conn.commit()
    conn.close()

def main():
    csv_url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46131-0014_00.csv"
    df = load_and_preprocess_csv(csv_url)
    df = clean_data(df)
    conn, cur = create_database("goodsTransportedByTrain.sqlite")
    insert_data_to_db(df, conn)
    print("Data pipeline executed successfully.")

if __name__ == "__main__":
    main()
