import pytest
from django.urls import reverse

dates = ['2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09']


@pytest.fixture()
def test_page_exist(client):
    url = reverse('')
    response = client.get(url)
    assert response.status_code == 200
