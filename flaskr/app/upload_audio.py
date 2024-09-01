# flaskr/app/upload_audio.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../speech_to_text_api')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../text_classifier_api')))
from flask import request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

import speech_to_text_api
import text_classifier_api

def upload_audio(app):
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
