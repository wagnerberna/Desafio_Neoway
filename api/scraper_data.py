from bs4 import BeautifulSoup
from service.process_data import ProcessData
from service.messages import *
import requests
import time


class CandidatesScrape:
    def __init__(self):
        self.stop_scraping = False

    def scrape_url(self, start_page=1, stop_page=0, sleep_time_page=0):
        page = start_page
        while not self.stop_scraping:
            time.sleep(sleep_time_page)
            self.scrape_page(page)

            if (page == stop_page):
                self.stop_scraping = True
                print(SCRAPING_COMPLETED.format(page))

            page = page + 1

    def scrape_page(self, page):
        cpfs_page = []
        endpoint = f"https://sample-university-site.herokuapp.com/approvals/{page}"
        req = requests.get(endpoint, timeout=5)
        soup = BeautifulSoup(req.text, "lxml")

        find_end_page = soup.find(string='Invalid page.')
        page_not_found = soup.find(string='404 page not found')

        if page_not_found:
            self.stop_scraping = True
            print(PAGE_NOT_FOUND)

        if find_end_page:
            self.stop_scraping = True
            print(SCRAPING_COMPLETED.format(page - 1))

        for child in soup.body.contents:
            if child.name == "li":
                cpfs_page.append(child.get_text())
            if child.name == "div":
                self.scrape_cpfs_list(cpfs_page)

    def scrape_cpfs_list(self, cpfs_page):
        if type(cpfs_page) is list:
            for cpf in cpfs_page:
                self.scrape_candidate(cpf)

    def scrape_candidate(self, candidate_cpf):
        cpf = candidate_cpf
        endpoint = f"https://sample-university-site.herokuapp.com/candidate/{cpf}"
        req = requests.get(endpoint)
        soup = BeautifulSoup(req.text, "lxml")

        path_name = soup.div.next_element
        name = path_name.next_element.next_element
        path_score = soup.div.next_sibling.next_sibling.next_element
        score = float(path_score.next_element.next_element)

        process_data = ProcessData()
        payload = process_data.process_payload(name, score, cpf)

        self.save_candidate(payload)

    def save_candidate(self, payload):
        url_post = "http://localhost:5000/register"

        resp = requests.post(url_post, json=payload)
        return resp.status_code


candidates_scrape = CandidatesScrape()
candidates_scrape.scrape_url(47, 50)
