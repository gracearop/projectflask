        # else:
            #     # Handle other intents using the classifier
            #     label, probability = text_classifier_api.classify_text(transcribed_text)
            #     print(f"Classification result: Label={label}, Probability={probability}")
            # try:
            #     # Check if the command starts with "login"
            #     if transcribed_text.lower().startswith("login"):
            #         login_info = process_login(transcribed_text)
            #         if login_info['matric_number'] and login_info['password']:
            #             # Simulate filling out the login form
            #             # You can customize this section based on how you want to authenticate users
            #             return render_template('login.html', 
            #                                    matric_number=login_info['matric_number'], 
            #                                    student_password=login_info['password'])
            #         elif login_info['page']:
            #             return redirect(url_for(f'main.{login_info["page"]}'))
            #         else:
            #             return jsonify({'error': 'Login details missing'}), 400
            #     else:
            #         label, probability = text_classifier_api.classify_text(transcribed_text)
            #         print(f"Classification result: Label={label}, Probability={probability}")

# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from flask import Flask, jsonify, request
# from werkzeug.utils import secure_filename
# from faster_whisper import WhisperModel
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tokenizers import BertWordPieceTokenizer
# from spellchecker import SpellChecker  # Import for spelling correction

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

#     # Initialize Whisper model
#     whisper_model = WhisperModel("large-v3", device="cpu", compute_type="float32")

#     # Load and prepare the intent classifier
#     csv_path = os.path.join(os.path.dirname(__file__), 'intentdata.csv')
#     print(f"Looking for intentdata.csv at: {csv_path}")
#     data = pd.read_csv(csv_path)
#     data.columns = data.columns.str.strip()
#     intents = data['Intent'].tolist()
#     text_input = data['Text'].tolist()

#     def clean(line):
#         cleaned_line = ''.join([char if char.isalpha() else ' ' for char in line])
#         return ' '.join(cleaned_line.split())

#     text_input = [clean(text) for text in text_input]
#     tokenizer = BertWordPieceTokenizer(lowercase=True, unk_token='<unk>')
#     tokenizer.train_from_iterator(text_input, vocab_size=30522)
#     subword_sequences = [tokenizer.encode(text).ids for text in text_input]
#     padded_sequences = pad_sequences(subword_sequences, padding='pre')

#     intent_to_index = {intent: idx for idx, intent in enumerate(set(intents))}
#     categorical_target = [intent_to_index[intent] for intent in intents]
#     num_classes = len(intent_to_index)
#     index_to_intent = {index: intent for intent, index in intent_to_index.items()}
#     categorical_vec = tf.keras.utils.to_categorical(categorical_target, num_classes=num_classes)

#     embed_dim = 300
#     lstm_num = 50
#     output_dim = categorical_vec.shape[1]
#     model = tf.keras.models.Sequential([
#         tf.keras.layers.Embedding(input_dim=30522 + 1, output_dim=embed_dim),
#         tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_num, dropout=0.1)),
#         tf.keras.layers.Dense(lstm_num, activation='relu'),
#         tf.keras.layers.Dropout(0.4),
#         tf.keras.layers.Dense(output_dim, activation='softmax')
#     ])
#     optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
#     model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
#     model.fit(padded_sequences, categorical_vec, epochs=100, verbose=0)

#     def correct_spelling(text):
#         spell = SpellChecker()
#         words = text.split()
#         corrected_words = [spell.correction(word) if word in spell.unknown([word]) else word for word in words]
#         return ' '.join(corrected_words)

#     def classify_intent(sentence):
#         sentence = correct_spelling(sentence)
#         tokens = tokenizer.encode(sentence).ids
#         tokens = tf.expand_dims(tokens, 0)
#         pred = model(tokens)
#         pred_class = np.argmax(pred.numpy(), axis=1)
#         return index_to_intent[pred_class[0]]

#     @app.route('/upload_audio', methods=['POST'])
#     def upload_audio():
#         if 'audio' not in request.files:
#             return jsonify({'error': 'No audio file part'}), 400

#         file = request.files['audio']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         if file:
#             filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
#             try:
#                 file.save(filepath)
#                 # Transcribe the audio
#                 segments, info = whisper_model.transcribe(filepath, beam_size=5)
#                 transcribed_text = " ".join([segment.text for segment in segments])
                
#                 # Predict the intent
#                 predicted_intent = classify_intent(transcribed_text)
                
#                 # Debugging output
#                 print(f"Transcribed text: {transcribed_text}")
#                 print(f"Predicted intent: {predicted_intent}")
                
#                 return jsonify({'message': 'File processed successfully', 'predicted_intent': predicted_intent}), 200
#             except Exception as e:
#                 print(f"Error saving file: {e}")
#                 return jsonify({'error': 'Error saving file'}), 500

#     # Register Blueprints
#     from . import db
#     db.init_app(app)

#     from . import auth
#     app.register_blueprint(auth.bp)

#     from . import routes
#     app.register_blueprint(routes.mb)

#     return app


# working document!!!

# import os
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
    # commentted parts
    # # endpoint to handle audio upload
    # @app.route('/upload_audio', methods=['POST'])
    # def upload_audio():
    #     if 'audio' not in request.files:
    #         return jsonify({'error': 'No audio file part'}), 400

    #     file = request.files['audio']
    #     if file.filename == '':
    #         return jsonify({'error': 'No selected file'}), 400

    #     if file:
    #         filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    #         try:
    #             file.save(filepath)
    #             return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200
    #         except Exception as e:
    #             print(f"Error saving file: {e}")
    #             return jsonify({'error': 'Error saving file'}), 500
            
    # @app.route('/upload_audio', methods=['POST'])
    # def upload_audio():
    #     if 'audio' not in request.files:
    #         return jsonify({'error': 'No audio file part'}), 400

    #     file = request.files['audio']
    #     if file.filename == '':
    #         return jsonify({'error': 'No selected file'}), 400

    #     if file:
    #         filename = secure_filename(file.filename)
    #         filepath = os.path.join(UPLOAD_FOLDER, filename)
            
    #         try:
    #             # Save the audio file temporarily for transcription
    #             file.save(filepath)
                
    #             # Transcribe the audio
    #             transcription = transcribe_audio(filepath)
    #             if not transcription:
    #                 return jsonify({'error': 'Transcription failed'}), 500
                
    #             # Classify the transcribed text
    #             label, probability = classify_text(transcription)
                
    #             # If classification is successful, save the file permanently
    #             if label:
    #                 return jsonify({
    #                     'message': 'File uploaded and processed successfully',
    #                     'filepath': filepath,
    #                     'transcription': transcription,
    #                     'intent': label,
    #                     'probability': probability
    #                 }), 200
    #             else:
    #                 os.remove(filepath)  # Remove the file if classification fails
    #                 return jsonify({'error': 'Classification failed'}), 500

    #         except Exception as e:
    #             print(f"Error processing file: {e}")
    #             return jsonify({'error': 'Error processing file'}), 500
    # commentted parts
    # @app.route('/upload_audio', methods=['POST'])
    # def upload_audio():
    #     if 'audio' not in request.files:
    #         return jsonify({'error': 'No audio file part'}), 400

    #     file = request.files['audio']
    #     if file.filename == '':
    #         return jsonify({'error': 'No selected file'}), 400

    #     if file:
    #         filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    #         try:
    #             file.save(filepath)
    #             transcribed_text = speech_to_text_api.transcribe_audio(filepath)
    #             print(f"Transcribed text: {transcribed_text}")  # Debugging output
    #         except Exception as e:
    #                 print(f"Error during transcription: {e}")
    #                 return jsonify({'error': 'Error during transcription'}), 500
    #             # Step 1: Transcribe the audio to text
    #             # transcribed_text = speech_to_text_api.transcribe_audio(filepath)
                
    #         try:
    #             label, probability = text_classifier_api.classify_text(transcribed_text)
    #             print(f"Classification result: Label={label}, Probability={probability}")  # Debugging output
    #             response = {
    #                 'transcribed_text': transcribed_text,
    #                 'intent': label,
    #                 'probability': probability
    #             }
    #             print(f"Response to be returned: {response}")  # Debugging output
    #             return jsonify(response), 200
    #         except Exception as e:
    #             print(f"Error during classification: {e}")
    #             return jsonify({'error': 'Error during classification'}), 500
    #             # Step 2: Classify the transcribed text
    #             # label, probability = text_classifier_api.classify_text(transcribed_text)
                
    #             # Step 3: Respond with the intent and save the audio
              
    #             # return jsonify(response), 200
    #         # except Exception as e:
    #             # print(f"Error processing file: {e}")
    #             # return jsonify({'error': 'Error processing file'}), 500

    # # Register Blueprints
    # from . import db
    # db.init_app(app)

    # from . import auth
    # app.register_blueprint(auth.bp)

    # from . import routes
    # app.register_blueprint(routes.mb)

    # return app

# segments, info = model.transcribe("MLKDream_64kb.mp3", beam_size=5, language="en", condition_on_previous_text=False)

# for segment in segments:
#     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            # try:
            #     if transcribed_text.lower().startswith("login"):
            #         # Process the transcribed text to extract matric number, password, and page name
            #         try:
            #             matric_number, password, page_name = process_transcribed_text(transcribed_text)
            #         except ValueError as e:
            #             return jsonify({'error': str(e)}), 400

            #         # Map page name to route
            #         label_to_route = {
            #             '__label__std': 'index',
            #             '__label__biodata': 'biodata',
            #             '__label__fees': 'fees',
            #             '__label__otherfees': 'otherFees',
            #             '__label__coursereg': 'courseReg',
            #             '__label__results': 'results',
            #             '__label__accommodation': 'accommodation',
            #             '__label__cop': 'COP',
            #             '__label__docs': 'myDocuments',
            #             '__label__settings': 'settings',
            #         }

            #         route_name = label_to_route.get(page_name, 'index')  # Default to 'index' if page not found

            #         # Perform login by calling the login function directly or sending a request
            #         login_successful = process_login(matric_number, password)
            #         if login_successful:
            #             return redirect(url_for(f'main.{route_name}'))
            #         else:
            #             return jsonify({'error': 'Login failed. Incorrect matric number or password.'}), 400

            #     else:
            #         return jsonify({'error': 'Login command is incomplete.'}), 400
            # except Exception as e:
            #     print(f"Error during processing: {e}")
            #     return jsonify({'error': 'An error occurred during processing'}), 500
