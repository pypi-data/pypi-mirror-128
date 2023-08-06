#!/usr/bin/env python

"""Tests for `tidytxt` package."""
import pytest
import sys, copy
import pandas as pd
import spacy

sys.path.append("..")
from tidytxt.tidytxt import _ngrams, unnest_tokens

nlp = spacy.load("en_core_web_sm")

emma_sample = ["She was the youngest of the two daughters of a most affectionate,",
               "indulgent father; and had, in consequence of her sister's marriage, been",
               "mistress of his house from a very early period. Her mother had died",
               "too long ago for her to have more than an indistinct remembrance of",
               "her caresses; and her place had been supplied by an excellent woman as",
               "governess, who had fallen little short of a mother in affection.",
               "Sixteen years had Miss Taylor been in Mr. Woodhouse's family, less as a",
               "governess than a friend, very fond of both daughters, but particularly",
               "of Emma. Between _them_ it was more the intimacy of sisters. Even before",
               "Miss Taylor had ceased to hold the nominal office of governess, the"]


text_df = pd.DataFrame({"text":emma_sample})

def test_ngrams_return_bigrams():
  copy_df = copy.deepcopy(text_df)
  copy_df['parsed_text'] = list(nlp.pipe(copy_df['text']))
  _ngrams(copy_df, 'parsed_text')
  assert all(copy_df.parsed_text.explode(",").dropna().map(len) == 2)

def test_unnest_tokens_simple_whole_pipeline():
  assert len(unnest_tokens(text_df, "word", "text", nlp)) == 141

def test_unnest_tokens_custom_bigram():
  custom_bigrams=unnest_tokens(text_df, "word", "text", nlp, "tok2vec", token="ngrams", n=2)
  assert len(custom_bigrams) == 112

