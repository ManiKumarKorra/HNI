
    
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
def check_answer_type(user_message):
    # Load the saved model and vectorizer
    model = joblib.load('answer_model.pkl')
    vectorizer = joblib.load('answer_vectorizer.pkl')
    
    # Transform user input and predict
    X_test = vectorizer.transform([user_message])
    answer_type = model.predict(X_test)[0]
    probabilities = model.predict_proba(X_test).max()
    print(f"{user_message}, {answer_type}, {probabilities:.2f}")
    return answer_type


# message = "I'm sorry, I don't have that information at the moment"
# answer_type = check_answer_type(message)
# print(answer_type)
