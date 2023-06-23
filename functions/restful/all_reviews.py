from bs4 import BeautifulSoup
import requests
import time

# 64 pages max for this test example (handy later)
URL = "https://www.amazon.in/Baseus-Screenbar-Adjustable-Brightness-Temperature/dp/B08CXL3YQ8/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

# used for rotation
USER_AGENTS = ["", "", "", "", ""]


def all_reviews(URL, headers):
    BASE_URL = (
        "https://www." + URL.split(".")[1] + "." + URL.split(".")[2].split("/")[0]
    )

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    see_all_reviews_anchor = soup.find(attrs={"data-hook": "see-all-reviews-link-foot"})

    all_reviews_URL = BASE_URL + see_all_reviews_anchor["href"]
    all_reviews_URL_clean = "/".join(all_reviews_URL.split("/")[0:-1])

    reviews_page = requests.get(all_reviews_URL_clean, headers=headers)
    reviews_soup = BeautifulSoup(reviews_page.content, "html.parser")

    all_reviews_parse_tree_list = reviews_soup.find_all(attrs={"data-hook": "review"})

    MAX_PAGES = 2
    count = 1
    while not reviews_soup.find(class_="a-disabled a-last") and count <= MAX_PAGES:
        # single page reviews here
        for rev in all_reviews_parse_tree_list:
            print(rev.find(attrs={"data-hook": "review-title"}).get_text())
            print(rev.find(attrs={"data-hook": "review-body"}).get_text())
            print("")

        time.sleep(1)

        next_page_URL = reviews_soup.find("li", class_="a-last")
        next_page_URL = "https://amazon.in" + next_page_URL.contents[0]["href"]

        time.sleep(1)

        reviews_soup = BeautifulSoup(
            requests.get(next_page_URL, headers=headers).content, "html.parser"
        )
        all_reviews_parse_tree_list = reviews_soup.find_all(attrs={"data-hook": "review"})

        count += 1

all_reviews(URL, headers)
