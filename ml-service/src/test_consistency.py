from predict import SpamPredictor

# Create predictor
predictor = SpamPredictor()

# The exact message from your screenshots
test_message = """Congratulations,
A cashback of ₹3,999 has been initiated on your account.
Please confirm your details to avoid reversal.
Thank you for choosing our service."""

print("Testing the EXACT cashback message from your screenshots:")
print("=" * 70)
print(f"Message: {test_message}")
print("=" * 70)

# Test multiple times to verify consistency
print("\n🔄 Testing 5 times to verify consistency:\n")

for i in range(5):
    result = predictor.predict(test_message)
    print(f"Test {i+1}: {result['prediction'].upper()} - "
          f"Confidence: {result['confidence']*100:.2f}% - "
          f"Spam Prob: {result['spam_probability']*100:.2f}%")

print("\n✅ All predictions should be IDENTICAL!")
