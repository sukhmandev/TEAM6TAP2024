import requests

file_path = input("Enter the full path to the file you want to upload: ")

upload_url = "http://localhost/bWAPP/unrestricted_file_upload.php"

file_name = file_path.split('/')[-1]

uploaded_file_url = f"http://localhost/bWAPP/images/{file_name}"

try:
    with open(file_path, 'rb') as file_to_upload:
        files = {'uploaded_file': file_to_upload}
        data = {
            'form': 'submit', 
            'action': 'upload'
        }

        response = requests.post(upload_url, files=files, data=data, cookies={'security_level': '0'})

       
        if response.status_code == 200:
            print("File uploaded successfully!")

            uploaded_file_response = requests.get(uploaded_file_url)

            if uploaded_file_response.status_code == 200:
                print("File upload vulnerability detected!")
                print(f"Uploaded file is accessible at: {uploaded_file_url}")
            else:
                print("File upload was successful, but the file is not accessible.")
        else:
            print(f"Failed to upload the file. Status code: {response.status_code}")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
