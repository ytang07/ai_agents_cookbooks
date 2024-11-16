from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
from pyngrok import ngrok
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# This is your agent response - you can change this variable anytime
agent_response = "Hello! I am your virtual agent. I can say whatever you put in this string variable!"

@app.route("/")
def home():
    """Display the agent response on web page"""
    return agent_response

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Handle incoming calls and read the agent response"""
    # Create Twilio response
    resp = VoiceResponse()
    
    # Have Twilio read the agent response
    resp.say(agent_response, voice='alice')
    
    return str(resp)

if __name__ == '__main__':
    # Start ngrok
    ngrok_tunnel = ngrok.connect(5006)
    print('\nServer Links:')
    print(f'Ngrok URL: {ngrok_tunnel.public_url}')
    print(f'View response at: {ngrok_tunnel.public_url}')
    print(f'Twilio webhook URL: {ngrok_tunnel.public_url}/voice')
    print('\nIMPORTANT: Set your Twilio voice webhook to the URL above')
    print('\nTo test:')
    print('1. Visit the Ngrok URL to see the text')
    print('2. Call your Twilio number to hear it')
    
    # Run Flask app
    app.run(port=5006)