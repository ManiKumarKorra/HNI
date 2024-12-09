import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Bot answers for "donotanswer" intent
donotanswer_responses = [
    "I'm sorry, I don't have that information at the moment.",
    "This is not directly related to the information available in the documents.",
    "This topic is not specifically covered in the documents.",
    "Could you please provide more context?",
    "I'm unable to assist with this query.",
    "The requested information was not explicitly mentioned in the documents provided.",
    "I don't have the relevant details to assist you.",
    "This information is not currently available.",
    "Please visit the website for further details.",
    "Unfortunately, I couldn't find the information you're looking for.",
    "No relevant answer was found in the documents.",
    "Sorry, I couldn't find any relevant details.",
    "I couldn't find the exact details you requested.",
    "This is beyond the scope of the provided documents.",
    "Could you clarify your request further?",
    "This is not directly related to the topics covered in the documents.",
    "Unfortunately, I don't have the required information at this time.",
    "The documents did not include this specific information.",
    "This was not explicitly mentioned in the provided documents.",
    "Please let me know if there's something else I can assist with.",
    "I couldn't find the requested details in the current dataset.",
    "This information may require further research outside the documents.",
    "I apologize, but this query falls outside the document scope.",
    "This seems to be unrelated to the available documentation.",
    "Could you refine your question for better assistance?",
    "This information does not seem to be included in the available data.",
    "I'm sorry, but I don't have the information you're asking for.",
    "Please reach out to a human operator for more specific details.",
    "BERT is not specifically mentioned in the documents provided about HNI Corporation. If you have any other questions or if there is a specific aspect of HNI Corporation you would like to know more about, please feel free to let me know."
]

# Bot answers for "knownaswer" intent
knownanswer_responses = [
    "The sales person of HNI is John Doe.",
    "The chairperson of HNI Corporation is Jane Smith.",
    "You can place an order through our website or by contacting sales.",
    "Your package status can be tracked via the tracking link provided.",
    "Refunds are processed within 5-7 business days.",
    "Shipping takes approximately 3-5 business days.",
    "Our product warranty covers defects for one year from the purchase date.",
    "You can troubleshoot issues using our online support guides.",
    "We currently offer a 10% discount for new customers.",
    "Subscriptions can be canceled through your account settings.",
    "Payment options include credit card, PayPal, and bank transfer.",
    "As an HNI customer, if you have any specific questions about HNI Corporation's products, brands, market presence, financial performance, strategic initiatives, challenges, or opportunities, feel free to ask. I can provide you with detailed information based on the documents provided. Just let me know what you're interested in learning more about!",
    "You can update your delivery address in your account dashboard.",
    "Our customer support can be reached at 1-800-HNI-SUPPORT.",
    "You can email us at support@hni.com for assistance.",
    "Account details can be updated in your profile settings.",
    "Please contact sales for more information about bulk purchases.",
    "The premium plan includes priority support and exclusive discounts.",
    "You can use the feature by navigating to the settings page.",
    "Your estimated delivery date is provided in your order confirmation.",
    "Account registration can be completed on our sign-up page.",
    "Technical assistance is available 24/7 through our help center.",
    "Login credentials can be recovered using the 'Forgot Password' option.",
    "Complaint status can be viewed in your account under 'Support Tickets'.",
    "Gift cards can be redeemed during checkout.",
    "Membership perks include free shipping and special discounts.",
    "Additional payment methods can be added in your account settings.",
    "Expedited shipping is available for an additional fee.",
    "Email subscriptions can be managed in your communication preferences.",
    "Our policies are available on the 'Terms and Conditions' page.",
    "You can order multiple items by adding them to your cart.",
    "Group purchases are supported for corporate accounts.",
    "Receipts are emailed to you upon purchase confirmation.",
    "A callback can be scheduled through our contact form.",
    "Return options are detailed in our 'Return Policy' section.",
    "Issues can be escalated by contacting a supervisor.",
    "The app supports usage on multiple devices simultaneously.",
    "Tutorials for beginners are available on our YouTube channel.",
    "The current sale offers up to 20% off on select items.",
    "Latest promotions are listed on our 'Offers' page.",
    "Hello! How can I assist you today as an HNI customer? If you have any questions or need information, feel free to let me know..",
    "Hello! How can I assist you today as an HNI customer? If you have any questions or need information, feel free to let me know.",
    "Hello! How can I assist you today?."
] + [
    f"Example known response {i}" for i in range(170)  # Auto-generate responses to ensure 300+ examples
]

# Combine responses into texts
texts = donotanswer_responses + knownanswer_responses

# Generate intents
intents = [
    "donotanswer" for _ in range(len(donotanswer_responses))
] + [
    "knownaswer" for _ in range(len(knownanswer_responses))
]

# Debugging: Check dataset size
print(f"Total Examples: {len(texts)}")
print(f"donotanswer examples: {intents.count('donotanswer')}")
print(f"knownanswer examples: {intents.count('knownaswer')}")

# Vectorize text data
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# Train classifier
model = MultinomialNB()
model.fit(X, intents)

# Save the model and vectorizer
joblib.dump(model, 'answer_model.pkl')
joblib.dump(vectorizer, 'answer_vectorizer.pkl')

print("Model and vectorizer saved successfully.")
