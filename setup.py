import keyring
import getpass

def setup_credentials():
    print("Setting up secure credentials for AI Blog Automation")
    print("-" * 50)
    
    # OpenAI API Key
    openai_key = getpass.getpass("Enter your OpenAI API key: ")
    keyring.set_password('openai', 'api_key', openai_key)
    
    # WordPress Application Password
    wp_password = getpass.getpass("Enter your WordPress application password: ")
    keyring.set_password('wordpress', 'application_password', wp_password)
    
    print("\nCredentials stored securely!")
    print("Please remember to configure your .env file with WordPress URL and username.")

if __name__ == "__main__":
    setup_credentials()
