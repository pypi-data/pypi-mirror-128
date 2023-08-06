"""Main module."""

import copy,re
import numpy as np

def bind_tf_idf(df, term, document, n):
  """
  tf(t,d) = # of time term t occurs in document d / # words in document
  tf(i,j)=the number of occurrences of term t(i) in document d(j)

  df(t) = # of t in N documents
  idf(t) = ln(n documents) - ln(n documents containing terms)
   - n=the number of documents term t(i) occurs in
   - N=the number of documents in the collection
  tfidf = tf(t,d) * idf(t)
  """
  tot_by_group = df.groupby(document).size().reset_index(name="total")

  out = df.merge(tot_by_group, how='left', on=document)\
          .assign(tf = lambda x: x[n] / x['total'])
  
  N = len(df[document].unique())
  doc_totals = df.groupby(term).size()\
                               .reset_index(name="n_i")\
                               .assign(idf = lambda x: np.log10(N / x.n_i))\
                               .drop("n_i", axis=1)

  return out.merge(doc_totals, how="left", on=term)\
            .assign(tf_idf = lambda x: x.tf*x.idf)


#!TODO
def cast_dtm():
  """tidy to document term matrix readble in sklearn"""
  pass


def count(df, *args, name="n", sort = True):
  count_df = df.groupby(list(args))
  count_df = count_df.size().reset_index(name=name)
  if sort:
    return count_df.sort_values(name, ascending=False)
  else:
    return count_df


def only_alphnum(sent):
  """Returns string with only alphanumericals"""
  pattern = re.compile('[\W_]+')
  return ' '.join([pattern.sub('', w) for w in sent.split(" ")])


#!TODO
def tidy():
  """should be able to tidy object from sklearn"""
  pass


def top_n(df, by, within=None, n=15):
  if within is not None:
    return df.sort_values([within, by], ascending=False)\
           .groupby(within).head(n)
  else:
    return df.sort_values(by).head(n)

def _custom_bigram_toks(sent):
  return [b for b in zip(sent.split()[:-1], sent.split(" ")[1:]) 
          if (b[0] != b[1])]


def _ngrams(df, parsed_col, filter_stops: bool = True, filter_punct: bool = True):
  """
  Extract an ordered sequence of n-grams (``n`` consecutive tokens) from a spaCy
    ``Doc`` or ``Span``, for one or multiple ``n`` values, optionally filtering n-grams
    by the types and parts-of-speech of the constituent tokens.

  Adapted from https://textacy.readthedocs.io/en/0.11.0/_modules/textacy/extract/basics.html#ngrams
  """
  df[parsed_col] = df[parsed_col].map(lambda x: list((x[i : i + 2] for i in range(len(x) - 2 + 1))))
  df[parsed_col] = df[parsed_col].map(lambda x: list((ng for ng in x if not any(w.is_space for w in ng))))
  
  if filter_stops is True:
    df[parsed_col] = df[parsed_col].map(lambda x: list((ng for ng in x if not ng[0].is_stop and not ng[-1].is_stop)))
  if filter_punct is True:
    df[parsed_col] = df[parsed_col].map(lambda x: list((ng for ng in x if not any(w.is_punct for w in ng))))
  return df


def unnest_tokens(df, output, input, nlp, *args, to_lower:bool = True, **kwargs):
  """
  *kwargs takes the following args:
    - to_lower = {True, False}
    - token = {"words", "ngrams"}
    - n = 2

  *args can take the following: 
    - "tok2vec"
    - "tagger"
    - "parser"
    - "ner"
    - "attribute_ruler"
    - "lemmatizer"

  If empty, runs spacy default pipeline.

  return doc column so that we can use spacy methods.
  """
  copy_df = copy.deepcopy(df)
  arg_dict = kwargs
  token = "words" if arg_dict.get("token") is None else arg_dict['token']
  
  # Check if n is provided with ngrams
  if token == "ngrams":
    assert arg_dict.get("n") is not None, "n ngrams must be provideds" 
    n = arg_dict.get("n")
    assert n < 1, "n must be greater than 1"
    if n > 2:
      raise NotImplementedError

  # Discard NAs, if any.
  if any(copy_df[input].isna()): 
    copy_df = copy_df[~copy_df[input].isna()]
  
  if to_lower:
    copy_df[input] = copy_df[input].str.lower()
  
  if len(args) == 0: # Spacy default pipeline
    print(f"Pipeline: {nlp.pipe_names}")
    copy_df["txt_parsed"] = list(nlp.pipe(copy_df[input]))
    if token == "noun_chunks":
      copy_df["txt_parsed"] = copy_df.txt_parsed.map(lambda x: list(x.noun_chunks))
    
    # Ngram tokenizer using pipeline. slow but more flexible.
    elif (token == "ngrams") & (n == 2):
      _ngrams(copy_df, "txt_parsed")

  elif (len(args) == 1) & (list(args)[0] == "tok2vec"): # only tokenizer
    print(f"Pipeline: tokenizer")
    if token == "words":
      tokenizer = nlp.tokenizer
      copy_df["txt_parsed"] = list(tokenizer.pipe(copy_df[input], batch_size=50))
    
    # Custom bigram tokenizer. Fast but limited.
    elif (token == "ngrams") & (n == 2):
      copy_df["txt_parsed"] = copy_df[input].map(_custom_bigram_toks)
  
  else: # custom pipeline
    all_comps = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"]
    disabled_pipeline = [comp for comp in all_comps if comp not in list(args)]
    print(f"Pipeline: {list(args)}")
    with nlp.select_pipes(disable=disabled_pipeline):
      copy_df["txt_parsed"] = list(nlp.pipe(copy_df[input]))
  
  return copy_df.drop(input, axis=1)\
                .explode(["txt_parsed"], ", ")\
                .dropna()\
                .rename(columns={"txt_parsed": f"{output}"})\
                .reset_index(drop=True)
