'''This module is the entrypoint for the `Cat's Rare Treasures` FastAPI app.'''
from fastapi import FastAPI, HTTPException
from db.connection import connect_to_db
from pydantic import BaseModel 
from pg8000.exceptions import DatabaseError, InterfaceError

app = FastAPI()
@app.get('/api/healthcheck')
def get_healthcheck():
    return {'message' : 'everything ok!'} 

@app.get('/api/treasures')
def get_treasures():
    conn = connect_to_db()
    treasures_list = conn.run("""SELECT * FROM treasures ORDER BY age;""")
    treasure = [{'treasure_id' : row[0], 
                 'treasure_name': row[1], 
                 'colour': row[2], 
                 'age': row[3], 
                 'cost_at_auction': row[4], 
                 'shop': row[5]} 
                 for row in treasures_list]
    conn.close()
    return {"treasure": treasure}

@app.get('/api/treasures?sort_by={parameter}')
def get_sorted_treasures():
    conn = connect_to_db()