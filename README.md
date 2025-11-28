# 🦊 Animal Web Generator

## 💡 Project Description

This project is a dynamic web generator that fetches real-time animal data from the **API Ninjas Animal API** based on user input and automatically creates an interactive HTML page displaying the results.

It demonstrates best practices in Python development, including:
* **Modular Architecture:** Separation of concerns between **Data Fetching** (`data_fetcher.py`) and **Website Generation** (`animals_web_generator.py`).
* **API Interaction:** Making authenticated HTTP GET requests using the `requests` library.
* **Configuration Management:** Securely loading API keys from a `.env` file using `python-dotenv`.
* **Graceful Error Handling:** Displaying a custom message on the generated website when a search yields no results.

## 🛠️ Installation & Setup

Before running the project, you need to set up your environment and provide an API key.

### 1. Dependencies

This project requires the following Python libraries:

```bash
pip install requests python-dotenv