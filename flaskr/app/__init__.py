import os
from urllib import response
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import requests  # Add this for sending audio to Colab
import numpy as np
import tensorflow as tf
import pandas as pd

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16 MB max upload size
    )
    UPLOAD_FOLDER = os.path.join(app.instance_path, 'audio')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance and upload folders exist
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        print(f"Instance path: {app.instance_path}")
        print(f"Upload folder path: {UPLOAD_FOLDER}")
    except OSError as e:
        print(f"Error creating instance or upload folders: {e}")

 
    # Define the URL of your Colab server
    COLAB_URL = "http://a8a7-34-83-1-211.ngrok-free.app/process_audio"  # Updated endpoint

    # Define a function to send audio to the Colab server
    def send_audio_to_colab(filepath):
        try:
            with open(filepath, 'rb') as file:
                files = {'audio_file': file}
                response = requests.post(COLAB_URL, files=files)
                response.raise_for_status()  # Raise an error for HTTP errors
                return response.json()  # Ensure this returns a dictionary
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return {}  # Return an empty dict on error
        except ValueError as e:
            print(f"JSON parsing error: {e}")
            return {}  # Return an empty dict on JSON parsing error

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

   
    @app.route('/upload_audio', methods=['POST'])
    def upload_audio():
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file part'}), 400

        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            try:
                file.save(filepath)
                # Send the file to Colab for processing
                result = send_audio_to_colab(filepath)
                predicted_intent = result.get('predicted_intent', 'No intent found')
                return jsonify({'message': 'File processed successfully', 'predicted_intent': predicted_intent}), 200
            except Exception as e:
                print(f"Error saving file: {e}")
                return jsonify({'error': 'Error saving file'}), 500
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import routes
    app.register_blueprint(routes.mb)
    # app.register_blueprint(routes.mb, url_prefix='/students')

    return app



# import os
# from flask import Flask, jsonify, render_template, request, redirect, url_for
# # from jinja2 import TemplateNotFound
# # import tensorflow as tf
# # from tensorflow.keras.preprocessing.sequence import pad_sequences
# # import numpy as np
# # import pandas as pd
# # from flaskr import routes

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#         MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16 MB max upload size
#     )
#     UPLOAD_FOLDER = os.path.join(app.instance_path, 'audio')

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
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
    
#     # endpoint to handle audio upload
#     @app.route('/upload_audio', methods=['POST'])
#     def upload_audio():
#         if 'audio' not in request.files:
#             return jsonify({'error': 'No audio file part'}), 400

#         file = request.files['audio']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         if file:
#             filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#             try:
#                 file.save(filepath)
#                 return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200
#             except Exception as e:
#                 print(f"Error saving file: {e}")
#                 return jsonify({'error': 'Error saving file'}), 500
            

            
#     from . import db
#     db.init_app(app)

#     from . import auth
#     app.register_blueprint(auth.bp)

#     from . import routes
#     app.register_blueprint(routes.mb)
#     # app.register_blueprint(routes.mb, url_prefix='/students')



#     return app
