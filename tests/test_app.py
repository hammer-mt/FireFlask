def test_visit_the_homepage(tester): 
    response = tester.get('/')
    assert response.status_code == 200
    assert b'FireFlask' in response.data