import requests
from bs4 import BeautifulSoup

def csrf_test(url, action):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    csrf_token = soup.find('input', {'name': 'csrf_token'})

    if not csrf_token:
        print(f"Potential CSRF vulnerability detected in {action}")
    else:
        print(f"CSRF protection found for {action}")

if __name__ == "__main__":
    base_url = "http://localhost/bwapp-master/bWAPP"

    csrf_test(f"{base_url}/change_password.php", "Change password")
    csrf_test(f"{base_url}/change_secret.php", "Change secret")
    csrf_test(f"{base_url}/transfer_amount.php", "Transfer amount")
