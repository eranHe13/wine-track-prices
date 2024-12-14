from bs4 import BeautifulSoup
from selenium import webdriver
from similarity import compute_similarity


def create_empty_wine():
    """Creates an empty wine object."""
    return {
        "id": None,
        "name": None,
        "regular_price": None,
        "club_price": None,
        "sale_price": None,
        "url": None,
        "image_url": None
    }


def extract_field(soup, selector, attribute=None, default=None):
    """
    Utility function to extract fields from a BeautifulSoup object.
    :param soup: BeautifulSoup object
    :param selector: CSS selector to find the element
    :param attribute: Attribute to extract, or None to get text content
    :param default: Default value if the element is not found
    :return: Extracted value or default
    """
    element = soup.select_one(selector)
    if element:
        if attribute:
            return element.get(attribute, default)
        return element.get_text(strip=True)
    return default


def scrape(name):
    url = f'https://www.paneco.co.il/catalogsearch/result/?q={name}'

    # Selenium WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Parse the HTML content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the product list
        product_list = soup.select_one(
            "#amasty-shopby-product-list > div.products.wrapper.assssssssss.grid.products-grid.amscroll-page > ol"
        )

        if not product_list:
            return create_empty_wine()  # Return an empty wine object if the product list is not found

        print("Product list found")

        # Find the first product in the list
        first_li = product_list.find('li', class_="item product product-item")

        if not first_li:
            return create_empty_wine()  # Return an empty wine object if no products are found

        print("First product found")

        # Extract necessary fields
        link_tag = first_li.find("a", class_="product photo product-item-photo")
        product_name = link_tag.get("data-name") if link_tag else None
        product_href = link_tag.get("href") if link_tag else None
        img_tag = link_tag.find("img", class_="product-image-photo") if link_tag else None
        product_img_url = img_tag.get("src") if img_tag else None

        # Check similarity
        if product_name and compute_similarity(product_name, name) < 0.85:
            print("ValueError: The wine name does not match closely enough.")
            raise ValueError

        regular_price = extract_field(first_li, "span[id^='product-price-']", "data-price-amount")
        sale_price = extract_field(first_li, "div.info-sales-message")

        # Construct wine object
        wine = {
            "id": None,  # Placeholder for ID, can be updated if available
            "name": product_name,
            "regular_price": regular_price,
            "club_price": None,  # Placeholder for club price, can be updated if available
            "sale_price": sale_price,
            "url": product_href,
            "image_url": product_img_url
        }

        return wine

    except ValueError:
        # Return an empty wine object if similarity check fails
        return create_empty_wine()

    except Exception as e:
        print(f"An error occurred: {e}")
        # Return an empty wine object on error
        return create_empty_wine()

    finally:
        # Ensure the driver quits in all cases
        driver.quit()


