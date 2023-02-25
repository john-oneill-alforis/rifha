import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
}
content = None

# make a request to the website
url = "https://www.bleepingcomputer.com/news/security/europol-busts-ceo-fraud-gang-that-stole-38m-in-a-few-days/"
response = requests.get(url, headers=headers)

# parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")


# Ugly way of doing this - need to find something a little more efficient
# than three seperate loops
for x in soup.find_all("div", {"class": "cz-related-article-wrapp"}):
    x.decompose()

for x in soup.find_all("h3"):
    x.decompose()

for x in soup.find_all("h2"):
    x.decompose()

intial_text = soup.findAll("div", {"class": "articleBody"})[0].text


print(intial_text)


# print the extracted links
# print(links)
