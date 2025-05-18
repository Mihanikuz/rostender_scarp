from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def get_element_text(driver, xpath):
    try:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text.strip()
    except:
        return "Не найдено"
    
def get_element_href(driver, xpath):
    try:
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.get_attribute('href')
    except:
        return "Не найдено"

def scrape_tender_data(driver, url):
    try:
        # Переход на страницу тендера
        driver.get(url)
        time.sleep(2)
        print(f"Обрабатывается ссылка: {url}")

        # Основные данные тендера
        tender_data = {
            'number': get_element_text(driver, '//div[contains(@class, "tender-info-header-number")]'),
            'date': get_element_text(driver, '//div[contains(@class, "tender-info-header-start_date")]'),
            'title': get_element_text(driver, '//h1[contains(@class, "tender-header__h4")]'),
            'initial_price': get_element_text(driver, '//span[@class="tender-body__label"][contains(text(), "Начальная цена")]/following-sibling::span//span[@class="tender-body__text"]'),
            'company_inn': get_element_text(driver, '//span[@class="tender-body__label"][contains(., "ИНН")]/following-sibling::span[@class="tender-body__field"]'),
            'company': get_element_text(driver, '//span[contains(@class, "tender-info__text")]'),
            'location': get_element_text(driver, '//div[@data-id="place"]'),
            'contact_person': get_element_text(driver, '//span[@class="tender-body__label"][contains(.,"Контактное лицо")]/following-sibling::span[@class="tender-body__field"]'),
            'phone': get_element_text(driver, '//span[@class="tender-body__label"][contains(.,"Телефон")]/following-sibling::span[@class="tender-body__field"]'),
            'email': get_element_text(driver, '//span[@class="tender-body__label"][contains(.,"Электронная почта")]/following-sibling::span[@class="tender-body__field"]'),
            'link': url,
            'customer_analysis_link': get_element_href(driver, "//a[contains(., 'Анализ заказчика')]")
        }

        # Переход на страницу анализа заказчика
        if tender_data['customer_analysis_link'] != "Не найдено":
            driver.get(tender_data['customer_analysis_link'])
            time.sleep(5)

            # Данные анализа заказчика
            analysis_data = {
                'inn': get_element_text(driver, '//ul[@class="list pb-0 mb-0 list--13"]/li[contains(., "ИНН:")]').replace('ИНН:', '').strip(),
                'address': get_element_text(driver, '//div[@class="row mb-4"]/div[1]/div[2]').strip(),
                'phones_comp': ', '.join([p.text.strip() for p in driver.find_elements(By.XPATH, '//div[contains(@class, "col-md-3")]//div[contains(@data-id, "phone")]/div[contains(., "+")]')]) or None,
                'email_comp': ', '.join([e.text.strip() for e in driver.find_elements(By.XPATH, '//div[contains(@class, "col-md-4")]//div[contains(@data-id, "emails")]/div[contains(., "@")]')]) or None
            }
        else:
            analysis_data = {
                'inn': "Не найдено",
                'address': "Не найдено",
                'phones_comp': "Не найдено",
                'email_comp': "Не найдено"
            }

        # Подсчет количества полученных данных
        data_count = sum(1 for value in {**tender_data, **analysis_data}.values() if value != "Не найдено")
        print(f"Получено данных: {data_count} из {len(tender_data) + len(analysis_data)}")

        # Объединение данных
        return {**tender_data, **analysis_data}
        
    except Exception as e:
        print(f"Ошибка при обработке {url}: {str(e)}")
        return None

def process_tenders(input_csv, output_csv):
    # Инициализация драйвера
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Авторизация (выполняется один раз)
        auth_url = "https://rostender.info/registration/confirm?reg=2283d14fc0f165ef777ccb9eaf8dc85d&cid=912342cd7b46444429d926c04953ee9b"
        print("Выполняется авторизация...")
        driver.get(auth_url)
        time.sleep(5)
        print("Авторизация успешно завершена")

        # Чтение CSV файла с ссылками
        with open(input_csv, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            links = [row['link'] for row in reader if row['link']]
        
        results = []
        total_links = len(links)
        print(f"\nНайдено ссылок для обработки: {total_links}")
        
        for i, link in enumerate(links, 1):
            print(f"\nОбработка ссылки {i} из {total_links}")
            result = scrape_tender_data(driver, link)
            if result:
                results.append(result)
                print(f"Успешно обработано: {i}/{total_links}")
            else:
                print(f"Ошибка обработки: {i}/{total_links}")
        
        if results:
            with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(results)
            print(f"\nРезультаты сохранены в {output_csv}")
            print(f"Успешно обработано тендеров: {len(results)} из {total_links}")
        else:
            print("Не удалось получить данные ни по одному тендеру")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    process_tenders('csv/tenders_tree.csv', 'csv/tenders.csv')