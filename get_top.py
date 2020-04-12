import requests
from bs4 import BeautifulSoup

websites = {
    "BuzzFeed": ["https://www.buzzfeed.com/trending", ["featured-card__headline link-gray", "js-card__link link-gray"]],
    "CNN": ["https://www.cnn.com/specials/last-50-stories", ["cd__headline-text"]],
    "New York Times": ["https://www.nytimes.com/", ["css-1cmu9py esl82me0", "balancedHeadline"]],
    "Huffington Post": ["https://www.huffpost.com/news/topic/trending-topics", ["card__headline card__headline--long"]],
    "NBC News": ["https://www.nbcnews.com/latest-stories", ["headline___38PFH"]],
    "Washington Post": ["https://www.washingtonpost.com/", []],
    "Wall Street Journal": ["https://www.wsj.com/", []],
    "The Atlantic": ["https://www.theatlantic.com/most-popular/", ["hed"]],
    "ABC News": ["https://abcnews.go.com/", []],
    "The Onion": ["https://www.theonion.com/", ["sc-1qoge05-0 eoIfRA"]]
}


def get_top(site, n=10):
    top = {}
    s = requests.get(websites[site][0], headers={
                     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
    soup = BeautifulSoup(s.content, features="html.parser")
    if site == "BuzzFeed" or site == "Huffington Post":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}, href=True):
                top[j.get_text()] = j['href']
    elif site == "CNN":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                top[j.get_text()] = "https://cnn.com" + \
                    j.find_parent(href=True)['href']
    elif site == "New York Times":
        for j in soup.find_all("span", attrs={"class": None}):
            if j.find_parent(href=True) and "https://www.nytimes.com" not in j.find_parent(href=True)['href']:
                top[j.get_text()] = "https://www.nytimes.com" + \
                    j.find_parent(href=True)['href']
        for j in soup.find_all(attrs={"class": websites[site][1][0]}):
            top[j.get_text()] = "https://www.nytimes.com" + \
                j.find_parent(href=True)['href']
    elif site == "NBC News":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                top[j.get_text()] = j.find_parent(href=True)['href']
    elif site == "Washington Post":
        for j in soup.find_all(attrs={"data-pb-placeholder": "Write headline here"}, href=True):
            top[j.get_text().strip()] = j['href']
    elif site == "Wall Street Journal":
        l = soup.find_all("a", href=True)
        for i in range(len(l)):
            try:
                int(l[i].get_text())
                top[l[i-1].get_text()] = l[i-1]['href']
            except:
                pass
    elif site == "The Atlantic":
        for i in websites[site][1]:
            for j in soup.find_all(attrs={"class": i}):
                top[j.get_text().strip()] = "https://www.theatlantic.com" + \
                    j.find_parent(href=True)['href']
    elif site == "ABC News":
        for j in soup.find_all(attrs={"data-analytics": "cid=clicksource_4380645_3_mobile_web_only_headlines_headlines_hed"}, href=True):
            top[j.get_text()] = j['href']
    elif site == "The Onion":
        for j in soup.find_all(attrs={"class": websites[site][1][0]}):
            top[j.get_text()] = j.find_parent(href=True)['href']
    ans = {}
    k = list(top.keys())
    for i in range(n):
        if i < len(k):
            ans[k[i]] = top[k[i]]
    return ans


print(get_top("The Onion"))
