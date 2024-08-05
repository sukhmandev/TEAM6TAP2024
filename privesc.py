from zapv2 import ZAPv2
import time

def setup_zap():
    zap = ZAPv2(apikey='your_api_key_here', proxies={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})
    return zap

def test_direct_url_access(zap, base_url):
    print("Testing Direct URL Access...")
    restricted_urls = [
        "/vulnerabilities/csrf/",
        "/vulnerabilities/exec/",
        "/vulnerabilities/upload/",
        "/vulnerabilities/captcha/"
    ]
    
    for url in restricted_urls:
        full_url = f"{base_url}{url}"
        response = zap.core.send_request(f"GET {full_url} HTTP/1.1\r\nHost: localhost\r\n\r\n")
        if "200 OK" in response:
            print(f"Potential privilege escalation via direct access: {full_url}")
        else:
            print(f"Access denied as expected: {full_url}")

def test_form_manipulation(zap, base_url):
    print("\nTesting Form Data Manipulation...")
    login_url = f"{base_url}/login.php"
    
    # Attempt login with default low privilege credentials
    response = zap.core.send_request(
        f"POST {login_url} HTTP/1.1\r\nHost: localhost\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
        f"username=user&password=password&Login=Login"
    )
    
    if "Login failed" not in response:
        print("Logged in with low privilege user")
        
        # Try to access admin page
        admin_url = f"{base_url}/vulnerabilities/admin/"
        response = zap.core.send_request(f"GET {admin_url} HTTP/1.1\r\nHost: localhost\r\n\r\n")
        
        if "Admin Panel" in response:
            print("Potential privilege escalation: Low privilege user accessed admin panel")
        else:
            print("Access to admin panel denied as expected")
    else:
        print("Failed to log in with low privilege user")

def main():
    zap = setup_zap()
    base_url = "http://localhost/DVWA"
    
    # Ensure ZAP is ready
    while not zap.core.is_in_scope(base_url):
        zap.core.include_in_scope(base_url)
        time.sleep(2)
    
    test_direct_url_access(zap, base_url)
    test_form_manipulation(zap, base_url)

if __name__ == "__main__":
    main()
