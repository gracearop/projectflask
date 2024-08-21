import os
import re
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
# from . import routes
# Import the API modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../speech_to_text_api')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../text_classifier_api')))
# from app.auth import process_login
from app.words_to_special_char import special_char_map
from word2number import w2n
import speech_to_text_api
import text_classifier_api

# Function to convert words to numbers
def words_to_number(text):
    try:
        return str(w2n.word_to_num(text))
    except ValueError:
        return text  # Return the original text if it can't be converted

# Function to convert words to special characters
def words_to_special_char(text):
    return special_char_map.get(text.lower(), text)

# Function to format the matric number
def format_matric_number(matric_number_text):
    # Convert words to numbers
    numeric_part = words_to_number(matric_number_text)
    # Remove non-alphanumeric characters except letters and numbers
    numeric_part = re.sub(r'[^a-zA-Z0-9]', '', numeric_part)

    # Apply the specific format: 4 digits / 2 chars / 3 chars / 4 digits
    formatted_matric_number = rf"{numeric_part[:4]}\{numeric_part[4:6]}\{numeric_part[6:9]}\{numeric_part[9:]}"
    return formatted_matric_number

# Main function to process transcribed text
def process_transcribed_text(transcribed_text):
    # Split the text into parts based on "with" and "and" while ignoring these words in the result
    parts = re.split(r'\b(?:with|and)\b', transcribed_text, maxsplit=3)

    # Ensure we have at least 4 parts
    if len(parts) < 4:
        raise ValueError("Text could not be split into the required 4 parts.")

    # Process the second part for matric number conversion
    matric_number = format_matric_number(parts[1].strip())

    # Process the third part for password conversion
    password_words = parts[2].strip().split()
    password = ''.join(words_to_special_char(word) for word in password_words)

    # The fourth part is sent directly to the text classifier
    page_name = parts[3].strip()

    return matric_number, password, page_name

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'audio'),  # Add UPLOAD_FOLDER to app.config
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16 MB max upload size
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance and upload folders exist
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        print(f"Instance path: {app.instance_path}")
        print(f"Upload folder path: {app.config['UPLOAD_FOLDER']}")
    except OSError as e:
        print(f"Error creating instance or upload folders: {e}")

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    # Define the upload_audio route within create_app
    @app.route('/upload_audio', methods=['POST'])
    def upload_audio():
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file part'}), 400

        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            try:
                file.save(filepath)
                transcribed_text = speech_to_text_api.transcribe_audio(filepath)
                print(f"Transcribed text: {transcribed_text}")  # Debugging output
            except Exception as e:
                print(f"Error during transcription: {e}")
                return jsonify({'error': 'Error during transcription'}), 500

            try:
                label, probability = text_classifier_api.classify_text(transcribed_text)
                print(f"Classification result: Label={label}, Probability={probability}")  # Debugging output

                # Mapping dictionary
                label_to_route = {
                    '__label__std': 'index',
                    '__label__biodata': 'biodata',
                    '__label__fees': 'fees',
                    '__label__otherfees': 'otherFees',
                    '__label__coursereg': 'courseReg',
                    '__label__results': 'results',
                    '__label__accommodation': 'accommodation',
                    '__label__cop': 'COP',
                    '__label__docs': 'myDocuments',
                    '__label__settings': 'settings',
                }

                # Get the route name
                route_name = label_to_route.get(label, None)
                if not route_name:
                    return jsonify({'error': 'No matching route for label'}), 400

                response = {
                    'transcribed_text': transcribed_text,
                    'intent': label,
                    'probability': probability
                }
                print(f"Response to be returned: {response}")  # Debugging output

                # Generate the URL for redirection
                route_url = url_for(f'main.{route_name}')
                print(f"Generated URL for redirection: {route_url}")  # Debugging output

                # Redirect to the route
                return redirect(route_url)
 
            except Exception as e:
                print(f"Error during classification: {e}")
                return jsonify({'error': 'Error during classification'}), 500

        # Register Blueprints
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import routes
    app.register_blueprint(routes.mb)
    # print(app.url_map) #for returning registered url's
    
    return app

# import os
# import re
# import numpy as np
# import pandas as pd
# from werkzeug.utils import secure_filename
# from flask import Flask, jsonify, render_template, request, redirect, url_for
# from jinja2 import TemplateNotFound
# # from . import routes
# # Import the API modules
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../speech_to_text_api')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../text_classifier_api')))
# from app.auth import process_login
# from app.words_to_special_char import special_char_map
# from word2number import w2n
# import speech_to_text_api
# import text_classifier_api

# def create_app(test_config=None):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#         MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16 MB max upload size
#     )
#     UPLOAD_FOLDER = os.path.join(app.instance_path, 'audio')

#     if test_config is None:
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         app.config.from_mapping(test_config)

#     # ensure the instance and upload folders exist
#     try:
#         os.makedirs(app.instance_path, exist_ok=True)
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#         print(f"Instance path: {app.instance_path}")
#         print(f"Upload folder path: {UPLOAD_FOLDER}")
#     except OSError as e:
#         print(f"Error creating instance or upload folders: {e}")

#     # a simple page that says hello
#     @app.route('/hello')
#     def hello():
#         return 'Hello, World!'
  

# # Function to convert words to numbers
# def words_to_number(text):
#     try:
#         return str(w2n.word_to_num(text))
#     except ValueError:
#         return text  # Return the original text if it can't be converted

# # Function to convert words to special characters
# def words_to_special_char(text):
#     return special_char_map.get(text.lower(), text)

# # Function to format the matric number
# def format_matric_number(matric_number_text):
#     # Convert words to numbers
#     numeric_part = words_to_number(matric_number_text)
#     # Remove non-alphanumeric characters except letters and numbers
#     numeric_part = re.sub(r'[^a-zA-Z0-9]', '', numeric_part)

#     # Apply the specific format: 4 digits / 2 chars / 3 chars / 4 digits
#     formatted_matric_number = rf"{numeric_part[:4]}\{numeric_part[4:6]}\{numeric_part[6:9]}\{numeric_part[9:]}"
#     return formatted_matric_number

# # Main function to process transcribed text
# def process_transcribed_text(transcribed_text):
#     # Split the text into parts based on "with" and "and" while ignoring these words in the result
#     parts = re.split(r'\b(?:with|and)\b', transcribed_text, maxsplit=3)

#     # Ensure we have at least 4 parts
#     if len(parts) < 4:
#         raise ValueError("Text could not be split into the required 4 parts.")

#     # Process the second part for matric number conversion
#     matric_number = format_matric_number(parts[1].strip())

#     # Process the third part for password conversion
#     password_words = parts[2].strip().split()
#     password = ''.join(words_to_special_char(word) for word in password_words)

#     # The fourth part is sent directly to the text classifier
#     page_name = parts[3].strip()

#     return matric_number, password, page_name

# @app.route('/upload_audio', methods=['POST'])
# def upload_audio():
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file part'}), 400

#     file = request.files['audio']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
#         try:
#             file.save(filepath)
#             transcribed_text = speech_to_text_api.transcribe_audio(filepath)
#             print(f"Transcribed text: {transcribed_text}")  # Debugging output
#         except Exception as e:
#             print(f"Error during transcription: {e}")
#             return jsonify({'error': 'Error during transcription'}), 500

#         try:
#             if transcribed_text.lower().startswith("login"):
#                 # Process the transcribed text to extract matric number, password, and page name
#                 try:
#                     matric_number, password, page_name = process_transcribed_text(transcribed_text)
#                 except ValueError as e:
#                     return jsonify({'error': str(e)}), 400

#                 # Map page name to route
#                 label_to_route = {
#                     '__label__std': 'index',
#                     '__label__biodata': 'biodata',
#                     '__label__fees': 'fees',
#                     '__label__otherfees': 'otherFees',
#                     '__label__coursereg': 'courseReg',
#                     '__label__results': 'results',
#                     '__label__accommodation': 'accommodation',
#                     '__label__cop': 'COP',
#                     '__label__docs': 'myDocuments',
#                     '__label__settings': 'settings',
#                 }

#                 route_name = label_to_route.get(page_name, 'index')  # Default to 'index' if page not found

#                 # Perform login by calling the login function directly or sending a request
#                 login_successful = process_login(matric_number, password)
#                 if login_successful:
#                     return redirect(url_for(f'main.{route_name}'))
#                 else:
#                     return jsonify({'error': 'Login failed. Incorrect matric number or password.'}), 400

#             else:
#                 return jsonify({'error': 'Login command is incomplete.'}), 400
#         except Exception as e:
#             print(f"Error during processing: {e}")
#             return jsonify({'error': 'An error occurred during processing'}), 500

#         try:
#             label, probability = text_classifier_api.classify_text(transcribed_text)
#             print(f"Classification result: Label={label}, Probability={probability}")  # Debugging output

#             # Mapping dictionary
#             label_to_route = {
#                 '__label__std': 'index',
#                 '__label__biodata': 'biodata',
#                 '__label__fees': 'fees',
#                 '__label__otherfees': 'otherFees',
#                 '__label__coursereg': 'courseReg',
#                 '__label__results': 'results',
#                 '__label__accommodation': 'accommodation',
#                 '__label__cop': 'COP',
#                 '__label__docs': 'myDocuments',
#                 '__label__settings': 'settings',
#             }

#             # Get the route name
#             route_name = label_to_route.get(label, None)
#             if not route_name:
#                 return jsonify({'error': 'No matching route for label'}), 400

#             response = {
#                 'transcribed_text': transcribed_text,
#                 'intent': label,
#                 'probability': probability
#             }
#             print(f"Response to be returned: {response}")  # Debugging output

#             # Generate the URL for redirection
#             route_url = url_for(f'main.{route_name}')
#             print(f"Generated URL for redirection: {route_url}")  # Debugging output

#             # Redirect to the route
#             return redirect(route_url)

#         except Exception as e:
#             print(f"Error during classification: {e}")
#             return jsonify({'error': 'Error during classification'}), 500
            
#     # Register Blueprints
#     from . import db
#     db.init_app(app)

#     from . import auth
#     app.register_blueprint(auth.bp)

#     from . import routes
#     app.register_blueprint(routes.mb)

#     return app