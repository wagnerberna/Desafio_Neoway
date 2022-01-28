from bs4 import BeautifulSoup
from service.process_data import ProcessData
import requests
import time


class CandidatesScrape:
    def __init__(self):
        self.stop_scrapping = False

    def scrape_url(self, start_page=1, stop_page=0, sleep_time_page=0):
        page = start_page
        print(f"page start {page}")
        while not self.stop_scrapping:
            time.sleep(sleep_time_page)
            self.scrape_page(page)
            page = page + 1

            if (page == stop_page + 1):
                self.stop_scrapping = True

    def scrape_page(self, page):
        print(f"page fn scraper {page}")
        cpfs_page = []
        endpoint = f"https://sample-university-site.herokuapp.com/approvals/{page}"
        req = requests.get(endpoint, timeout=5)
        soup = BeautifulSoup(req.text, "lxml")
        find_end_page = soup.find(string='Invalid page.')

        if find_end_page:
            self.stop_scrapping = True

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
candidates_scrape.scrape_url(100, 105)
