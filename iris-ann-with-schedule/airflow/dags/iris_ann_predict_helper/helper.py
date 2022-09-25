import time
import datetime
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Float, Integer, DateTime


def generate_date_timestamp():
    for_date = datetime.datetime.now().astimezone().replace(microsecond=0)

    return f"{for_date}"


def generate_id_timestamp():
    current_time = time.time()
    time_obj = time.localtime(current_time)
    for_id = time.strftime("%Y%m%d", time_obj)
    
    return f"{for_id}"


def insert_tb_input(uri, table, data):
    df = pd.read_csv(data)
    data = df.to_dict('list')
  
    db = create_engine(uri)

    meta = MetaData()

    tb_target = Table(table, meta, 
        Column('id', Integer, primary_key = True), 
        Column('sepal_length', Float), 
        Column('sepal_width', Float),
        Column('petal_length', Float),
        Column('petal_width', Float),
    )

    conn = db.connect()
    
    for i in range(df.shape[0]):
        insert_data = tb_target.insert().values(
            sepal_length = data['sepal_length'][i], 
            sepal_width = data['sepal_width'][i],
            petal_length = data['petal_length'][i],
            petal_width = data['petal_width'][i]
        )

        conn.execute(insert_data)
    conn.close()


def query_all_tb_input(uri, table):
    db = create_engine(uri)

    meta = MetaData()

    tb_target = Table(table, meta, 
        Column('id', Integer, primary_key = True), 
        Column('sepal_length', Float), 
        Column('sepal_width', Float),
        Column('petal_length', Float),
        Column('petal_width', Float),
    )

    conn = db.connect()

    query_data = tb_target.select()
    conn = db.connect()
    result = conn.execute(query_data)

    data = []

    for row in result:
        data.append({
            'id': row[0],
            'sepal_length': row[1],
            'sepal_width': row[2],
            'petal_length': row[3],
            'petal_width': row[4]
        })

    return data


def insert_tb_output(uri, table, data):
    db = create_engine(uri)

    meta = MetaData()

    tb_target = Table(table, meta, 
        Column('executed_at', DateTime), 
        Column('id', Integer), 
        Column('classes', Integer),
    )

    conn = db.connect()
    
    for i in range(len(data)):
        insert_data = tb_target.insert().values(
            executed_at = data[i]['executed_at'], 
            id = data[i]['id'],
            classes = data[i]['classes']
        )

        conn.execute(insert_data)
    conn.close()
