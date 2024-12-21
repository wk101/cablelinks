import sys
from dbm import error

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Back, Style, init
import re
from typing import List

# Initialize colorama for colored output
init(autoreset=True)

def setup_driver() -> webdriver.Chrome:
    """
    Set up the Chrome WebDriver.

    Returns:
        webdriver.Chrome: The configured WebDriver instance.
    """
    print(Fore.BLUE + "Setting up the driver...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional: run headless Chrome
    driver = webdriver.Chrome(service=service, options=options)
    print(Fore.GREEN + "Driver setup complete.")
    return driver

def navigate_to_page(driver: webdriver.Chrome, url: str) -> None:
    """
    Navigate to a specified URL and wait for the page to load.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        url (str): The URL to navigate to.
    """
    print(Fore.YELLOW + f"Navigating to {url}")
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print(Fore.CYAN + "Page loaded.")

def extract_links(driver: webdriver.Chrome) -> List[str]:
    """
    Extract links from the main page.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.

    Returns:
        List[str]: A list of links to submarine cable pages.
    """
    print(Fore.MAGENTA + "Extracting links...")
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/submarine-cable/']"))
    )
    links = [element.get_attribute('href') for element in elements if 'trivia' not in element.get_attribute('href')]
    print(Fore.GREEN + f"Found {len(links)} links.")
    return links[:645]  # Limit to first 645 links for testing or demonstration

def scrape_data(driver: webdriver.Chrome, links: List[str]) -> pd.DataFrame:
    """
    Scrape data from the provided list of links.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        links (List[str]): A list of links to submarine cable pages.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped data.
    """
    columns = ['cable_name', 'rfs', 'cable_length', 'owners', 'suppliers', 'submarine_networks_url', 'submarine_cable_map_url']
    df = pd.DataFrame(columns=columns)
    print(Fore.YELLOW + "Scraping data from links...")

    for link in links:
        print(Fore.CYAN + f"Visiting link: {link}")
        driver.get(link)
        cable_info = {column: '' for column in columns}  # Initialize dictionary with empty values for each column
        cable_info['submarine_cable_map_url'] = link
        cable_info['cable_name'] = re.search(r'/([^/]+)$', link).group(1)  # Extract cable name from URL

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div ul')))
            list_items = driver.find_elements(By.CSS_SELECTOR, 'li.mb-2')  # Target li with class mb-2

            if len(list_items) == 5:
                rfs = list_items[0].text.split('\n')[-1].strip()
                cable_length = list_items[1].text.split('\n')[-1].strip()
                cable_length = cable_length.strip('"')
                owners = list_items[2].text.split('\n', 1)[-1].strip().replace(',', ' - ')
                suppliers = list_items[3].text.split('\n', 1)[-1].strip().replace(',', ' - ')
                submarine_networks_url = list_items[4].find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            elif len(list_items) == 4:
                 rfs = list_items[0].text.split('\n')[-1].strip()
                 cable_length = list_items[1].text.split('\n')[-1].strip()
                 cable_length = cable_length.strip('"')
                 owners = list_items[2].text.split('\n', 1)[-1].strip().replace(',', ' - ')
                 suppliers = list_items[3].text.split('\n', 1)[-1].strip().replace(',', ' - ')
                 submarine_networks_url = "Not Given"
            elif len(list_items) == 3:
                rfs = list_items[0].text.split('\n')[-1].strip()
                cable_length = list_items[1].text.split('\n')[-1].strip()
                cable_length = cable_length.strip('"')
                owners = list_items[2].text.split('\n', 1)[-1].strip().replace(',', ' - ')
                suppliers = "Not Given"
                submarine_networks_url = "Not Given"
            else:
                print(Fore.RED + f"Wrong no col, link: {link} len: {len(list_items)}")
                sys.exit(1)

            print(Fore.GREEN + f"RFS: {rfs}")
            print(Fore.CYAN + f"Cable Length: {cable_length}")
            print(Fore.YELLOW + f"Owners: {owners}")
            print(Fore.MAGENTA + f"Suppliers: {suppliers}")
            print(Fore.BLUE + f"Submarine Networks URL: {submarine_networks_url}")

            cable_info.update({
                    'rfs': rfs,
                    'cable_length': cable_length,
                    'owners': owners,
                    'suppliers': suppliers,
                    'submarine_networks_url': submarine_networks_url
            })
            df = pd.concat([df, pd.DataFrame([cable_info])], ignore_index=True)

        except Exception as e:
            print(Fore.RED + f"Failed to scrape data from {link}: {e}")

    return df

def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        filename (str): The filename for the CSV.
    """
    print(Fore.MAGENTA + f"Saving data to {filename}...")
    df.to_csv(filename, index=False)
    print(Fore.GREEN + "Data saved successfully!")

def main() -> None:
    """
    Main function to orchestrate the web scraping process.
    """
    driver = setup_driver()
    main_url = 'https://www.submarinecablemap.com/'
    navigate_to_page(driver, main_url)
    links = extract_links(driver)
    scraped_data = scrape_data(driver, links)
    save_to_csv(scraped_data, 'submarine_cables.csv')
    driver.quit()
    print(Fore.GREEN + Back.BLACK + "Scraping process completed!")

if __name__ == "__main__":
    main()
