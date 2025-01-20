import streamlit as st
from scraper import scrape_with_selenium
import pandas as pd

# Streamlit app
st.title("Dynamic Web Scraper")
st.markdown("Enter the URL of a website and select the elements you want to scrape.")

# User inputs
url = st.text_input("Enter website URL:", "https://example.com")
elements_to_scrape = st.multiselect(
    "Select elements to scrape:",
    ["Headings", "Links", "Paragraphs", "Images"]
)
custom_selector = st.text_input(
    "Optional: Enter a custom CSS selector to scrape specific elements (e.g., '.class-name'):"
)
pagination = st.checkbox("Enable pagination?")
pagination_param = st.text_input(
    "Pagination query parameter (e.g., 'page'):", "" if not pagination else "page"
)
page_limit = st.slider("Number of pages to scrape:", 1, 10, 5 if pagination else 1)

# Scrape button
if st.button("Scrape"):
    if not url or not elements_to_scrape:
        st.error("Please enter a valid URL and select elements to scrape.")
    else:
        st.info("Scraping in progress...")
        results = scrape_with_selenium(
            url,
            browser_mode=True,
            elements=elements_to_scrape,
            custom_selector=custom_selector,
            pagination=pagination,
            pagination_param=pagination_param,
            page_limit=page_limit,
        )

        if "error" in results:
            st.error(f"An error occurred: {results['error']}")
        else:
            # Display results
            for key, value in results.items():
                if value:
                    st.write(f"### {key.capitalize()}")
                    if key == "images":
                        for img_url in value:
                            st.image(img_url, caption=img_url, use_column_width=True)
                    else:
                        st.write(pd.DataFrame({key: value}))
