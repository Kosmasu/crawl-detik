import json
import katalog_crawler
import artikel_crawler
import os

URL_KATALOG = "https://inet.detik.com/indeks"
namaFileKatalog = "katalog"
namaFileCorpus = "corpus"
resultdir = "hasil"

page = int(input("Jumlah page >> "))

print("crawling katalog...")
articles = katalog_crawler.crawl(URL_KATALOG, page)
# 1 page 20 artikel
print("katalog length:", len(articles)) 

# create hasil dir if not exist
if (not os.path.exists(resultdir) or not os.path.isdir(resultdir)):
  os.mkdir(resultdir)

with open(f"hasil/{namaFileKatalog}.json", 'w') as f:
  json.dump(articles, f)

corpus = []
for index, article in enumerate(articles):
  print(f"{index + 1}.\tcrawling article...")
  temp = artikel_crawler.crawl(article["link"])
  if temp:
    corpus.append(temp)
    print(f"\tberhasil.")
  else:
    print(f"\tgagal.")
    

with open(f"hasil/{namaFileCorpus}.json", 'w') as f:
  json.dump(corpus, f)

print("done.")