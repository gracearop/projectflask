# from flask import Flask, request, jsonify
# import sqlite3
# from faster_whisper import WhisperAPI  # Assuming this is the library you're using
# from nltk import classify_intent  # Assuming this is a custom intent classification function

# app = Flask(__name__)
# DATABASE = 'path/to/your/database.db'

# # Function to connect to the database
# def get_db():
#     conn = sqlite3.connect(DATABASE)
#     return conn

# # Function to insert voice command details into the database
# def insert_voice_command(voice_command, target_url, command_description):
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO voice_commands (voice_command, target_url, command_description)
#         VALUES (?, ?, ?)
#     ''', (voice_command, target_url, command_description))
#     conn.commit()
#     conn.close()

# # Route to process voice command
# @app.route('/process_voice_command', methods=['POST'])
# def process_voice_command():
#     audio_data = request.files['audio']  # Assuming audio data is sent as a file
#     whisper_api = WhisperAPI()
#     voice_command_text = whisper_api.speech_to_text(audio_data)  # Convert speech to text

#     intent = classify_intent(voice_command_text)  # Classify the intent
#     target_url = intent['target_url']
#     command_description = intent['description']

#     # Insert the command details into the database
#     insert_voice_command(voice_command_text, target_url, command_description)

#     return jsonify({
#         'status': 'success',
#         'voice_command': voice_command_text,
#         'target_url': target_url,
#         'command_description': command_description
#     })

# if __name__ == '__main__':
#     app.run(debug=True)



    # @app.route('/predict', methods=['POST'])
    # def predict():
    #     user_input = request.form['user_input']
    #     predicted_intent = response(user_input)
        
    #     # Debug print
    #     print(f"User input: {user_input}")
    #     print(f"Predicted intent: {predicted_intent}")

    #     # Ensure the intent matches an HTML file name
    #     html_file = f"{predicted_intent}.html"
    #         # Debug print
    #     print(f"HTML file to render: {html_file}")
    #     try:
    #         return render_template(html_file)
    #     except TemplateNotFound:
    #         return render_template('error.html', message="Intent not recognized or HTML file not found")

     