from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def init_driver(headless=True):
    """Initialize Selenium WebDriver with WebDriverManager."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_with_selenium(
    url, browser_mode=True, elements=None, custom_selector=None, pagination=False, pagination_param=None, page_limit=5
):
    """Scrape website with Selenium."""
    driver = init_driver(headless=browser_mode)
    results = {"headings": [], "links": [], "paragraphs": [], "images": [], "custom": []}
    try:
        for page in range(1, page_limit + 1 if pagination else 2):
            current_url = f"{url}?{pagination_param}={page}" if pagination and pagination_param else url
            driver.get(current_url)

            # Wait for the page to load completely
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")

            if "Headings" in elements:
                results["headings"].extend(
                    [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
                )

            if "Links" in elements:
                results["links"].extend(
                    [a["href"] for a in soup.find_all("a", href=True)]
                )

            if "Paragraphs" in elements:
                results["paragraphs"].extend(
                    [p.get_text(strip=True) for p in soup.find_all("p")]
                )

            if "Images" in elements:
                results["images"].extend(
                    [img["src"] for img in soup.find_all("img", src=True)]
                )

            if custom_selector:
                results["custom"].extend(
                    [el.get_text(strip=True) for el in soup.select(custom_selector)]
                )

            if not pagination or page == page_limit:
                break

        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()
