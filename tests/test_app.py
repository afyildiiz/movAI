# Unit Testler
# Unit testler, bireysel işlevlerin veya endpoint'lerin düzgün çalışıp çalışmadığını kontrol eder.

import pytest
from app import app  # Flask uygulamanı import et
app.testing = True

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/about')  # Doğru endpoint
    assert response.status_code == 200
    assert b"WHILE DESIGNING THIS SITE" in response.data  # HTML'deki metni kontrol et

def test_invalid_method(client):
    response = client.post('/home')  # GET yerine POST gönder
    assert response.status_code == 405  # Method Not Allowed


# Integration Testler
# Integration testleri, farklı bileşenlerin bir arada çalışmasını test eder. Örneğin, bir form gönderimi ve veritabanı kaydı.
    """
    
def test_form_submission(client):
    response = client.post('/about', data={'name': 'Test User', 'email': 'test@example.com', 'message':'helloWorld!'})
    assert response.status_code == 200
    assert b"Form submitted successfully" in response.data

    """