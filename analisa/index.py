#conda install -n nlp beautifulsoup4
#conda install -n nlp lxml

from bs4 import BeautifulSoup
from nltk import bigrams, trigrams, ngrams, word_tokenize
from collections import Counter, defaultdict
import random, math

with open('hasil/corpus.xml', 'r', encoding='utf8') as f:
  corpus = BeautifulSoup(f.read(), 'xml') 

# - berapa jumlah kata unik
# - rata-rata kata per kalimat
# - rata-rata panjang kalimat per dokumen

from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

wordCount = 0
sentenceCount = 0
documentCount = 0
uniqueWords = set()

documents = corpus.findAll('doc')
documentCount = len(documents)
for document in documents:
  sentences = document.findAll('s')
  sentenceCount += len(sentences)
  for sentence in sentences:
    words = tokenizer.tokenize(sentence.string)
    wordCount += len(words)
    for word in words:
      uniqueWords.add(word)

print("wordCount:", wordCount)
print("sentenceCount:", sentenceCount)
print("documentCount:", documentCount)

print("amount of unique words:", len(uniqueWords))
print("avg word in sentence:", wordCount/sentenceCount)
print("avg sentence in document:", sentenceCount/documentCount)

# Create a placeholder for model
model = defaultdict(lambda: defaultdict(lambda: 0))

# Count frequency of co-occurance
documents = corpus.findAll('doc')
for document in documents:
  sentences = document.findAll('s')
  # print(sentences[0].text)
  for sentence in sentences:
    for w1, w2, w3 in ngrams(sentence.text.split(), 3, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        model[(w1, w2)][w3] += 1

# Let's transform the counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count

# print(model)
# print(dict(model["hari","ini"]))
# print(dict(model["samsung","galaxy"]))

prompt = ["hari","ini"]
sentence_buffer = prompt[:]
thres = 0.04 # pick words above threshold

for prompt_pointer in range(100):
  lmodel = dict(model[tuple(sentence_buffer[-2:])])
  ngram_sorted = {key: val for key, val in sorted(lmodel.items(), key = lambda ele: ele[1], reverse=True)}
  ngram_filtered = {key: val for key, val in ngram_sorted.items() if val > thres}
  
  picked_word = list(ngram_filtered.keys())[math.floor(random.random()*len(ngram_filtered))] # randomly pick eligible word
  if picked_word == "</s>": # break if end of sentence
    break
  
  sentence_buffer.append(picked_word)
  print(sentence_buffer)