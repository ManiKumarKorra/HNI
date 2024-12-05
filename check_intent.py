import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
def load_model_and_predict(user_message):
    # Load the saved model and vectorizer
    model = joblib.load('intent_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    
    # Transform user input and predict
    X_test = vectorizer.transform([user_message])
    intent = model.predict(X_test)[0]
    probabilities = model.predict_proba(X_test).max()
    print(f"{user_message}, {intent}, {probabilities:.2f}")
    return intent


# Example usage
# message = "hiiiii"
# intent = load_model_and_predict(message)
