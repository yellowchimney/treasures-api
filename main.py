'''This module is the entrypoint for the `Cat's Rare Treasures` FastAPI app.'''
from fastapi import FastAPI, HTTPException, Query
from db.connection import connect_to_db
from pydantic import BaseModel 
from pg8000.exceptions import DatabaseError, InterfaceError
from pprint import pprint
app = FastAPI()
@app.get('/api/healthcheck')
def get_healthcheck():
    return {'message' : 'everything ok!'} 

@app.get('/api/treasures')
def get_treasures(sort_by = 'age'):
    conn = connect_to_db()
    allowed_columns = {'age', 'cost_at_auction', 'treasure_name'}
    if sort_by not in allowed_columns:
        raise HTTPException (status_code = 400, detail = 'invalid column request')
    
    query = f'''
        SELECT * FROM treasures 
        JOIN shops 
        USING(shop_id) 
        ORDER BY {sort_by};'''
    
    treasures_list = conn.run(query)
    treasure = [{'treasure_id' : row[1], 
                 'treasure_name': row[2], 
                 'colour': row[3], 
                 'age': row[4], 
                 'cost_at_auction': row[5], 
                 'shop': row[6]} 
                 for row in treasures_list]
    conn.close()
    return {"treasure": treasure}

