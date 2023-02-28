import json
import katalog_crawler
import artikel_crawler
import os
from nltk.tokenize import sent_tokenize

URL_KATALOG = "https://inet.detik.com/indeks"
namaFileKatalog = "katalog"
#namaFileCorpus = "corpus"
namaFileCorpus = "corpus"
resultdir = "hasil"

page = int(input("Jumlah page >> "))

def writecorpus(s):
  with open(f"hasil/{namaFileCorpus}.xml", 'a', encoding="utf-8") as f:
    f.write(f"\n{s}")
  f.close()

print("crawling katalog...")
articles = katalog_crawler.crawl(URL_KATALOG, page)
# 1 page 20 artikel
print("katalog length:", len(articles)) 

# create hasil dir if not exist
if (not os.path.exists(resultdir) or not os.path.isdir(resultdir)):
  os.mkdir(resultdir)

with open(f"hasil/{namaFileKatalog}.json", 'w') as f:
  json.dump(articles, f)
  f.close()

corpus = []
with open(f"hasil/{namaFileCorpus}.xml", 'w', encoding="utf-8") as f:
  f.write("<corpus>")
f.close()

for index, article in enumerate(articles):
  print(f"{index + 1}.\tcrawling article...")
  url = article["link"]
  temp = artikel_crawler.crawl(article["link"])
  if temp:
    writecorpus(f"<doc id=\"{index + 1}\" url=\"{url}\">")
    corpus.append(temp)
    print(f"\tberhasil.")
    # process content
    # temp["contents"]
    # print(temp["contents"])
    for p in temp["contents"]:
      sentences = sent_tokenize(p)
      for s in sentences:
        writecorpus(f"<s>{s}</s>")
    writecorpus("</doc>")
  else:
    print(f"\tgagal.")
  

# with open(f"hasil/{namaFileCorpus}.json", 'w') as f:
#   json.dump(corpus, f)
#   f.close()

writecorpus("</corpus>")

print("done.")