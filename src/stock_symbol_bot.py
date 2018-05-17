import praw
from praw.exceptions import APIException
import re
import os
import dynamodb_client as db
import comment_parser as cparser
import comment_builder as cbuilder
import reddit_client as rc
import traceback

subreddit_name = 'robinhood'
submissions_limit = 15
exclude_submissions = ['referral']

try:

  is_fresh_comment_found = False
  submissions = rc.get_submissions(subreddit_name, submissions_limit)
  for submission in submissions:
    title = submission.title
    if any(word in title.lower() for word in exclude_submissions):
      print("Skipping submission : %s " % title)
      continue
    print("Processing submission : %s" % title)
    fresh_comment = rc.get_fresh_comment_with_symbols(submission)
    if fresh_comment is None:
      continue
    is_fresh_comment_found = True
    print("Found fresh comment in submission : %s with comment id : %s " % (title, fresh_comment.id))
    break;

  if fresh_comment is not None:
    symbols = cparser.parse_comment(fresh_comment)
    symbols = list(sorted(set(symbols)))
    #print(symbols)
    if len(symbols) < 8:
      bot_comment = cbuilder.build_bot_comment(symbols)
      print("\nBot generated comment in response to comment id %s : \n%s" % (fresh_comment.id, bot_comment) )
      response_comment = fresh_comment.reply(bot_comment)
      #response_comment = comment # uncomment for testing without the api call
    else:
      print("Skipping comment with 8 or more symbols : %s" % fresh_comment.id)
  else:
    print("No fresh comment found")

  if (is_fresh_comment_found and response_comment is not None and response_comment.id is not None):
    db.mark_item_visited(fresh_comment.id)
    print("Marking comment id %s as replied" % fresh_comment.id)

except Exception as e:
  print(e)
  print("Program Terminated")
