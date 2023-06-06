## Project Title: LangChain chatbot to chat with any website

The project in question is a web application built with Flask, leveraging the Langchain library to facilitate a chatbot. The Langchain tool also plays a crucial role in processing URLs and sitemaps. This chatbot utilizes OpenAI's GPT-3.5 model to perform natural language processing and comprehension. To manage vector storage, the FAISS library is deployed, while MongoDB serves as the database solution for data persistence, storing and retrieving the chatbot's memory efficiently.

### Project Structure

The project is organized into several Python scripts, each with its specific function:

- `app.py`: This is the primary Flask application script, responsible for setting up the web server and defining the application's routes.

- `Chatbot.py`: This script houses the `Chatbot` class, which manages user interactions with the chatbot.

- `embed_process.py`: This script is tasked with embedding and indexing documents for the chatbot.

- `sitemap.py` and `url.py`: These scripts take on the job of loading data from sitemaps and URLs respectively.

- `User.py`: This script introduces the `User` class, representing a user interacting with the chatbot.

- `memory.py`: This script takes care of the chatbot's memory, enabling it to recall past interactions with users.

- `config.py`: This script is a crucial component, handling multiple tasks such as loading environment variables, retrieving OpenAI API Key, MongoDB credentials, and setting up logging with both general and error log handlers. It ensures that log files are rotated daily, and it creates a log directory if it doesn't exist. It also has a custom formatter class for timestamps in logs, which converts time to UTC.

### Installation

To install and run this project, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/ademarc/langchain-chat-website.git
cd langchain-chat-website
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Install `libmagic`:

If you're using a Unix-like operating system (like Linux or macOS), you can usually install `libmagic` using your system's package manager. For example, on a Debian-based Linux system (like Ubuntu), you can install `libmagic` using `apt`:

```bash
sudo apt-get update
sudo apt-get install libmagic1
```

On macOS, you can use Homebrew:

```bash
brew install libmagic
```

If you're using a Python environment, you might also need to install the `python-magic` package, which is a Python interface to the `libmagic` file type identification library. You can install it using `pip`:

```bash
pip install python-magic
```

4. Set up your environment variables:

Copy the `.env.sample` file to a new file named `.env` and fill in the required environment variables.

5. Run the application:

```bash
python app.py
```

The application will start running on `http://127.0.0.1:5000`.

## Usage

The application provides three main endpoints:

- `/addUrl`: This endpoint accepts a POST request with a JSON body containing a list of URLs to be processed by the chatbot. 

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"urls": ["https://example.com", "https://anotherexample.com"]}' http://127.0.0.1:5000/addUrl
    ```

- `/addSiteMap`: This endpoint accepts a POST request with a JSON body containing a sitemap to be processed by the chatbot.

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"sitemap": "https://example.com/sitemap.xml"}' http://127.0.0.1:5000/addSiteMap
    ```

- `/askQuestion`: This endpoint accepts a POST request with a JSON body containing a user ID and a message input. The chatbot will process the message and return a response.

    Example request:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"user_id": "12345", "message_input": "Hello, chatbot!"}' http://127.0.0.1:5000/askQuestion
    ```

## Author

This project was created by Marcus Adebayo.

---

### .env.sample

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=langchain
OPENAI_API_KEY=your_openai_api_key
```

Replace `mongodb://localhost:27017` with your MongoDB URI and `your_openai_api_key` with your OpenAI API key.