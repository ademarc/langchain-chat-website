from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import time
from config import setup_logging, get_db_creds
from url import load_url
from sitemap import load_sitemap
from embed_process import embed_docs
from pymongo import MongoClient
from Chatbot import Chatbot

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
    start_time = time.time()
    try:

        if request.content_type == 'application/json':
            data = request.get_json()
            user_id = data.get('user_id')
            message_input = data.get('message_input')
        else:
            raise ValueError('Invalid content type')
        
        # Check if username, message_input and input_type are provided
        if not user_id or not message_input:
            raise ValueError('user_id and message_input are required')
        logger.info(f'Received message from user {user_id}')

        # Initialize chatbot
        chatbot = Chatbot()
        # Check if user exists in DB, if not create user
        user = chatbot.get_user(user_id)
        if not user:
            chatbot.create_user(user_id)
            user = chatbot.get_user(user_id)
        result = None  # Initialize result to a default value

        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # convert to milliseconds
        result = chatbot.ask_user_question(user_id, message_input)
        logger.info(f'Successfully processed message from user {user_id} in {processing_time:.0f} milliseconds')

        return jsonify(result), 200

    except ValueError as e:
        logger.error(f'Bad request: {e}')
        return jsonify({'error': 'Bad request'}), 400
    except Exception as e:
        logger.error(f'Server error: {e}')
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
