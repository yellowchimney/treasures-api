"""This module contains the test suite for the
`Cat's Rare Treasures` FastAPI app."""

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
    def test_200_get_confirmation_of_health(self, client):
        response = client.get("/api/healthcheck")
        assert response.status_code == 200
        assert response.json() == {"message": "everything ok!"}


class TestGetTreasures:
    def test_200_get_treasures_returns_all_treasures(self, client):
        response = client.get("/api/treasures")
        assert response.status_code == 200
        body = response.json()
        assert len(body["treasure"]) > 0
        for treasure in body["treasure"]:
            assert type(treasure["treasure_id"]) == int
            assert type(treasure["treasure_name"]) == str
            assert type(treasure["colour"]) == str
            assert type(treasure["age"]) == int
            assert type(treasure["cost_at_auction"]) == float
            assert type(treasure["shop"]) == str

    def test_200_get_returns_treasures_in_ascending_ord(self, client):
        response = client.get("/api/treasures")
        body = response.json()
        age_list = [treasure["age"] for treasure in body["treasure"]]
        sorted_age_list = sorted(age_list)
        assert age_list == sorted_age_list


class TestSortedTreasure:
    def test_200_gets_sorted_by_age_returns_in_ascending_ord(self, client):
        response = client.get("/api/treasures?sort_by=age")
        body = response.json()
        age_list = [treasure["age"] for treasure in body["treasure"]]
        sorted_age_list = sorted(age_list)
        assert age_list == sorted_age_list

    def test_200_gets_sorted_by_cost_returns_in_ascending_ord(self, client):
        response = client.get("/api/treasures?sort_by=cost_at_auction")
        body = response.json()
        cost_list = [treasure["cost_at_auction"] for treasure in body["treasure"]]
        sorted_cost_list = sorted(cost_list)
        assert cost_list == sorted_cost_list

    def test_200_gets_sorted_by_name_returns_in_ascending_ord(self, client):
        response = client.get("/api/treasures?sort_by=treasure_name")
        body = response.json()
        name_list = [treasure["treasure_name"] for treasure in body["treasure"]]
        sorted_name_list = sorted(name_list)
        assert name_list == sorted_name_list

    def test_200_gets_sorted_by_age_returns_in_descending_ord(self, client):
        response = client.get("/api/treasures?sort_by=age&order=desc")
        body = response.json()
        age_list = [treasure["age"] for treasure in body["treasure"]]
        sorted_age_list = sorted(age_list, reverse=True)
        assert age_list == sorted_age_list

    def test_200_gets_sorted_by_cost_returns_in_descending_ord(self, client):
        response = client.get("/api/treasures?sort_by=cost_at_auction&order=desc")
        body = response.json()
        cost_list = [treasure["cost_at_auction"] for treasure in body["treasure"]]
        sorted_cost_list = sorted(cost_list, reverse=True)
        assert cost_list == sorted_cost_list

    def test_200_gets_sorted_by_name_returns_in_descending_ord(self, client):
        response = client.get("/api/treasures?sort_by=treasure_name&order=desc")
        body = response.json()
        name_list = [treasure["treasure_name"] for treasure in body["treasure"]]
        sorted_name_list = sorted(name_list, reverse=True)
        assert name_list == sorted_name_list

    def test_gets_colour_only_requests(self, client):
        response = client.get("/api/treasures?colour=gold")
        body = response.json()
        expected = {
            "treasure": [
                {
                    "treasure_id": 3,
                    "treasure_name": "treasure-b",
                    "colour": "gold",
                    "age": 13,
                    "cost_at_auction": 500.0,
                    "shop": "shop-f",
                },
                {
                    "treasure_id": 10,
                    "treasure_name": "treasure-c",
                    "colour": "gold",
                    "age": 13,
                    "cost_at_auction": 15.99,
                    "shop": "shop-c",
                },
            ]
        }
        assert body == expected

    def test_returns_sort_by_and_colour_requests(self, client):
        response = client.get("/api/treasures?sort_by=age&colour=gold")
        body = response.json()
        age_list = [treasure["age"] for treasure in body["treasure"]]
        sorted_age_list = sorted(age_list)
        print(sorted_age_list)
        for treasure in body["treasure"]:
            print(treasure)
            assert treasure["colour"] == "gold"
        assert age_list == sorted_age_list

    def test_returns_sort_by_and_order_requests_with_colour(self, client):
        response = client.get(
            "/api/treasures?sort_by=treasure_name&order=desc&colour=gold"
        )
        body = response.json()
        name_list = [treasure["treasure_name"] for treasure in body["treasure"]]
        sorted_name_list = sorted(name_list, reverse=True)
        for treasure in body["treasure"]:
            assert treasure["colour"] == "gold"
        assert name_list == sorted_name_list


class TestPostTreasure:
    def test_returns_201(self, client):
        response = client.post(
            "/api/treasures",
            json={
                "treasure_name": "treasure-g",
                "colour": "gold",
                "age": 15,
                "cost_at_auction": "56.00",
                "shop_id": 3,
            },
        )
        body = response.json()
        expected_body = {
            "treasure": {
                "treasure_id": 27,
                "treasure_name": "treasure-g",
                "colour": "gold",
                "age": 15,
                "cost_at_auction": 56.00,
                "shop_id": 3,
            }
        }
        assert response.status_code == 201
        assert body["treasure"]["treasure_name"] == "treasure-g"
        assert type(body["treasure"]["treasure_name"]) == str
        assert body == expected_body


class TestPatchTreasure:
    def test_returns_updated_value(self, client):
        response = client.patch("/api/treasures/3", json={"cost_at_auction": 200})
        body = response.json()
        assert response.status_code == 200
        new_price = 200
        assert body["treasure"][0][4] == new_price

    def test_returns_422_for_invalid_input(self, client):
        response = client.patch("/api/treasures/3", json={"cost_at_auction": "a"})
        assert response.status_code == 422


class TestDeleteTreasure:
    def test_status_code(self, client):
        response = client.delete("/api/treasures/26")
        assert response.status_code == 204

    def test_treasure_table_updated(self, client):
        client.delete("/api/treasures/5")
        response = client.get("/api/treasures")
        body = response.json()
        id_list = [dict["treasure_id"] for dict in body["treasure"]]
        assert 5 not in id_list
