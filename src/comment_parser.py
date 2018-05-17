import praw
from praw.exceptions import APIException
import pdb
import re
import os

#### Parsing comments

def parse_symbols_in_comments(comments):
  try:
    symbols = []
    for comment in comments:
      matches = parse_comment(comment)
      if len(matches) > 0:
        symbols.extend(matches)
  except:
      print("Exception while parsing for symbols in comments")
  return symbols

def parse_comment(comment):
  try:
    matches = re.findall(r'\$[a-zA-Z]+', comment.body)
  except:
    matches = []
    print("Exception while parsing comment : %s" % comment.body)
    print("comment id : %s" % comment.id)
  return matches


