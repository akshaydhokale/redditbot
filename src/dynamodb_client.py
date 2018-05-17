import boto3

def mark_item_visited(itemid):
  dynamodb = boto3.resource('dynamodb')
  visited_items = dynamodb.Table('visiteditems')

  visited_items.put_item(
           Item={
               'postcommentid': itemid
            }
        )
  return True

def check_item_visited(itemid):
  #print("checking item visited #%s#" % itemid)
  dynamodb = boto3.resource('dynamodb')
  visited_items = dynamodb.Table('visiteditems')
  #print("Instanciated the table")
  response = visited_items.get_item(Key={'postcommentid': itemid})
  #print("done calling dynamo")
  if 'Item' in response:
    item = response['Item']
  else:
    item = None
  return item

