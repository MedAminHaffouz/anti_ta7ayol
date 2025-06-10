
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "AIzaSyBvSa477dy5JF5krImDR1Gi56-AMLtOmOI"

def classify_claim(claim_text, similarity_threshold=0.6):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={claim_text}&key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'claims' not in data:
            return -1  # no claims found

        # Prepare texts for similarity check
        input_texts = [claim_text]
        for claim in data['claims']:
            claim_text_api = claim.get('text', '')
            # TF-IDF vectors for input and API claim
            vectorizer = TfidfVectorizer().fit(input_texts + [claim_text_api])
            vectors = vectorizer.transform(input_texts + [claim_text_api])
            sim = cosine_similarity(vectors[0], vectors[1])[0][0]

            # print(sim, claim_text_api)  # Uncomment to debug similarity scores
            
            if sim >= similarity_threshold:
                # Trust this claim rating
                rating = claim.get('claimReview', [{}])[0].get('textualRating', '').lower()
                if 'true' in rating:
                    return 1
                elif 'false' in rating:
                    return 0
                else:
                    return -1
        return -1  # no similar claims found
    except requests.RequestException:
        return -1  # network or API error


