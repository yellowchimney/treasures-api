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
def get_treasures(colour: str = None, sort_by: str = 'age', order: str = 'asc'):
    conn = connect_to_db()
    allowed_columns = {'age', 'cost_at_auction', 'treasure_name'}
    allowed_order = {'asc', 'desc'}

    if sort_by not in allowed_columns:
        raise HTTPException (status_code = 400, detail = 'invalid column request')

    if order not in allowed_order:
        raise HTTPException (status_code = 400, detail = 'invalid order direction')
    
    query = query = '''SELECT * FROM treasures JOIN shops USING(shop_id)'''
    if colour: 
        query += f'''WHERE colour = :colour'''
    query += f''' ORDER BY {sort_by} {order};'''
    
    treasures_list = conn.run(query, colour = colour)
    treasure = [{'treasure_id' : row[1], 
                 'treasure_name': row[2], 
                 'colour': row[3], 
                 'age': row[4], 
                 'cost_at_auction': row[5], 
                 'shop': row[6]} 
                 for row in treasures_list]
    conn.close()
    return {"treasure": treasure}

class NewTreasure(BaseModel):
    treasure_name: str
    colour: str
    age: int
    cost_at_auction: float
    shop_id: int


@app.post('/api/treasures',status_code=201)
def post_treasures(new_treasure: NewTreasure):
    conn = connect_to_db()
    query = ('''INSERT INTO treasures (treasure_name, colour, age, cost_at_auction, shop_id)
    VALUES
    (:treasure_name, :colour, :age, :cost_at_auction, :shop_id) RETURNING *;''')
    inserted_treasure = conn.run(query,**dict(new_treasure))[0]
    columns = [col['name']for col in conn.columns]
    treasure_for_cat = zip(columns,inserted_treasure)
    return {'treasure': treasure_for_cat}

