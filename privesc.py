import requests

def privilege_escalation_test(url, method="get", data=None):
    session = requests.Session()

    try:
        if method.lower() == "get":
            response = session.get(url)
        elif method.lower() == "post":
            response = session.post(url, data=data)

        if response.status_code == 200:
            print(f"Potential privilege escalation vulnerability detected: {url}")
            print(f"Response content: {response.text[:100]}...")  # Print first 100 characters
        else:
            print(f"Access denied as expected: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while testing {url}: {e}")

if __name__ == "__main__":
    dvwa_url = "http://localhost/DVWA"  # Replace with your DVWA URL

    # Test direct URL access
    privilege_escalation_test(f"{dvwa_url}/vulnerabilities/csrf/")

    # Test form data manipulation
    privilege_escalation_test(f"{dvwa_url}/vulnerabilities/exec/", "post",
                              {"username": "admin", "password": "password"})
