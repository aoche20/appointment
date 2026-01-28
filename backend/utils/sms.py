import requests

def send_sms(phone, message):
    url = "https://api.mtn.com/v1/momo/payment"  # Exemple, adapter selon opérateur
    data = {
        "to": phone,
        "message": message
    }
    # Ici, tu appelleras le vrai endpoint MoMo / Wave
    response = requests.post(url, json=data)
    return response.status_code, response.text
