import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the secret key
secret = os.getenv("BETTER_AUTH_SECRET")
print(f"Secret key: {secret}")

# Create a test payload
payload = {
    "sub": "user_test123",
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(minutes=15),
    "iat": datetime.utcnow(),
    "iss": "todo-app",
    "aud": "todo-app-users"
}

print(f"Payload: {payload}")

# Encode the token
try:
    encoded_token = jwt.encode(payload, secret, algorithm="HS256")
    print(f"Encoded token: {encoded_token}")

    # Decode the token to verify with audience
    decoded_payload = jwt.decode(encoded_token, secret, algorithms=["HS256"], audience="todo-app-users")
    print(f"Decoded payload: {decoded_payload}")
    print("SUCCESS: Token encoding/decoding works correctly!")

except Exception as e:
    print(f"ERROR: {e}")