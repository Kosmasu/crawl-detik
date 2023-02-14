import requests
import json
import re

def crawl(url, jumlahPage):
  for i in range(jumlahPage):
    text = requests.get(f"{url}/{i + 1}").text

    articles = []
    for match in re.finditer(r"<article([\s\S\n]+?)>([\s\S\n]+?)</article>", text):
      article = {}
      article["image"] = re.search(r"i-img=\'([\s\S]+?)\'", match.group(1)).group(1)
      article["datetime_epoch"] = re.search(r"d-time=\"([\s\S]+?)\"", match.group(1)).group(1)

      temp = re.search(r"class=\"media__title\"([\s\S\n]+?)</h3>", match.group(2)).group()
      article["title"] = re.search(r"dtr-ttl=\"([\s\S]+?)\"", temp).group(1)
      article["link"] = re.search(r"href=\"([\s\S]+?)\"", temp).group(1)
      articles.append(article)
  return articles