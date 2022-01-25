from bs4 import BeautifulSoup
import requests


class CandidateScrape:
    def __init__(self, url):
        self.url = url

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
        print(name)
        path_score = soup.div.next_sibling.next_sibling.next_element
        # print(path_score)
        score = float(path_score.next_element.next_element)
        print(score)

        url_post = "http://localhost:5000/register"
        payload = {"name": name, "score": score, "cpf": cpf}

        response = requests.post(url_post, json=payload)
        print(response)


if __name__ == "__main__":

    url = "https://sample-university-site.herokuapp.com/approvals/"
    inst_test = CandidateScrape(url)

    inst_test.scrape_candidate("178.422.117-11")
