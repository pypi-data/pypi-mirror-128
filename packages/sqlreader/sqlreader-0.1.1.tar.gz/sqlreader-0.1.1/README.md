# Simple sql reader

##  To read file
```python
import sqlreader as sql
sql.set_base_dir('sql_queries/') # default '/'
q = sql.read('query_name')
```

##### OR 
```python
q = sql.read('sql_queries/query_name')

```

------------

## Clear cache
```python
sql.clear_cache()
```

------------


## To creat class SQLReader

```python
import sqlreader
sql = sqlreader.SQLReader() # params 'directory_name' and 'auto_clear'
q = sql.read('query_name')
```
