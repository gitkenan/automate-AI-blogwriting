# AI Blog Post Automation

This project automates the process of generating and publishing daily AI blog posts using OpenAI's ChatGPT and WordPress integration.

## Features

- Fetches trending AI topics using Google News
- Generates high-quality blog posts using ChatGPT
- Allows for manual review and editing before publishing
- Securely manages API keys and credentials
- Publishes directly to WordPress
- Includes comprehensive logging

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- WordPress site with XML-RPC enabled
- WordPress application password

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd trendingAIblogs
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your WordPress URL and username.

5. Run the setup script to configure your credentials:
   ```bash
   python setup.py
   ```

## Usage

Run the script:
```bash
python daily_ai_blog.py
```

The script will:
1. Fetch trending AI topics
2. Generate a blog post
3. Save it for your review
4. Open it in your default text editor
5. Wait for your confirmation
6. Publish to WordPress

## Automation

### Windows
Use Task Scheduler to run the script daily:
1. Open Task Scheduler
2. Create a new task
3. Set the action to run your Python interpreter with the script
4. Set your preferred schedule

### Linux/macOS
Add a cron job:
```bash
crontab -e
```
Add:
```
0 9 * * * /path/to/venv/bin/python /path/to/daily_ai_blog.py
```

## Logging

Logs are saved to `daily_ai_blog.log`. Check this file for execution details and any errors.

## Security

- API keys and passwords are stored securely using the system's credential manager
- Sensitive data is never stored in plain text
- Basic content filtering is implemented

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
