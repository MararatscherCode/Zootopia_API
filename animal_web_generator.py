import os
# --- NEW: Import the data_fetcher module ---
import data_fetcher 


def safe_summary(animals, animal_name):
  """
  Generates the HTML list items (<li>) for the animals data.
  Handles the 'not found' case gracefully.
  """
  output = ''

  # If the API returned an empty list, generate the custom HTML message.
  if not animals or not isinstance(animals, list):
      # Custom HTML message for "not found"
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

  # If animals were found, generate the list items
  for animal in animals:
    name = animal.get("name")

    output += '<li class="cards__item">\n'
    
    if name:
      output += f'<div class="card__title">{name}</div>\n'

    output += '<p class="card__text">'

    # API Ninjas structure: characteristics are nested.
    characteristics = animal.get("characteristics") or {}

    # Diet
    diet = characteristics.get("diet")
    if diet:
      output += f"<strong>Diet:</strong> {diet}<br/>\n"

    # Location (using 'location' from API Ninjas)
    locations = characteristics.get("location")
    if locations:
      output += f"<strong>Location:</strong> {locations}<br/>\n"

    # Type (using 'class' from API Ninjas)
    type_value = characteristics.get("class") 
    if type_value:
      output += f"<strong>Type:</strong> {type_value}<br/>\n"

    output += '</p></li>\n'

  return output


def main():
  # Get the animal name from the user
  print("Enter a name of an animal: ", end="")
  user_animal_name = input()
  
  # --- NEW: Call the function from the imported module ---
  animals_data = data_fetcher.fetch_data(user_animal_name)

  if animals_data is None:
    print("Generation halted due to data fetching error.")
    return

  # STEP 2: Generate HTML summary (pass the user's input name for the error message)
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