from array import array
from bs4 import BeautifulSoup
from unicodedata import normalize
from service.validate_cpf import validate_cpf
import requests
import time


class CandidateScrape:
    def scrape_url(self, start_page, stop_page=4671):

        for page in range(start_page, stop_page + 1):
            time.sleep(5)
            self.scrape_page(page)

    def scrape_page(self, page):
        cpfs_page = []
        endpoint = f"https://sample-university-site.herokuapp.com/approvals/{page}"
        req = requests.get(endpoint, timeout=2)
        soup = BeautifulSoup(req.text, 'lxml')

        for child in soup.body.contents:
            if child.name == 'li':
                cpfs_page.append(child.get_text())
            if child.name == 'div':
                self.scrape_cpfs_list(cpfs_page)
        print(f'page: {page}')
        print(cpfs_page)

    def scrape_cpfs_list(self, cpfs_page):
        if type(cpfs_page) is list:
            for cpf in cpfs_page:
                self.scrape_candidate(cpf)
                print(cpf)

    def scrape_candidate(self, candidate_cpf):
        cpf = candidate_cpf
        endpoint = f"https://sample-university-site.herokuapp.com/candidate/{cpf}"
        req = requests.get(endpoint)
        soup = BeautifulSoup(req.text, "lxml")

        path_name = soup.div.next_element
        name = path_name.next_element.next_element
        path_score = soup.div.next_sibling.next_sibling.next_element
        score = float(path_score.next_element.next_element)

        clean_name = name.lower().strip()
        clean_name = normalize('NFKD', clean_name).encode('ASCII', 'ignore').decode('utf-8')
        clean_cpf = cpf = ''.join([(char) for char in cpf if char.isdigit()])
        cpf_is_valid = validate_cpf(clean_cpf)

        payload = {"name": clean_name, "score": score, "cpf": clean_cpf, "valid_cpf": cpf_is_valid}
        self.save_candidate(payload)

    def save_candidate(self, payload):
        url_post = "http://localhost:5000/register"

        resp = requests.post(url_post, json=payload)
        print(resp.status_code)
        return resp.status_code


if __name__ == "__main__":

    scraper_candidates = CandidateScrape()

    # scraper_candidates.scrape_candidate("178.422.117-11")
    # print(validate_cpf('18563240790'))
    scraper_candidates.scrape_url(1006, 1006)
