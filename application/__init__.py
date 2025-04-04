# from flask import Flask, request, render_template, jsonify
# import pickle
# import pandas as pd

# app = Flask(__name__)

# # Load the model when the application starts
# try:
#     model = pickle.load(open('final_model.sav', 'rb'))
# except Exception as e:
#     print(f"Error loading model: {e}")
#     model = None

# @app.route('/', methods=['GET'])
# def home():
#     """Render the home page with input form"""
#     return render_template('index.html')

# # @app.route('/predict', methods=['POST'])
# # def predict():
# #     """Handle prediction requests"""
# #     print("enter")
# #     if request.method == 'POST':
# #         try:
            
# #             # Get news text from form
# #             news_text = request.form.get('news_text', '')
            
# #             if not news_text:
# #                 return render_template('index.html', 
# #                                      error="Please enter some news text")
            
# #             print("andar")
# #             # Make prediction
# #             prediction = model.predict([news_text])
# #             print(f"Prediction:{prediction}")
# #             # Convert prediction to human-readable result
# #             result = "Real News" if prediction[0] == 1 else "Fake News"
# #             print("result")
# #             return render_template('index.html', 
# #                                  news_text=news_text,
# #                                  result=result)
            
# #         except Exception as e:
# #             return render_template('index.html', 
# #                                  error=f"An error occurred: {str(e)}")
# @app.route('/predict', methods=['POST'])
# def predict():
#     """Handle prediction requests"""
#     print("Entered predict route")
#     if request.method == 'POST':
#         try:
#             news_text = request.form.get('news_text', '')
            
#             if not news_text:
#                 return render_template('index.html', 
#                                     error="Please enter some news text")
            
#             print(f"Received text: {news_text[:50]}...")  # Log first 50 chars
            
#             # Make prediction
#             prediction = model.predict([news_text])
#             print(f"Raw prediction: {prediction}")  # Debug output
            
#             result = "Real News" if prediction[0] == 1 else "Fake News"
#             print(f"Formatted result: {result}")
            
#             # Render the result template instead
#             return render_template('result.html',
#                                 news_text=news_text,
#                                 result=result,
#                                 prediction_class='real' if prediction[0] == 1 else 'fake')
            
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return render_template('index.html',
#                                 error=f"An error occurred: {str(e)}")
# # @app.route('/predict', methods=['POST'])
# # def predict():
# #     """Handle prediction requests"""
# #     print("Entered predict route")
# #     if request.method == 'POST':
# #         try:
# #             news_text = request.form.get('news_text', '')
            
# #             if not news_text:
# #                 return render_template('index.html', 
# #                                     error="Please enter some news text")
            
# #             print(f"Received text: {news_text[:50]}...")  # Log first 50 chars
            
# #             # Make prediction
# #             prediction = model.predict([news_text])
# #             print(f"Raw prediction: {prediction}")  # Debug output
            
# #             result = "Real News" if prediction[0] == 1 else "Fake News"
# #             print(f"Formatted result: {result}")
            
# #             return render_template('index.html',
# #                                 news_text=news_text,
# #                                 result=result,
# #                                 prediction_class='real' if prediction[0] == 1 else 'fake')
            
# #         except Exception as e:
# #             print(f"Error: {str(e)}")
# #             return render_template('index.html',
# #                                 error=f"An error occurred: {str(e)}")

# @app.route('/predict_api', methods=['POST'])
# def predict_api():
#     """API endpoint for predictions (returns JSON)"""
#     if request.method == 'POST':
#         try:
#             data = request.get_json()
#             news_text = data.get('text', '')
            
#             if not news_text:
#                 return jsonify({'error': 'No text provided'}), 400
                
#             prediction = model.predict([news_text])
            
#             return jsonify({
#                 'text': news_text,
#                 'prediction': int(prediction[0]),
#                 'result': "Real News" if prediction[0] == 1 else "Fake News"
#             })
            
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session

# Load the model when the application starts
try:
    model = pickle.load(open('final_model.sav', 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/', methods=['GET'])
def home():
    """Render the home page with input form"""
    # Clear any previous results from session
    session.pop('news_text', None)
    session.pop('result', None)
    session.pop('prediction_class', None)
    return render_template('index.html')

@app.route('/result')
def result():
    """Display the result page"""
    # Get results from session
    news_text = session.get('news_text')
    result = session.get('result')
    prediction_class = session.get('prediction_class')
    
    if not all([news_text, result, prediction_class]):
        flash('No analysis results found. Please submit news text first.')
        return redirect(url_for('home'))
    
    return render_template('result.html',
                         news_text=news_text,
                         result=result,
                         prediction_class=prediction_class)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    if request.method == 'POST':
        try:
            news_text = request.form.get('news_text', '').strip()
            
            if not news_text:
                flash('Please enter some news text')
                return redirect(url_for('home'))
            
            # Make prediction
            prediction = model.predict([news_text])
            print(f"Prediction: {prediction}")
            
            # Convert prediction to human-readable result
            result = "Real News" if prediction[0] == 1 else "Fake News"
            prediction_class = 'real' if prediction[0] == 1 else 'fake'
            
            # Store results in session
            session['news_text'] = news_text
            session['result'] = result
            session['prediction_class'] = prediction_class
            
            # Redirect to result page
            return redirect(url_for('result'))
            
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('home'))

@app.route('/predict_api', methods=['POST'])
def predict_api():
    """API endpoint for predictions (returns JSON)"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            news_text = data.get('text', '')
            
            if not news_text:
                return jsonify({'error': 'No text provided'}), 400
                
            prediction = model.predict([news_text])
            
            return jsonify({
                'text': news_text,
                'prediction': int(prediction[0]),
                'result': "Real News" if prediction[0] == 1 else "Fake News"
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/test_model')
def test_model():
    """Test the model with sample inputs"""
    test_cases = [
        "This is clearly fake news designed to mislead people",  # Should be fake
        "The president announced new economic policies today",  # Should be real
        "Aliens landed in New York yesterday",  # Should be fake
        "Scientists discovered a new species in the Amazon"  # Should be real
    ]
    
    results = []
    for text in test_cases:
        prediction = model.predict([text])[0]
        results.append({
            'text': text,
            'prediction': bool(prediction),
            'label': "Real News" if prediction else "Fake News"
        })
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)