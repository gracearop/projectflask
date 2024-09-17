import os
import re
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../speech_to_text_api')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../text_classifier_api')))
# from app.auth import process_login
# from app.words_to_special_char import special_char_map
from word2number import w2n
import speech_to_text_api
import text_classifier_api


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

                route_name = label_to_route.get(label, None)
                if not route_name:
                    return jsonify({'error': 'No matching route for label'}), 400

                response = {
                    'transcribaed_text': transcribed_text,
                    'intent': label,
                    'probability': probability
                }
                print(f"Response to be returned: {response}")  # Debugging output

                route_url = url_for(f'main.{route_name}')
                print(f"Generated URL for redirection: {route_url}")  # Debugging output

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

# Expose upload_audio function at the module level
# __all__ = ['upload_audio', 'create_app']