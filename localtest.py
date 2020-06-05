from handler import lambda_handler
#from api import lambda_handler
import os

os.environ['key'] = ''

event = {}
event['queryStringParameters'] = {}
event['queryStringParameters']['key'] = ''
event['queryStringParameters']['region'] = 'us-east-1'
event['queryStringParameters']['custom'] = 'SES'


lambda_handler(event, '')