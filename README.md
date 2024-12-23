# Submarine Cable Scraper

This project is a web scraper for extracting information about submarine cables from the [Submarine Cable Map](https://www.submarinecablemap.com/). It uses Selenium to navigate the website and scrape data, and stores the results in a CSV file.

## Features
- Automatically navigates to the submarine cable map website.
- Extracts key details for each cable, including:
  - Cable name
  - Ready for Service (RFS) date
  - Cable length
  - Owners
  - Suppliers
  - Submarine Networks URL
- Saves the data to a CSV file for further analysis.
- Handles pages with varying numbers of details.
- Uses `colorama` for colorful and user-friendly console outputs.

## Requirements

### Python Version
- Python 3.8 or higher is recommended.

### Dependencies
- `pandas`
- `selenium`
- `webdriver-manager`
- `colorama`

### Additional Requirements
- **Google Chrome** must be installed on your system for the Chrome WebDriver to function correctly.

### Install Requirements
Run the following command to install the dependencies:
```bash
pip install -r requirements.txt
```

## Getting Started

Follow these steps to set up and run the project:

### Step 1: Install Python
Ensure you have Python 3.8 or higher installed on your system.
- **Windows**: Download Python from the [official Python website](https://www.python.org/downloads/). During installation, make sure to check the box that says "Add Python to PATH."
- **Mac**: Download Python from the [official Python website](https://www.python.org/downloads/) or use Homebrew:
  ```bash
  brew install python
  ```

### Step 2: Install Git
Ensure Git is installed on your system.
- **Windows**: Download Git from the [official Git website](https://git-scm.com/downloads/) and follow the installation instructions.
- **Mac**: Install Git using Homebrew:
  ```bash
  brew install git
  ```

### Step 3: Clone the Repository
Use Git to clone the project repository:
```bash
git clone https://github.com/your-repo/submarine-cable-scraper.git
```
Navigate to the project directory:
```bash
cd submarine-cable-scraper
```

### Step 4: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 5: Run the Script
Execute the main script:
```bash
python main.py
```

### Step 6: View the Results
The results will be saved in a file named `submarine_cables.csv` in the project directory.

## Usage

### Step 1: Run the Script
Execute the main script to start the scraping process:
```bash
python main.py
```

### Step 2: View the Results
Once the script completes, the results will be saved in a CSV file named `submarine_cables.csv` in the project directory.

### Customizing the Script
You can customize the following aspects of the script:
- **Number of links to scrape:** Adjust the limit in `extract_links` to control how many links are processed. By default, the script processes up to 645 links:
  ```python
  return links[:645]  # Limit to first 645 links for testing or demonstration
  ```
- **Output filename:** Change the filename in the `save_to_csv` function.

## Project Structure
```
.
├── main.py             # Main scraping script
├── requirements.txt     # List of dependencies
├── README.md            # Project documentation
└── submarine_cables.csv # Output file (generated after running the script)
```

## Error Handling
- If the scraper encounters a page with unexpected structure, it will log an error message and skip the link.
- Make sure the website structure matches the assumptions in the script, as web scraping relies on the HTML structure.

## Notes
- The scraper runs in headless mode by default. To see the browser in action, comment out the line:
  ```python
  options.add_argument("--headless")
  ```
- This script is for educational and non-commercial purposes only. Respect the website's terms of service.


