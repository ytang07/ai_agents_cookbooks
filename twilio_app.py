from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Your Twilio credentials
TWILIO_ACCOUNT_SID = environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = environ["TWILIO_AUTH_TOKEN"]

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/answer", methods=['POST'])
def answer_call():
    """Handle incoming calls and generate TwiML response"""
    # Create TwiML response object
    response = VoiceResponse()
    
    # Get the spoken text from the call
    spoken_text = request.values.get('SpeechResult', '')
    
    if not spoken_text:
        # If no speech detected, prompt the user to speak
        gather = response.gather(
            input='speech',
            action='/process_speech',
            timeout=3,
            language='en-US'
        )
        gather.say('Please ask your question about Rapamycin.')
    else:
        # Forward to processing endpoint
        response.redirect('/process_speech')
    
    return str(response)

@app.route("/process_speech", methods=['POST'])
def process_speech():
    """Process the speech and get response from agent"""
    # Create TwiML response object
    response = VoiceResponse()
    
    # Get the spoken text
    spoken_text = request.values.get('SpeechResult', '')
    
    try:
        # Get response from your agent
        agent_response = agent.chat(spoken_text)
        
        # Convert agent response to string and clean up if needed
        tts_text = str(agent_response)
        
        # Have Twilio speak the response
        response.say(tts_text, voice='alice')
        
    except Exception as e:
        # Handle any errors
        response.say("I'm sorry, there was an error processing your request.")
        print(f"Error: {str(e)}")
    
    return str(response)

@app.route("/call", methods=['POST'])
def make_call():
    """Initiate a call to a specified number"""
    to_number = request.form['to']
    
    try:
        call = client.calls.create(
            to=to_number,
            from_='your_twilio_phone_number',
            url=request.url_root + 'answer'
        )
        return f"Call initiated with SID: {call.sid}"
    except Exception as e:
        return f"Error making call: {str(e)}"

if __name__ == "__main__":
    try:
        # Try different ports if 5000 is in use
        port = 5000
        while port < 5010:  # Try up to port 5009
            try:
                app.run(debug=True, port=port)
                break
            except OSError:
                port += 1
        if port == 5010:
            print("Could not find an available port")
    except Exception as e:
        print(f"Error starting the server: {str(e)}")