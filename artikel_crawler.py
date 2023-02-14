import requests
import re

def crawl(url):
  text = requests.get(url).text
  page = {}

  # find first article tag
  article = re.search(r"<article([\s\S\n]*?)>([\s\S\n]+?)</article>", text).group(2)
  del text

  # f = open("coba.html", "w", encoding="utf-8")
  # f.write(article)
  # f.close()
  # del f

  # parsing header
  try:
    header = re.search(r"<div class=\"detail__header\">([\s\S\n]+?)detail__date([\s\S\n]+?)</div>", article).group()
    page["title"] = re.search(r"<h1 class=\"detail__title\">([\s\S\n]+?)</h1>", header).group(1).strip()
    page["author"] = re.search(r"<div class=\"detail__author\">([\s\S\n]+?)<span", header).group(1).strip().removesuffix("-").rstrip()
    page["date"] = re.search(r"<div class=\"detail__date\">([\s\S\n]+?)</div>", header).group(1).strip()
    del header
  except:
    print("\terror crawl header!\n url:", url)

  # parsing content
  try:
    body = re.search(r"<div([\s\S\n]+?)id=\"detikdetailtext\">([\s\S\n]+?)detail__body-tag([\s\S\n]+?)</div>", article).group(2)
    page["contents"] = re.findall(r"<p>([^<>]+?)</p>", body)
    del body
  except:
    print("\terror crawl body!\n url:", url)
  return page

