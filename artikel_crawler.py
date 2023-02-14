import requests
import re

def removesuffix(line,suffix):
  if line.endswith(suffix):
   line_new = line[:-len(suffix)]
  return line_new

# def rstrip(self):
#   return self

def crawl(url):
  text = requests.get(url).text
  page = {}

  # find first article tag
  try:
    article = re.search(r"<article([\s\S\n]*?)>([\s\S\n]+?)</article>", text).group(2)
    del text
  except:
    print("\terror crawl first article tag!\n url:", url)
    return None

  # f = open("coba.html", "w", encoding="utf-8")
  # f.write(article)
  # f.close()
  # del f

  # parsing header
  try:
    header = re.search(r"<div class=\"detail__header\">([\s\S\n]+?)detail__date([\s\S\n]+?)</div>", article).group()
    page["title"] = re.search(r"<h1 class=\"detail__title\">([\s\S\n]+?)</h1>", header).group(1).strip()
    author = re.search(r"<div class=\"detail__author\">([\s\S\n]+?)<span", header).group(1).strip()
    removesuffix(author,"-")
    page["author"] = author.rstrip()
    page["date"] = re.search(r"<div class=\"detail__date\">([\s\S\n]+?)</div>", header).group(1).strip()
    del header
  except Exception as inst:
    print(inst)
    print("\terror crawl header!\n url:", url)
    return None

  # parsing content
  try:
    body = re.search(r"<div([\s\S\n]+?)id=\"detikdetailtext\">([\s\S\n]+?)detail__body-tag([\s\S\n]+?)</div>", article).group(2)
    page["contents"] = re.findall(r"<p>([^<>]+?)</p>", body)
    del body
  except:
    print("\terror crawl body!\n url:", url)
    return None
  return page

