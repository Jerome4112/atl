from fastapi.testclient import TestClient
from ATL.main import app

#Erstellung der Testdaten

client = TestClient(app)

def create_access_token_for_test():
    # Erstellen der Daten für den Testbenutzer
    test_user_data = {
        "name": "testuser",
        "hashed_password": "Test",
        "is_authorised": True  
    }
    # POST-Anfrage, um den Testbenutzer zu registrieren
    response = client.post("/user/register", json=test_user_data)
    # Das Zugriffstoken des Testbenutzers
    access_token = response.json()["access_token"]
    return access_token

#Erstellen eines Testkunden
def create_customer_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    customer_data = {
        "id": 1,
        "name": "Test Customer",
        "adress": "Test Adress",
        "adressNr": 1,
        "email": "test@test.ch",
        "tel": 123456789,
        "city": "Test City",
        "postalCode": 1234,
    }
    response = client.post("/customer/", headers=headers, json=customer_data)
    return response


#Erstellen eines Testmitarbeiters
def create_employee_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    employee_data = {
        "id": 1,
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@test.ch",
        "passwordEmail": "Test",
        "tel": 123456789,
    }
    response = client.post(f"/employee/{1}", headers=headers, json=employee_data)
    return response

#Erstellen eines Testauftrags
def create_order_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    order_data = {
        "id": 1,
        "title": "Test",
        "hardware": "Test",
        "details": "Test",
    }
    response = client.post(f"/order/{1},{1}", headers=headers, json=order_data)
    return response

#Erstellen eines Testprogramms
def create_program_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    program_data = {
        "id": 1,
        "title": "Test",
        "licenseKey": "ABCDEF-123456-ABCDEF-123456-ABCDEF",
        "version": "1.123",
        "installLink": "https://www.test.ch",
    }
    response = client.post(f"/program/", headers=headers, json=program_data)
    return response