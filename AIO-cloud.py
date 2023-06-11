import subprocess
from time import sleep
from tqdm import tqdm 
import concurrent.futures
from google.auth.exceptions import DefaultCredentialsError, RefreshError
from oauth2client.client import HttpAccessTokenRefreshError
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import CredentialUnavailableError
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, SSLError


aioFactory = ['AIO-aws.py', 'AIO-az.py', 'AIO-gcp.py']

# Define a runing the IAC stack at once omitting authenication errors for demo
def run_aioFactory(aioFactory):
    try:
        subprocess.run(['python', run_aioFactory], check=True)
    except (DefaultCredentialsError, RefreshError, HttpAccessTokenRefreshError,
            ClientAuthenticationError, CredentialUnavailableError,
            NoCredentialsError, PartialCredentialsError, SSLError) as e:
        print(f'Authentication or authorization error occurred while running {run_aioFactory}: {str(e)}')
    except subprocess.CalledProcessError as e:
        raise

# Use a ThreadPoolExecutor to run the aioFactory in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(run_aioFactory, aioFactory)
print("time elasped executing between clsoud actions")


for cloud_factory in tqdm(aioFactory): 
        sleep(30)


