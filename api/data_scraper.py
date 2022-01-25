from array import array
from bs4 import BeautifulSoup
import requests


class CandidateScrape:
    # def __init__(self, ):
    #     self.start_page = start_page
    #     self.stop_page = stop_page

    def scrape_url(self, start_page, stop_page=4671):
        page = start_page
        cpfs_page = []
        endpoint = f"https://sample-university-site.herokuapp.com/approvals/{page}"
        print(endpoint)
        req = requests.get(endpoint)
        soup = BeautifulSoup(req.text, 'lxml')

        for child in soup.body.contents:
            print(child.name)
            if child.name == 'li':
                cpfs_page.append(child.get_text())
            if child.name == 'div':
                print('fim da página')
                self.scrape_cpfs_page(cpfs_page)

        print(cpfs_page)

    def scrape_cpfs_page(self, cpfs_page):
        if type(cpfs_page) is list:
            for cpf in cpfs_page:
                self.scrape_candidate(cpf)

    def scrape_candidate(self, candidate_cpf):
        cpf = candidate_cpf
        endpoint = f"https://sample-university-site.herokuapp.com/candidate/{cpf}"
        req = requests.get(endpoint)
        soup = BeautifulSoup(req.text, "lxml")
        # print(req.url)
        # print(soup)
        path_name = soup.div.next_element
        # print(path_name)
        name = path_name.next_element.next_element
        # print(name)
        path_score = soup.div.next_sibling.next_sibling.next_element
        # print(path_score)
        score = float(path_score.next_element.next_element)
        # print(score)

        url_post = "http://localhost:5000/register"
        payload = {"name": name, "score": score, "cpf": cpf}

        resp = requests.post(url_post, json=payload)
        print(resp.status_code)
        return resp.status_code


if __name__ == "__main__":

    scraper_candidates = CandidateScrape()

    # scraper_candidates.scrape_candidate("178.422.117-11")
    scraper_candidates.scrape_url(5)
