from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import time
from config import setup_logging, get_db_creds
from werkzeug.datastructures import FileStorage
import os
from url import load_url
from sitemap import load_sitemap
from embed_process import embed_docs
from pymongo import MongoClient
from werkzeug.exceptions import BadRequest

# Set up logging
logger = setup_logging()

# Set up MongoDB
MONGODB_URI, MONGODB_DB_NAME = get_db_creds()
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/addUrl', methods=['POST'])
def process_url():
    start_time = time.time()
    urls = request.json['urls']
    for url in urls:
        if not db.urls.find_one({'url': url}):
            logger.info(f'Processing {url}...')
            urls_data = load_url([url])
            embed_docs(urls_data)
            db.urls.insert_one({'url': url})
        else:
            logger.info(f'URL {url} already processed')
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000  # convert to milliseconds
    logger.info(f'Successfully handled {urls} in {processing_time:.0f} milliseconds')
    return jsonify({'message': 'URLs handled successfully'}), 200

@app.route('/addSiteMap', methods=['POST'])
def process_sitemap():
    start_time = time.time()
    sitemap = request.json['sitemap']
    if not db.sitemaps.find_one({'sitemap': sitemap}):
        sitemap_data = load_sitemap(sitemap)
        embed_docs(sitemap_data)
        db.sitemaps.insert_one({'sitemap': sitemap})
    else:
        logger.info(f'Sitemap {sitemap} already processed')
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000  # convert to milliseconds
    logger.info(f'Successfully handled {sitemap} in {processing_time:.0f} milliseconds')
    return jsonify({'message': 'Sitemap handled successfully'}), 200

@app.route('/askQuestion', methods=['POST'])
def process_question():
    question = request.json['question']
    # Handle the question here
    # Return a success message if the question is handled successfully
    return jsonify({'message': 'Question handled successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
