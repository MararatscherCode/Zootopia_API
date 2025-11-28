import json


def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


def safe_summary(animals):
  output = ''
  for animal in animals:
    name = animal.get("name")
    
    # Start of the list item
    output += '<li class="cards__item">\n'
    
    # Card title (animal name)
    if name:
      output += f'<div class="card__title">{name}</div>\n'

    # Card text (characteristics)
    output += '<p class="card__text">'
    
    characteristics = animal.get("characteristics") or {}
    diet = characteristics.get("diet")
    if diet:
      output += f"<strong>Diet:</strong> {diet}<br/>\n"

    locations = animal.get("locations") or []
    if isinstance(locations, list) and len(locations) > 0:
      first_location = locations[0]
      if first_location:
        output += f"<strong>Location:</strong> {first_location}<br/>\n"
        

    type_value = characteristics.get("type")
    if type_value:
      output += f"<strong>Type:</strong> {type_value}<br/>\n"
      
    # End of card text and list item
    output += '</p></li>\n'
    
  return output


def main():
  try:
    animals_data = load_data('animals_data.json')
  except Exception as e:
    print(f"Error loading data: {e}")
    return

  summary = safe_summary(animals_data)
  tpl_path = 'animals_template.html'
  try:
    with open(tpl_path, 'r', encoding='utf-8') as f:
      tpl = f.read()
  except Exception as e:
    print(f"Error reading template {tpl_path}: {e}")
    return

  start_tag = '<ul class="cards">'
  end_tag = '</ul>'
  
  start_index = tpl.find(start_tag) + len(start_tag)
  end_index = tpl.find(end_tag)

  if start_index != -1 and end_index != -1:
    before_list = tpl[:start_index]
    after_list = tpl[end_index:]
    
    filled = f"{before_list}\n{summary}\n{after_list}"
  else:
    print("Error: Could not find <ul> tags in the template.")
    return

  output_path = 'animals_template.html'
  try:
    with open(output_path, 'w', encoding='utf-8') as f:
      f.write(filled)
    print(f"Generated {output_path} (template preserved as {tpl_path})")
  except Exception as e:
    print(f"Error writing output {output_path}: {e}")

if __name__ == "__main__":
  main()