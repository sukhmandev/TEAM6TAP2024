import requests
from bs4 import BeautifulSoup

def set_security_level(session, base_url, level):
    security_levels = {"low": "0", "medium": "1", "high": "2"}
    if level not in security_levels:
        print(f"Unknown security level: {level}")
        return False
    
    security_level_url = f"{base_url}/security.php"
    payload = {
        'security_level': security_levels[level],
        'form': 'submit'
    }
    
    try:
        response = session.post(security_level_url, data=payload)
        if response.status_code == 200:
            print(f"Security level set to {level.capitalize()}")
            return True
        else:
            print(f"Failed to set security level to {level}. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error setting security level: {e}")
        return False

def csrf_test(session, url, action):
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

    security_levels = ['low', 'medium', 'high']

    with requests.Session() as session:
        # Set session cookies by logging in if needed
        # Assuming you have a login mechanism
        # login(session, base_url)  # Implement this if your application requires login

        for level in security_levels:
            if set_security_level(session, base_url, level):
                print(f"\nTesting CSRF for security level: {level.capitalize()}")
                for url, action in urls:
                    csrf_test(session, url, action)
