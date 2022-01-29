from service.scraper_data import CandidatesScrape


def scraping(start_page=1, stop_page=0, sleep_time_page=0):
    candidates_scrape = CandidatesScrape()
    candidates_scrape.scrape_url(start_page, stop_page, sleep_time_page)
