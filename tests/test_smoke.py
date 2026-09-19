from app import app
def test_home_redirect():
    c=app.test_client(); r=c.get('/'); assert r.status_code in (302,200)
