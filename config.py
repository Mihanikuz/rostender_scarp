# Настройки Chrome
CHROME_OPTIONS = {
    "headless": True,
    "disable_gpu": True,
    "no_sandbox": True
}

# URL для авторизации
AUTH_URL = https://rostender.info/registration/confirm?reg=3d184511f5c4509170dd2ce27f09decd&cid=c4cc7ad1ecdd94afc51f2e59cbf0387e"

# URL страницы тендеров
TENDERS_URL = "https://rostender.info/category/tendery-kvadrokoptery"

# Настройки сохранения
SAVE_SETTINGS = {
    "folder": "pages",
    "filename": "tender_page_{page}.html"
}

# Путь и имена файлов для сохранения CSV
CSV_FOLDER = "csv"
CSV_INPUT_FILENAME = "tenders_tree.csv"
CSV_OUTPUT_FILENAME = "tenders.csv"

# Дополнительные опции Chrome
CHROME_OPTIONS_EXTRA = [
    "--start-maximized",
    "--ignore-certificate-errors"
]

# Задержки (в секундах)
PAGE_LOAD_DELAY = 2
AUTH_DELAY = 5

# XPATH-ы для элементов тендера
TENDER_XPATHS = {
    'number': '//div[contains(@class, "tender-info-header-number")]',
    'date': '//div[contains(@class, "tender-info-header-start_date")]',
    'title': '//h1[contains(@class, "tender-header__h4")]',
    'initial_price': '//span[@class="tender-body__label"][contains(text(), "Начальная цена")]/following-sibling::span//span[@class="tender-body__text"]',
    'company_inn': '//span[@class="tender-body__label"][contains(., "ИНН")]/following-sibling::span[@class="tender-body__field"]',
    'company': '//span[contains(@class, "tender-info__text")]',
    'location': '//div[@data-id="place"]',
    'contact_person': '//span[@class="tender-body__label"][contains(.,"Контактное лицо")]/following-sibling::span[@class="tender-body__field"]',
    'phone': '//span[@class="tender-body__label"][contains(.,"Телефон")]/following-sibling::span[@class="tender-body__field"]',
    'email': '//span[@class="tender-body__label"][contains(.,"Электронная почта")]/following-sibling::span[@class="tender-body__field"]',
    'customer_analysis_link': "//a[contains(., 'Анализ заказчика')]"
}

# XPATH-ы для анализа заказчика
ANALYSIS_XPATHS = {
    'inn': '//ul[@class="list pb-0 mb-0 list--13"]/li[contains(., "ИНН:")]',
    'address': '//div[@class="row mb-4"]/div[1]/div[2]',
    'phones_comp': '//div[contains(@class, "col-md-3")]//div[contains(@data-id, "phone")]/div[contains(., "+")]',
    'email_comp': '//div[contains(@class, "col-md-4")]//div[contains(@data-id, "emails")]/div[contains(., "@")]'
}