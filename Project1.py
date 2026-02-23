import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

# check if url is given :
if len(sys.argv) < 2:
    print("please give a URL")
    sys.exit()

url = sys.argv[1]

# download the page
try:
    webpage = urlopen(url)
    data = webpage.read()
except:
    print("cannot open page")
    sys.exit()

# parse  html
soup = BeautifulSoup(data, "html.parser")

#  title

title = soup.find("title")
if title:
    print(title.get_text())
else:
    print("no title")


body = soup.find("body")

if body:
    # remove scripts and styles
    undesirable_tags = body.find_all(["script", "style"])
    for tag in undesirable_tags:
        tag.extract()
    
    # print body data
    text = body.get_text()
    for line in text.split("\n"):
        if line.strip():
            print(line.strip())
else:
    print("no body found")

## all links:
links_seen = set()
all_links = soup.find_all("a")

for link_tag in all_links:
    href = link_tag.get("href")
    
    if href and href not in links_seen:
        if not href.startswith("#"):
            print(href)
            links_seen.add(href)