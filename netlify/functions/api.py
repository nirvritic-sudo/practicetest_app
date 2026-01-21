import serverless_wsgi
from app import app

# Netlify functions look for a 'handler' function
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)