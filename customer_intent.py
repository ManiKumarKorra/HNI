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
    # Additional connect_with_human examples
    "Can I please talk to someone?",
    "Transfer me to a person, please",
    "I can't get help from the bot, connect me to a human",
    "Talk to me with a real agent",
    "Can I have a live conversation with a person?",
    "Let me connect to a human agent",
    "I want immediate help from a human",
    "Direct me to someone who can assist",
    "I need to speak to a human support agent",
    "Please, no bots, I need a human",
    "Who can I talk to for real help?",
    "Human support, please",
    "Can someone live talk to me?",
    "I need live help, not automated replies",
    "Is it possible to chat with a human now?",
    # Other examples
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
    "How do I register my account?",
    "Can I get technical assistance?",
    "Where do I log in?",
    "What is the status of my complaint?",
    "How do I redeem a gift card?",
    "What are the perks of membership?",
    "Can I add another payment method?",
    "Do you offer expedited shipping?",
    "How do I unsubscribe from emails?",
    "Where can I find your policies?",
    "Can I order multiple items?",
    "Do you support group purchases?",
    "Where is my receipt?",
    "Can I schedule a callback?",
    "What are the options for returns?",
    "How do I escalate my issue?",
    "Can I use the app on multiple devices?",
    "What do I do if I forgot my username?",
    "Are there tutorials for beginners?",
    "What is the current sale offer?",
    "hii",
    "hi",
    "hello",
    "how are you",
    "tell me about"
    "who is the"
]

# Corresponding intents
intents = [
    # connect_with_human labels
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    "connect_with_human", "connect_with_human", "connect_with_human", "connect_with_human",
    # Other intents
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other", "other", "other", "other", "other", "other", "other", "other",
    "other", "other", "other","other","other","other","other","other"
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
message = "How can I reset my account?"
intent = identify_intent(message)
print(f"Identified Intent: {intent}")
