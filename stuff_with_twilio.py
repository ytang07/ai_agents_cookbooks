import logging
import os

from dotenv import load_dotenv
from flask import Flask, request
from openai import OpenAI

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask_socketio import SocketIO, emit

from arize import process_call

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Twilio client
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

socketio = SocketIO(app)


@app.route("/", methods=["GET"])
def home():
    """Test route to verify server is running"""
    return "Twilio Flask app is running!"


@app.route("/answer", methods=["POST"])
def answer_call():
    """Handle incoming phone calls"""
    logger.info("Received incoming call")
    response = VoiceResponse()

    # Add a greeting and wait for the caller to speak
    gather = Gather(
        input="speech", action="/process_speech", timeout=3, speech_timeout="auto"
    )
    gather.say("Nine-one-one what is your emergency.")
    response.append(gather)

    # If the user doesn't say anything, try again
    response.redirect("/answer")

    return str(response)


# @socketio.on("send_message")
# def handle_source(json_data):
#     text = json_data["message"].encode("ascii", "ignore")
#     print("Server Says: " + text)


# Route for a webpage that displays call results
@app.route("/call_results", methods=["GET"])
def call_results():
    """Display the results of the call processing"""
    # Get ui.html from the current directory
    with open("ui.html", "r") as f:
        return f.read()


# Debug route to test the websocket
@app.route("/test_socket", methods=["GET"])
def test_socket():
    """Test the websocket connection"""
    socketio.emit(
        "send_message",
        {
            "priority": "GREEN",
            "department": "POLICEDEPT",
            "summary": "This is a test message",
            "confidence": 95,
        },
    )
    return {
        "priority": "GREEN",
        "department": "POLICEDEPT",
        "summary": "This is a test message",
        "confidence": 95,
    }


@app.route("/process_speech", methods=["POST"])
def process_speech():
    """Process the speech input from the caller"""
    logger.info("Processing speech from call")
    # Get the speech input
    speech_result = request.values.get("SpeechResult", "")
    logger.info(f"Received speech: {speech_result}")

    if speech_result:
        # Process the text using the process call function
        result = process_call(speech_result)
        logger.info(f"Processing result: {result}")

        # Create a response
        response = VoiceResponse()
        response.say(f"I heard: {speech_result}")
        socketio.emit("send_message", result)
        response.say(f"Processing result: {result}")
    else:
        # If no speech was detected
        logger.warning("No speech detected")
        response = VoiceResponse()
        response.say("I'm sorry, I didn't catch that. Please try again.")
        response.redirect("/answer")

    return str(response)


if __name__ == "__main__":
    # Run the Flask app on port 5000
    logger.info("Starting Flask application...")
    app.run(debug=True, port=5000)
    socketio.run(app, debug=True)