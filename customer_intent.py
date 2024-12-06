# import joblib
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB

# # Training data with expanded examples
# texts = [
#     # connect_with_human examples (30 examples)
#     "I want to talk to a human", "Connect me with a real person", 
#     "Can I speak with a human?", "I need to talk to someone",
#     "Get me a human agent", "Can you connect me with a person?",
#     "I need help from an operator", "Let me talk to a human being",
#     "Please connect me with a human", "I want to speak to an agent",
#     "Help me talk to a live agent", "Transfer me to a human",
#     "Can I talk to an operator?", "Is it possible to speak to a person?",
#     "Can you get me an agent?", "I want to chat with a live person",
#     "Can you transfer me to someone?", "I need to speak with someone",
#     "Connect me to customer service", "Can you get me a real human?",
#     "Put me in touch with an agent", "Let me talk to a customer representative",
#     "I don't want a bot, get me a human", "Can you transfer me to a live operator?",
#     "I need a human to help me", "I want to speak with a real agent",
#     "Connect me with operator", "Get me to someone who can help",
#     "Please transfer me to a human being", "I need real-time help from a person",
    
#     # other examples (270+ examples)
#     "who is the person",
#     "who is the sales person of hni",
#     "who is the chair person of hni",
#     "How do I place an order?", "Where is my package?",
#     "Can I get a refund?", "How long does shipping take?",
#     "What is the warranty on this product?", "I need help troubleshooting my issue",
#     "Is there a discount available?", "How do I cancel my subscription?",
#     "What are your payment options?", "Do you offer international shipping?",
#     "Can I change my delivery address?", "Is there a phone number I can call?",
#     "What is your support email?", "How do I update my account details?",
#     "Can I speak to sales?", "What are the benefits of your premium plan?",
#     "How do I use this feature?", "What is the estimated delivery date?",
#     "How do I register my account?", "Can I get technical assistance?",
#     "Where do I log in?", "What is the status of my complaint?",
#     "what are the brands with hni?",
#     "i need a fireplace with minimal carbon footprint",
#     "How do I unsubscribe from emails?", "Where can I find your policies?",
#     "i need a fireplace with minimal carbon footprint within hni",
#     "Where is my receipt?", "Can I schedule a callback?",
#     "i have spondilitis can you recommend me a good work station chair",
#     "Can I use the app on multiple devices?", "What do I do if I forgot my username?",
#     "Are there tutorials for beginners?", "What is the current sale offer?",
#     "i need cervical support work station chairs",
#     "How do I delete my account?", "What security measures are in place?",
#     "Can I change my subscription tier?", "Is there a student discount available?",
#     "i would like to customize hon's ignition model",
#     "Where can I find the terms and conditions?", "Can I cancel my order after placing it?",
#     "What is the best way to contact support?", "How can I subscribe to your newsletter?",
#     "with in hon product range can i customize or configure products?",
#     "Can I update my payment preferences online?", "How can I view my order history?",
#     "Can I get an itemized invoice?", "What options are available for bulk purchases?",
#     "What is your contact number?", "Do you have an app?",
#     "Can I talk to technical support?", "Is your service 24/7?",
#     "How do I apply for a return?", "Can I get product recommendations?",
#     "Where can I find reviews?", "What is your refund timeline?",
#     "Do you offer COD?", "Is there a mobile app available?",
#     "Can I update my profile details?", "What are your privacy policies?",
#     "Do you offer virtual consultations?", "Can I reschedule my appointment?",
#     "Where do I find user guides?", "What happens if my order is delayed?",
#     "Are there any ongoing discounts?", "How do I apply a coupon?",
#     "",
#     # Add more examples until 270+ examples for "other"
# ] + [
#     f"Other example query {i}" for i in range(170)  # Auto-generate to ensure 300+ examples
# ]

# # Generate intents
# intents = [
#     "connect_with_human" for _ in range(30)
# ] + [
#     "other" for _ in range(len(texts) - 30)
# ]

# # Debugging: Check dataset size
# print(f"Total Examples: {len(texts)}")
# print(f"connect_with_human examples: {intents.count('connect_with_human')}")
# print(f"other examples: {intents.count('other')}")


# # Vectorize text data
# vectorizer = CountVectorizer(stop_words='english')
# X = vectorizer.fit_transform(texts)

# # Train classifier
# model = MultinomialNB()
# model.fit(X, intents)

# # Save the model and vectorizer
# joblib.dump(model, 'intent_model.pkl')
# joblib.dump(vectorizer, 'vectorizer.pkl')

# print(f"Total Examples: {len(texts)}")
# print("Model and vectorizer saved successfully.")
