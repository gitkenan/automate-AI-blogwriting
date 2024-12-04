# AI Blog Automation System

An automated system for generating and publishing AI-focused blog posts using Python, OpenAI's GPT, and WordPress integration. This system automatically fetches trending AI topics, generates engaging content, and publishes it to your WordPress site.

## Features

- 🤖 Automated content generation using OpenAI's GPT
- 📊 Smart topic selection with keyword ranking system
- 🔒 Secure credential management
- 🌐 WordPress REST API integration
- 📝 HTML-formatted blog posts
- 🎯 Small business and entrepreneurship focus

## Prerequisites

- Python 3.10+
- WordPress site with REST API enabled
- OpenAI API key
- WordPress application password

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd trendingAIblogs
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the setup script to configure credentials:
```bash
python setup.py
```

## Configuration

1. Create a `.env` file with your WordPress URL:
```
WORDPRESS_URL=https://your-site.com/
WORDPRESS_USERNAME=your-username
```

2. Run setup.py to securely store:
- OpenAI API key
- WordPress application password

## Usage

Run the script:
```bash
python daily_ai_blog.py
```

The script will:
1. Fetch trending AI topics
2. Rank them based on relevance
3. Generate a blog post
4. Save it for review
5. Publish to WordPress after approval

## Topic Selection Algorithm

The system uses a sophisticated ranking algorithm that:
- Awards points for relevant keywords (AI tools, developments, innovations)
- Subtracts points for unwanted topics (financial, stock market)
- Ranks all topics by score for optimal selection

## Content Generation

The content generation is optimized for:
- Small business audience
- Practical AI applications
- Cost-effective solutions
- Clear calls-to-action
- Professional yet approachable tone

## Customization Guide

### Search Terms and Topic Selection

The system uses carefully chosen search terms and ranking keywords to find relevant AI news. Here's how to customize them for your needs:

#### Search Queries
In `get_trending_ai_topics()`, modify the search queries based on your focus:
```python
search_queries = [
    'new AI tool release',
    'artificial intelligence development',
    'AI research breakthrough',
    'machine learning innovation',
    'AI technology advancement'
]
```
- These queries are designed to find news about new tools and developments rather than financial news
- Add queries relevant to your industry or specific AI interests
- Keep queries specific enough to get relevant results but broad enough to get sufficient content

#### Keyword Ranking System
In `rank_and_filter_topics()`, customize the keywords that determine article relevance:

```python
relevant_keywords = [
    'tool', 'launch', 'release',      # New product announcements
    'research', 'breakthrough',        # Technical developments
    'innovation', 'platform',          # Industry advancement
    'open source', 'model',           # AI model releases
    'small business'                  # Target audience focus
]

exclude_keywords = [
    'stock', 'market', 'invest',      # Financial news
    'price', 'revenue', 'earnings'    # Market performance
]
```

- Each relevant keyword match adds +1 to the topic's score
- Each exclude keyword match subtracts -0.5 from the score
- Adjust these weights in the code to make the filtering more or less strict

### Content Generation Prompt

The blog generation prompt in `generate_blog_post()` is crucial for producing content that matches your goals:

```python
prompt = (
    "Write an engaging and informative blog post that:"
    "1. Starts with a compelling title\n"
    "2. Relates to practical business benefits\n"
    "3. Breaks down complex AI concepts\n"
    "4. Includes real-world examples\n"
    "5. Highlights cost-effective solutions\n"
)
```

#### Customization Areas:

1. **Audience Focus**: Currently targets small business owners - modify for your target audience
2. **Content Structure**: Adjust the HTML formatting for your WordPress theme
3. **Tone and Style**: Change the professional yet approachable tone as needed
4. **Call to Action**: Customize the ending to match your business goals
5. **Ethical Guidelines**: Currently includes Sharia compliance - modify or remove based on your values

### Example Customizations

For a technical AI blog:
```python
relevant_keywords = ['algorithm', 'architecture', 'framework', 'implementation']
prompt = "Write a technical deep-dive into the AI technology..."
```

For an AI education blog:
```python
relevant_keywords = ['learning', 'tutorial', 'guide', 'introduction']
prompt = "Write a beginner-friendly explanation of the AI concept..."
```

Remember to test your customizations with a few sample runs to ensure the content meets your expectations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
