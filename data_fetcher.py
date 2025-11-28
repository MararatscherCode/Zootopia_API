import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
# This must be done here so the API_KEY is available when the function is called
load_dotenv() 
API_KEY = os.getenv("API_NINJAS_KEY")
API_URL = "https://api.api-ninjas.com/v1/animals"


def fetch_data(animal_name):
  """
  Fetches the animals data for the animal 'animal_name' from the API Ninjas.

  Returns: a list of animals (list of dictionaries) or None if an error occurs.
  The structure of each animal dictionary generally matches the original requirements.
  """
  if not API_KEY:
    print("Error: API_NINJAS_KEY not found in .env file.")
    return None

  # Headers must include the API key for authentication
  headers = {'X-Api-Key': API_KEY}
  
  # Parameters include the 'name' of the animal to search for
  params = {'name': animal_name}
  
  print(f"Fetching data for '{animal_name}' from API...")
  
  try:
    response = requests.get(API_URL, headers=headers, params=params)
    
    # Raises an HTTPError for bad responses (4xx or 5xx)
    response.raise_for_status() 
    
    # API Ninjas returns a JSON list of animals (or an empty list [])
    return response.json()
    
  except requests.exceptions.RequestException as e:
    # Handle API/Network errors
    print(f"An API request error occurred: {e}")
    if response is not None and response.status_code == 401:
        print("Authentication Error: Check your API_NINJAS_KEY.")
    return None