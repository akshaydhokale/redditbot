import praw
from praw.exceptions import APIException
import dynamodb_client as db
import comment_parser as cparser 
from praw.models import MoreComments

bot_name = 'stock-symbol-bot'

def get_submissions(subreddit_name, submissions_limit):
  reddit = praw.Reddit(bot_name)
  subreddit = reddit.subreddit(subreddit_name)
  submissions = subreddit.hot(limit = submissions_limit)
  return submissions

def get_submission(titlewords):
  # Create reddit instance
  reddit = praw.Reddit(bot_name)

  print("Executing.....")
  # Select subreddit
  subreddit = reddit.subreddit(subreddit_name)
  for submission in subreddit.hot(limit = submissions_limit):
    #print(submission.title)
    print("...")
    if titlewords[0] in submission.title.lower() and titlewords[1] in submission.title.lower():
      print("Thread Found : " + submission.title)
      return submission
  
  return None

def check_if_replied(comment):
  #print('Comment ID : %s'% comment.id)
  dbitem = db.check_item_visited(comment.id)
  #print("dbitem : %s " % dbitem)
  #print("*\n")
  if dbitem is not None and comment.id == dbitem['postcommentid']:
    print("Comment previously replied : %s" % comment.id)
    return True
  return False

def get_fresh_comment_with_symbols(submission):
  comments = submission.comments
  print("Processing %d comments in this submission" % len(comments))
  for top_level_comment in comments:

    if isinstance(top_level_comment, MoreComments):    
      continue

    is_replied = check_if_replied(top_level_comment)

    if is_replied is True:
      continue
    
    symbols = cparser.parse_comment(top_level_comment)
    if len(symbols) > 0:
      print("Fresh comment found : %s" % top_level_comment.id)
      return top_level_comment
  return None
        
