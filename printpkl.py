import pickle
with open('responses.pkl', 'rb') as f:
    responses = pickle.load(f)
print(responses)