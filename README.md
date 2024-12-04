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

## Customization Note

The current prompt includes a requirement for Sharia compliance as the original author is Muslim. Feel free to modify the prompt in `daily_ai_blog.py` to align with your own values and requirements. The key sections to customize are:

1. Topic selection keywords in `rank_and_filter_topics()`
2. Content generation prompt in `generate_blog_post()`
3. HTML formatting templates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
