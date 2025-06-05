import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fact_check import classify_claim

result = classify_claim("apple is healthy")
print("Returned:", result)


