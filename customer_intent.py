from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training data
texts = [
    # connect_with_human examples
    "I want to talk to a human",
    "Connect me with a real person",
    "Can I speak with a human?",
    "I need to talk to someone",
    "Get me a human agent",
    "Can you connect me with a person?",
    "I need help from an operator",
    "Let me talk to a human being",
    "Please connect me with a human",
    "I want to speak to an agent",
    "Help me talk to a live agent",
    "Transfer me to a human",
    "Can I talk to an operator?",
    "Is it possible to speak to a person?",
    "Can you get me an agent?",
    "I want to chat with a live person",
    "Can you transfer me to someone?",
    "I need to speak with someone",
    "Connect me to customer service",
    "Can you get me a real human?",
    "Put me in touch with an agent",
    "Let me talk to a customer representative",
    "I don't want a bot, get me a human",
    "Can you transfer me to a live operator?",
    "I need a human to help me",
    "I want to speak with a real agent",
    "Connect me with operator",
    "Get me to someone who can help",
    "Please transfer me to a human being",
    "I need real-time help from a person",
    
    # other examples
    "What is your pricing?",
    "Can you help me reset my password?",
    "How do I change my email address?",
    "What are your operating hours?",
    "Tell me more about your services",
    "What is the return policy?",
    "How do I place an order?",
    "Where is my package?",
    "Can I get a refund?",
    "How long does shipping take?",
    "What is the warranty on this product?",
    "I need help troubleshooting my issue",
    "Is there a discount available?",
    "How do I cancel my subscription?",
    "What are your payment options?",
    "Do you offer international shipping?",
    "Can I change my delivery address?",
    "Is there a phone number I can call?",
    "What is your support email?",
    "How do I update my account details?",
    "Can I speak to sales?",
    "What are the benefits of your premium plan?",
    "How do I use this feature?",
    "What is the estimated delivery date?",
    "hi",
    "hello",
    "whats up"
]

intents = [
    # connect_with_human labels
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human",
    
    # other labels
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other", "other" , "other", "other", "other"
]

# Vectorize text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Train classifier
model = MultinomialNB()
model.fit(X, intents)

# Predict intent
def identify_intent(user_message):
    X_test = vectorizer.transform([user_message])
    return model.predict(X_test)[0]

# Example usage
# message = "connect we with agent"
# intent = identify_intent(message)
# print(f"Identified Intent: {intent}")
