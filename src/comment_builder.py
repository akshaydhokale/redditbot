import praw
from praw.exceptions import APIException
import pdb
import re
import os

#### Building comments

def append_comment_header_footer(comment_text):
  #print("appending header footer")
  header = "Google search links:\n\n"
  footer = ""
  comment_polished = "%s%s%s" % (header, comment_text, footer)
  #print("done appending header footer")
  return comment_polished

def build_symbol_link(symbol):
  link_format = "[%s](https://www.google.com/search?q=%s+stock)"
  symbol_link = link_format % (symbol,symbol[1:])
  #print(symbol_link)
  return symbol_link

def build_symbols_comment_list(symbols):
  #print("building symbols comment text")
  comment = []
  for symbol in symbols:
    symbol_link = build_symbol_link(symbol)
    comment.append("* %s \n" % symbol_link)

  output = "".join(comment)
  return output

def build_bot_comment(symbols):
  #print("building bot comment")
  symbol_links_list = build_symbols_comment_list(symbols)
  #print(symbol_links_list)
  comment_body = append_comment_header_footer(symbol_links_list)
  return comment_body

def build_symbols_comment_table(symbols):
  #print("building symbols comment text")
  max_cols = 8
  if len(symbols) < 8:
    max_cols = len(symbols)

  comment = []
  # first line of the table
  for x in range(max_cols):
    comment.append(str(x+1))
    comment.append('|')

  comment.append('\n')

  # second line of the table
  for y in range(max_cols):
    comment.append('-')
    comment.append('|')

  comment.append('\n')

  # Add stock symbols to the table
  count = 0
  for symbol in symbols:
    symbol_link = build_symbol_link(symbol)
    comment.append(symbol_link)
    comment.append('|')
    count += 1
    if count % 8 == 0:
      #print("***")
      comment.append('\n')

  output = "".join(comment)
  return output
