from pyngrok import ngrok
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)

try:
    # Start ngrok on port 5005
    public_url = ngrok.connect(5005)
    
    # Display connection info
    print(f"\nNgrok is running!")
    print(f"Public URL: {public_url}")
    print(f"Local port: 5005")
    
    # Get all active tunnels (optional, for verification)
    tunnels = ngrok.get_tunnels()
    print("\nActive tunnels:")
    for tunnel in tunnels:
        print(f"- {tunnel.public_url} -> {tunnel.config['addr']}")
        
except Exception as e:
    print(f"Error starting ngrok: {str(e)}")
    print("\nTroubleshooting tips:")
    print("1. Verify NGROK_AUTH_TOKEN is in your .env file")
    print("2. Check if port 5005 is available")
    print("3. Ensure ngrok is authenticated")

# To stop ngrok when you're done, run this:
ngrok.disconnect(public_url)