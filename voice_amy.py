from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
from pyngrok import ngrok

app = Flask(__name__)

# This is the message that will be displayed and read
agent_message = "This is your agent message. Change this text to whatever you want Twilio to say!"

@app.route("/")
def home():
    """Display the current message on the webpage"""
    return agent_message

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls by reading the agent message."""
    # Create TwiML response
    resp = VoiceResponse()
    
    # Read the agent message aloud
    resp.say(agent_message, voice='Polly.Amy')
    
    return str(resp)

if __name__ == "__main__":
    # Start ngrok on port 5005
    public_url = ngrok.connect(5005)
    print("\nServer is running!")
    print(f"\nView your message at: {public_url}")
    print(f"Set Twilio webhook to: {public_url}/voice")
    
    # Run Flask app
    app.run(debug=True, port=5005)