import google.generativeai as genai

# WE WILL PASTE THE KEY DIRECTLY HERE
TEST_KEY = "AIzaSyBtFhJ3Zbfkr3Phx1OBAa6hkSySROwKBZA,AIzaSyBwzrQpesMjkWvEOBV1dAtHx30qpjEeCC0,AIzaSyCqxMV8ZpfdmRVFscnIN1qIS918n-1feIg"

print("\n" + "="*50)
print(f"Testing Key: {TEST_KEY[:5]}...{TEST_KEY[-4:]}")

try:
    genai.configure(api_key=TEST_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content("Reply with exactly the word 'ONLINE'.")
    print(f"🎉 SUCCESS! Google says: {res.text.strip()}")
except Exception as e:
    print(f"❌ FAILED: {e}")
print("="*50 + "\n")
