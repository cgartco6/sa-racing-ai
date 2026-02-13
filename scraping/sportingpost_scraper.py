from playwright.sync_api import sync_playwright

def scrape_sportingpost_racecard(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector(".racecard")

        horses = []
        for row in page.query_selector_all(".runner-row"):
            name = row.query_selector(".runner-name").inner_text()
            jockey = row.query_selector(".runner-jockey").inner_text()
            trainer = row.query_selector(".runner-trainer").inner_text()
            rating = row.query_selector(".runner-rating").inner_text()
            horses.append({
                "name": name,
                "jockey": jockey,
                "trainer": trainer,
                "rating": float(rating)
            })
        browser.close()
        return horses
