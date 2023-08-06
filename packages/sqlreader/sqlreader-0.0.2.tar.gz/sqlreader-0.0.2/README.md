import sqlreader as sql


sql.set_base_dir('sql_queries/')
q = sql.read('query_name')

OR 

q = sql.read('sql_queries/query_name')


TO CLEAR CACHE:
    sql.clear_cache()
    