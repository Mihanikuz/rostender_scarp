from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from config import AUTH_URL, TENDERS_URL, CSV_FOLDER, CSV_INPUT_FILENAME
import csv
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def login_and_parse(driver):
    try:
        # Авторизация
        driver.get(AUTH_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Авторизация прошла успешно")

        # Переход на первую страницу тендеров
        page_num = 1
        tenders = []
        while True:
            url = f"{TENDERS_URL}?page={page_num}"
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tender-row"))
            )
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Парсинг ссылок на тендеры
            tender_links = soup.find_all('a', class_='tender-info__link')
            for link in tender_links:
                title = link.get('title', '').strip()
                href = link.get('href', '').strip()
                full_url = f"https://rostender.info{href}"
                tenders.append([title, full_url])

            # На первой итерации определяем номер последней страницы
            if page_num == 1:
                last_page = soup.find('input', {'name': 'page'})['max']
                last_page = int(last_page)
                print(f"Номер последней страницы: {last_page}")

            print(f"Страница {page_num} обработана, найдено {len(tender_links)} тендеров.")
            if page_num >= last_page:
                break
            page_num += 1

        # Сохраняем в CSV
        os.makedirs(CSV_FOLDER, exist_ok=True)
        csv_path = os.path.join(CSV_FOLDER, CSV_INPUT_FILENAME)
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['name', 'link'])
            writer.writerows(tenders)
        print(f"Выгружено {len(tenders)} тендеров в {csv_path}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    driver = setup_driver()
    login_and_parse(driver)