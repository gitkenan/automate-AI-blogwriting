import os
import sys
import openai
import keyring
import logging
import subprocess
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from gnews import GNews
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    filename='daily_ai_blog.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Retrieve API keys and credentials securely
OPENAI_API_KEY = keyring.get_password('openai', 'api_key')
WORDPRESS_URL = os.getenv('WORDPRESS_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = keyring.get_password('wordpress', 'application_password')

# Validate credentials
if not all([OPENAI_API_KEY, WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
    logging.error("Missing credentials. Please ensure all credentials are set.")
    sys.exit("Missing credentials. Please ensure all credentials are set.")

def get_trending_ai_topics(num_topics=5):
    """Fetch trending AI topics using GNews."""
    try:
        google_news = GNews(language='en', country='US', max_results=num_topics)
        news = google_news.get_news('artificial intelligence')
        topics = [item for item in news]
        logging.info(f"Fetched {len(topics)} trending topics.")
        return topics
    except Exception as e:
        logging.error(f"Failed to fetch trending topics: {e}")
        return []

def rank_and_filter_topics(topics):
    """Rank topics based on keyword matching scores without strict filtering."""
    # Keywords to identify relevant topics
    relevant_keywords = [
        'tool', 'launch', 'release', 'announce', 'develop', 'create',
        'research', 'breakthrough', 'innovation', 'discover', 'introduce',
        'platform', 'software', 'application', 'system', 'technology',
        'open source', 'model', 'algorithm', 'neural', 'deep learning',
        'machine learning', 'transformer', 'llm', 'ai model', 'small business',
        'chatgpt', 'openai', 'microsoft', 'google', 'anthropic', 'meta'
    ]
    
    # Keywords to exclude (with lower negative impact)
    exclude_keywords = [
        'stock', 'market', 'invest', 'price', 'share', 'trading',
        'nasdaq', 'nyse', 'profit', 'revenue', 'earnings', 'dividend',
        'etf', 'fund', 'portfolio', 'buy', 'sell', 'investor',
        'financial', 'finance', 'bank', 'investment'
    ]
    
    ranked_topics = []
    for topic in topics:
        title = topic['title'].lower()
        description = topic.get('description', '').lower()
        combined_text = f"{title} {description}"
        
        # Calculate score based on keyword matches
        score = 0
        matched_relevant = []
        matched_excluded = []
        
        # Count relevant keyword matches (weight: +1)
        for keyword in relevant_keywords:
            if keyword in combined_text:
                score += 1
                matched_relevant.append(keyword)
        
        # Count excluded keyword matches (weight: -0.5 to reduce impact)
        for keyword in exclude_keywords:
            if keyword in combined_text:
                score -= 0.5
                matched_excluded.append(keyword)
        
        # Add all topics with their scores
        ranked_topics.append({
            'topic': topic,
            'score': score,
            'matched_relevant': matched_relevant,
            'matched_excluded': matched_excluded
        })
        logging.info(f"Topic: {topic['title']}")
        logging.info(f"Score: {score}")
        logging.info(f"Matched relevant keywords: {matched_relevant}")
        logging.info(f"Matched excluded keywords: {matched_excluded}")
        logging.info("---")
    
    # Sort topics by score in descending order
    ranked_topics.sort(key=lambda x: x['score'], reverse=True)
    return ranked_topics

def select_topic(topics):
    """Select the highest-ranked topic from the list."""
    if not topics:
        logging.warning("No topics available to select.")
        return None
    
    # Rank the topics
    ranked_topics = rank_and_filter_topics(topics)
    
    if not ranked_topics:
        logging.warning("No topics found after ranking.")
        return None
    
    # Select the highest-ranked topic
    selected = ranked_topics[0]
    logging.info(f"Selected highest ranked topic:")
    logging.info(f"Title: {selected['topic']['title']}")
    logging.info(f"Score: {selected['score']}")
    logging.info(f"Matched relevant keywords: {selected['matched_relevant']}")
    logging.info(f"Matched excluded keywords: {selected['matched_excluded']}")
    
    return selected['topic']['title']

def generate_blog_post(topic):
    """Generate a blog post using OpenAI's ChatGPT model."""
    prompt = (
        f"Write an engaging and informative blog post about '{topic}' that demonstrates expertise in AI solutions "
        "while appealing to small business owners and entrepreneurs. "
        "The post should:\n"
        "1. Start with a compelling title that includes the topic\n"
        "2. Begin with a hook that relates the topic to practical business benefits\n"
        "3. Break down complex AI concepts into simple, actionable insights\n"
        "4. Include real-world applications and examples for small businesses\n"
        "5. Highlight cost-effective ways to implement AI solutions\n"
        "6. Address common concerns and misconceptions\n"
        "7. End with a clear call-to-action for businesses seeking AI consultation\n\n"
        "Format the post using proper HTML tags (<h2> for headings, <p> for paragraphs, <ul> or <ol> for lists). "
        "Make it morally and ethically sound, focusing on sustainable and responsible AI use. "
        "The tone should be professional yet approachable, positioning the author as a trusted AI solutions provider. "
        "Aim for approximately 1000 words."
    )
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()

        # Content filtering (basic example)
        disallowed_keywords = ['disallowed content', 'violence', 'illegal']
        if any(word in content.lower() for word in disallowed_keywords):
            logging.warning("Generated content contains disallowed content.")
            return None

        logging.info("Generated blog post successfully.")
        return content
    except Exception as e:
        logging.error(f"Failed to generate blog post: {e}")
        return None

def save_for_review(title, content):
    """Save the blog post locally for review."""
    filename = f"blog_post_{datetime.now().strftime('%Y%m%d')}.md"
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"# {title}\n\n{content}")
        logging.info(f"Blog post saved for review: {filename}")
        # Open the file in the default text editor
        try:
            if sys.platform.startswith('darwin'):  # macOS
                subprocess.call(('open', filename))
            elif os.name == 'nt':  # Windows
                os.startfile(filename)
            elif os.name == 'posix':  # Linux
                subprocess.call(('xdg-open', filename))
        except Exception as e:
            logging.error(f"Could not open the file automatically: {e}")
        return filename
    except Exception as e:
        logging.error(f"Failed to save or open the blog post: {e}")
        return None

def post_to_wordpress(title, content):
    """Post the blog to WordPress using REST API."""
    try:
        # Set up authentication
        auth = (WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        base_url = f"{WORDPRESS_URL}wp-json/wp/v2"

        # First, get or create tags
        tag_ids = []
        tag_names = ['AI', 'Artificial Intelligence', 'Technology']
        
        for tag_name in tag_names:
            # Check if tag exists
            response = requests.get(
                f"{base_url}/tags",
                params={'search': tag_name},
                auth=auth
            )
            
            if response.status_code == 200:
                tags = response.json()
                if tags:
                    # Tag exists, use its ID
                    tag_ids.append(tags[0]['id'])
                else:
                    # Create new tag
                    response = requests.post(
                        f"{base_url}/tags",
                        json={'name': tag_name},
                        auth=auth
                    )
                    if response.status_code == 201:
                        tag_ids.append(response.json()['id'])

        # Prepare the post data
        post_data = {
            'title': title,
            'content': content,
            'status': 'publish',
            'categories': [1],  # Default category ID
            'tags': tag_ids
        }

        # Make the POST request to create a new post
        response = requests.post(
            f"{base_url}/posts",
            json=post_data,
            auth=auth,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 201:
            post_id = response.json().get('id')
            logging.info(f"Blog post published successfully with ID: {post_id}")
        else:
            logging.error(f"Failed to publish blog post. Status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            
    except Exception as e:
        logging.error(f"Failed to publish blog post: {e}")

def test_wordpress_auth():
    """Test WordPress authentication and API connectivity."""
    try:
        auth = (WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        base_url = f"{WORDPRESS_URL}wp-json/wp/v2"

        # Test authentication by getting users
        response = requests.get(
            f"{base_url}/users/me",
            auth=auth
        )
        
        logging.info(f"Auth Test - Status Code: {response.status_code}")
        logging.info(f"Auth Test - Response: {response.text}")
        
        if response.status_code == 200:
            user_data = response.json()
            logging.info(f"Successfully authenticated as: {user_data.get('name')} (Role: {user_data.get('roles', [])})")
            return True
        else:
            logging.error("Authentication test failed")
            return False
            
    except Exception as e:
        logging.error(f"Auth test failed with error: {e}")
        return False

def main():
    # Test WordPress authentication first
    if not test_wordpress_auth():
        logging.error("WordPress authentication failed. Please check credentials.")
        return

    # Step 1: Get trending AI topics
    topics = get_trending_ai_topics()
    if not topics:
        logging.error("No topics fetched. Exiting.")
        return

    # Step 2: Select a topic
    topic = select_topic(topics)
    if not topic:
        logging.error("No topic selected. Exiting.")
        return

    # Step 3: Generate a blog post
    blog_post = generate_blog_post(topic)
    if not blog_post:
        logging.error("Failed to generate blog post. Exiting.")
        return

    # Step 4: Save for review
    filename = save_for_review(topic, blog_post)
    if not filename:
        logging.error("Failed to save blog post for review. Exiting.")
        return

    # Step 5: Prompt user to review and edit
    input("Please review and edit the blog post. Press Enter when you're ready to publish.")

    # Step 6: Read the edited blog post
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            edited_content = file.read()
    except Exception as e:
        logging.error(f"Failed to read the edited blog post: {e}")
        return

    # Step 7: Post to WordPress
    post_to_wordpress(topic, edited_content)

if __name__ == '__main__':
    main()
