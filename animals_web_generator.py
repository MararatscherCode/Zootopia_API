import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_NINJAS_KEY")
API_URL = "https://api.api-ninjas.com/v1/animals"


def fetch_animal_data(animal_name):
  """
  Fetches animal data from the API Ninjas Animal API.
  Returns a list of animals (which can be empty).
  """
  if not API_KEY:
    raise ValueError("API_NINJAS_KEY not found. Please create a .env file.")

  # Headers must include the API key for authentication
  headers = {'X-Api-Key': API_KEY}

  # Parameters include the 'name' of the animal to search for
  params = {'name': animal_name}

  print(f"Fetching data for '{animal_name}' from API...")

  try:
    response = requests.get(API_URL, headers=headers, params=params)

    # Raises an HTTPError for bad responses (4xx or 5xx)
    response.raise_for_status() 

    # API Ninjas returns a JSON list of animals (or an empty list)
    return response.json()

  except requests.exceptions.RequestException as e:
    # Print the error for debugging
    print(f"An API request error occurred: {e}")
    if response is not None and response.status_code == 401:
        print("Authentication Error: Check your API_NINJAS_KEY.")
    return None # Return None to stop processing


# The function now accepts the animal_name to use in the error message
def safe_summary(animals, animal_name):
  output = ''

  # --- MODIFIED LOGIC FOR HANDLING EMPTY RESULTS ---
  # If the API returns an empty list, generate the custom HTML message.
  if not animals or not isinstance(animals, list):
      # Create a custom, formatted error message inside a list item
      # Use an <h3> tag for a slightly smaller heading than the example <h2>
      error_message = f"""
<li class="cards__item">
    <div class="card__title">Search Failed 😥</div>
    <p class="card__text">
        <h3>The animal "<strong>{animal_name}</strong>" doesn't exist in our database.</h3>
        <p>Please check your spelling and try another animal name.</p>
    </p>
</li>
"""
      return error_message
  # --------------------------------------------------

  # If animals were found, proceed with generating the cards
  for animal in animals:
    name = animal.get("name")

    # Start of the list item
    output += '<li class="cards__item">\n'

    # Card title (animal name)
    if name:
      output += f'<div class="card__title">{name}</div>\n'

    # Card text (characteristics)
    output += '<p class="card__text">'

    # The API Ninjas structure: characteristics are nested.
    characteristics = animal.get("characteristics") or {}

    # Mapping the required fields to the API Ninjas response structure
    diet = characteristics.get("diet")
    if diet:
      output += f"<strong>Diet:</strong> {diet}<br/>\n"

    # API Ninjas uses 'location' (singular string) under characteristics.
    locations = characteristics.get("location")
    if locations:
      output += f"<strong>Location:</strong> {locations}<br/>\n"

    type_value = characteristics.get("class") # 'class' in API Ninjas is often the taxonomic type
    if type_value:
      output += f"<strong>Type:</strong> {type_value}<br/>\n"

    # End of card text and list item
    output += '</p></li>\n'

  return output


def main():
  # Get the animal name from the user
  print("Enter a name of an animal: ", end="")
  user_animal_name = input()
  
  # STEP 1: Fetch data for the user-entered animal name from the API
  animals_data = fetch_animal_data(user_animal_name)

  if animals_data is None:
    print("Could not retrieve animal data. Exiting.")
    return

  # STEP 2: Generate HTML summary (pass the user's input name)
  summary = safe_summary(animals_data, user_animal_name)
  tpl_path = 'animals_template.html'

  try:
    with open(tpl_path, 'r', encoding='utf-8') as f:
      tpl = f.read()
  except Exception as e:
    print(f"Error reading template {tpl_path}: {e}")
    return

  # STEP 3: Insert generated summary into the template
  start_tag = '<ul class="cards">'
  end_tag = '</ul>'

  # Find the position to insert the new list items
  start_index = tpl.find(start_tag) + len(start_tag)
  end_index = tpl.find(end_tag)

  if start_index != -1 and end_index != -1:
    before_list = tpl[:start_index]
    after_list = tpl[end_index:]

    # Insert the new summary
    filled = f"{before_list}\n{summary}\n{after_list}"
  else:
    print("Error: Could not find <ul> tags in the template.")
    return

  # STEP 4: Write the final HTML output
  output_path = 'animals.html' 
  try:
    with open(output_path, 'w', encoding='utf-8') as f:
      f.write(filled)
    print(f"Website was successfully generated to the file {output_path}.")
  except Exception as e:
    print(f"Error writing output {output_path}: {e}")

if __name__ == "__main__":
  main()