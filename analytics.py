from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_issues(
    new_description,
    existing_descriptions,
    threshold=0.4
):
    """
    Find previous complaints similar to the new complaint.
    """

    if not existing_descriptions:
        return []

    descriptions = existing_descriptions + [new_description]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        descriptions
    )

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    similar_issues = []

    for i, score in enumerate(similarities):

        if score >= threshold:

            similar_issues.append({
                "index": i,
                "similarity": round(
                    score * 100,
                    2
                )
            })

    # Highest similarity first
    similar_issues.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return similar_issues