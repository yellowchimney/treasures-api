'''This module contains the test suite for the
`Cat's Rare Treasures` FastAPI app.'''

from fastapi.testclient import TestClient
from main import app 
from db.seed import seed_db
import pytest

@pytest.fixture(autouse=True)
def reset_db():
    seed_db()

@pytest.fixture
def client():
    return TestClient(app)

class TestHealthcheck:
    def test_200_get_confirmation_of_health(self,client):
        response = client.get('/api/healthcheck')
        assert response.status_code == 200
        assert response.json() == {'message': 'everything ok!'}

class TestGetTreasures:
    def test_200_get_treasures_returns_all_treasures(self, client):
        response = client.get('/api/treasures')
        assert response.status_code == 200
        body = response.json()
        assert len(body['treasure']) > 0
        for treasure in body['treasure']:
            assert type(treasure['treasure_id']) == int
            assert type(treasure['treasure_name']) == str
            assert type(treasure['colour']) == str
            assert type(treasure['age']) == int
            assert type(treasure['cost_at_auction']) == float
            assert type(treasure['shop']) == str

    def test_200_get_returns_treasures_in_ascending_ord(self,client):
        response = client.get('/api/treasures')
        body = response.json()
        age_list = [treasure['age'] for treasure in body['treasure']]
        sorted_age_list = sorted(age_list)
        assert age_list == sorted_age_list

class TestSortedTreasure:
    def test_200_gets_sorted_by_age_returns_in_ascending_ord(self,client):
        response = client.get('/api/treasures?sort_by=age')
        body = response.json()
        age_list = [treasure['age'] for treasure in body['treasure']]
        sorted_age_list = sorted(age_list)
        assert age_list == sorted_age_list 
    def test_200_gets_sorted_by_cost_returns_in_ascending_ord(self,client):
        response = client.get('/api/treasures?sort_by=cost_at_auction')
        body = response.json()
        cost_list = [treasure['cost_at_auction'] for treasure in body['treasure']]
        sorted_cost_list = sorted(cost_list)
        assert cost_list == sorted_cost_list 
    def test_200_gets_sorted_by_name_returns_in_ascending_ord(self,client):
        response = client.get('/api/treasures?sort_by=treasure_name')
        body = response.json()
        name_list = [treasure['treasure_name'] for treasure in body['treasure']]
        sorted_name_list = sorted(name_list)
        assert name_list == sorted_name_list 

