def test_login_page(client):
    response = client.get("/iam/login")
    assert b"<title>Login</title>" in response.data
