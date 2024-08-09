import requests
from bs4 import BeautifulSoup

def csrf_test(url, action):
    session = requests.Session()
    try:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})

            if not csrf_token:
                print(f"Potential CSRF vulnerability detected in {action} at {url}")
            else:
                print(f"CSRF protection found for {action} at {url}")
        else:
            print(f"Failed to access {action} page: {url}. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Request failed for {action} at {url}: {e}")

if __name__ == "__main__":
    base_url = "http://10.211.55.7/bwapp-master/bWAPP"

    # List of URLs to test
    urls = [
        (f"{base_url}/csrf_1.php", "Change password"),
        (f"{base_url}/csrf_3.php", "Change secret"),
        (f"{base_url}/csrf_2.php", "Transfer amount")
    ]

    for url, action in urls:
        csrf_test(url, action)
