from url_scraper import NaverNewsUrlScraper


if __name__ == "__main__":
    scraper = NaverNewsUrlScraper("노인", "new", 1, 100)
    scraper.scrape()