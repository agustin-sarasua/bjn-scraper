import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium_db_loader.utils import (
    get_start_end_days,
    create_date_directory,
    generate_unique_filename,
)

DRIVER_PATH = "./chrome_driver/chromedriver"
MAIN_PAGE_URL = "http://bjn.poderjudicial.gub.uy/BJNPUBLICA/busquedaSelectiva.seam"
RESULTS_PAGE_TO = 30
ITEM_PAGE_TO = 30


def load_results_page(
    driver: webdriver.Chrome, start_day: str, end_day: str, limit: str
):
    # Find the date input fields and fill them
    date_from = driver.find_element(
        By.XPATH, '//*[@id="formBusqueda:j_id20:j_id23:fechaDesdeCalInputDate"]'
    )
    date_from.clear()  # Clear any existing value
    date_from.send_keys(start_day)  # Replace with the desired date

    date_to = driver.find_element(
        By.XPATH, '//*[@id="formBusqueda:j_id20:j_id147:fechaHastaCalInputDate"]'
    )
    date_to.clear()
    date_to.send_keys(end_day)

    # num_results = driver.find_element(By.XPATH, '//*[@id="formBusqueda:j_id20:j_id223:cantPagcomboboxField"]')
    # num_results.clear()
    # num_results.send_keys(limit)

    search_button = driver.find_element(
        By.XPATH, '//*[@id="formBusqueda:j_id20:Search"]'
    )
    search_button.click()

    # wait_time_in_seconds = 3  # Replace with your desired wait time
    time.sleep(5)

    # wait = WebDriverWait(driver, RESULTS_PAGE_TO)
    # results_loaded = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formResultados:dataTable"]')))


def is_next_page(driver: webdriver.Chrome):
    try:
        next_page_label = driver.find_element(
            By.XPATH, '//*[@id="formResultados:zonaPaginador"]/div/span[2]'
        )
        match = re.match(r"Página (\d+) de (\d+)", next_page_label.text)

        if match:
            current_page = int(match.group(1))
            total_pages = int(match.group(2))

            if current_page < total_pages:
                return True

        return False
    except Exception as e:
        print(e)
        return False


def process_results_page(driver: webdriver.Chrome, dir: str):
    print("Processing results page")
    # Find the table element
    table = driver.find_element(By.ID, "formResultados:dataTable:tb")

    # Find all table rows within the table
    table_rows = table.find_elements(By.TAG_NAME, "tr")

    wait = WebDriverWait(driver, ITEM_PAGE_TO)

    # Iterate over table rows
    for idx, row in enumerate(table_rows):
        print(f"Processing row {idx}")
        # Find the desired table cell in each row (e.g., the first cell)
        # table_cell = row.find_element(By.TAG_NAME, 'td')

        table_cell_1 = driver.find_element(
            By.XPATH, f'//*[@id="formResultados:dataTable:{idx}:colFec"]'
        )
        table_cell_2 = driver.find_element(
            By.XPATH, f'//*[@id="formResultados:dataTable:{idx}:j_id262"]'
        )
        table_cell_3 = driver.find_element(
            By.XPATH, f'//*[@id="formResultados:dataTable:{idx}:j_id264"]'
        )
        table_cell_4 = driver.find_element(
            By.XPATH, f'//*[@id="formResultados:dataTable:{idx}:j_id266"]'
        )

        filename = generate_unique_filename(
            table_cell_1.text, table_cell_2.text, table_cell_3.text, table_cell_4.text
        )
        file_path = f"{dir}/{filename}"

        print(f"Checking if exists {dir}/{filename}")
        if os.path.exists(f"{dir}/{filename}"):
            print(f"File {filename} already exists")
            continue

        # Click on the table cell to trigger the onclick event
        table_cell_3.click()

        # Wait for the new window to open
        wait.until(EC.number_of_windows_to_be(2))

        # Switch to the new window
        windows = driver.window_handles
        new_window = windows[1]
        driver.switch_to.window(new_window)

        new_window_html = driver.page_source

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_window_html)

        driver.close()

        # Switch back to the main window
        driver.switch_to.window(windows[0])

    if is_next_page(driver):
        print("Next page")
        next_button = driver.find_element(By.XPATH, '//*[@id="formResultados:sigLink"]')
        next_button.click()
        # Wait for a fixed amount of time
        time.sleep(5)

        # wait = WebDriverWait(driver, RESULTS_PAGE_TO)
        # results_loaded = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formResultados:dataTable"]')))
        print("Processing Next page")
        process_results_page(driver, dir)


def build_filters(year_from, year_to, limit, months_to_skip):
    filters = []
    for year in range(year_from, year_to + 1):
        for month in range(1, 13):
            if month in months_to_skip:
                continue  # Skip the specified months
            start_day, end_day = get_start_end_days(year, month)
            filters.append((start_day, end_day, limit))
    return filters


def main():
    # # Wait for the input field's value to change to the target value
    # timeout = 10  # seconds
    # wait = WebDriverWait(driver, timeout)
    # # Wait until the value changes to the target value
    # wait.until(EC.text_to_be_present_in_element_value((By.XPATH, '//*[@id="formBusqueda:j_id20:j_id223:cantPagcomboboxField"]'), "10"))

    # Load Filters
    months_to_skip = []
    # months_to_skip = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    filters = build_filters(
        year_from=2005, year_to=2007, limit=10, months_to_skip=months_to_skip
    )

    # Process Filters
    for filter in filters:
        service = Service(executable_path=DRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
        driver = webdriver.Chrome(service=service, options=options)
        # Load main page
        driver.get(MAIN_PAGE_URL)
        print(f"Processing filter {filter}")
        start_day, end_day, limit = filter
        dir = create_date_directory(start_day, end_day)
        load_results_page(driver, start_day, end_day, limit)
        process_results_page(driver, dir)
        driver.quit()

    # dir = create_date_directory('01/04/2023', '30/04/2023')
    # results_loaded = load_results_page(driver, '01/04/2023', '30/04/2023', '10')
    # process_results_page(driver, dir)

    # Don't forget to close the browser when you're done
