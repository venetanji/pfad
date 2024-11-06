# Best used in REPL (shift+enter to run selected lines)
import gensim.downloader
wv = gensim.downloader.load('fasttext-wiki-news-subwords-300')

vec_rome = wv.get_vector("rome")
vec_italy = wv.get_vector("italy")
vec_france = wv.get_vector("france")
result = wv.similar_by_vector(vec_rome - vec_italy + vec_france, topn=1)