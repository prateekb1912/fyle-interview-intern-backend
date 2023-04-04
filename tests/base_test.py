def test_api_running(client):
    response = client.get('/')

    assert response.status_code == 200
    
    response = response.json

    assert response['status'] == 'ready'

def test_api_endpoint_not_exists(client):
    response = client.get('/assignments/')

    assert response.status_code == 404
    
    error = response.json['error']

    assert error == 'NotFound'