from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Training data
texts = [

    # Network
    "wifi is not working",
    "wifi connection is down",
    "internet is not working",
    "internet connection is very slow",
    "network problem in computer lab",
    "no internet in classroom",
    "campus wifi keeps disconnecting",
    "unable to connect to wifi",
    "network connection failed",
    "internet service is unavailable",

    # Electrical
    "electricity is not working",
    "power is not available in classroom",
    "light is not working",
    "classroom lights are broken",
    "fan is not working",
    "ceiling fan has stopped working",
    "electrical switch is damaged",
    "power failure in laboratory",
    "short circuit in classroom",
    "electric socket is damaged",

    # Water
    "water is leaking",
    "water leakage in washroom",
    "tap is not working",
    "water supply is unavailable",
    "no water in washroom",
    "pipeline is leaking",
    "water pipe is broken",
    "drinking water problem",
    "water tank is overflowing",
    "faucet is damaged",

    # Cleanliness
    "washroom is dirty",
    "classroom is not clean",
    "garbage is not collected",
    "dust is everywhere",
    "garbage is overflowing",
    "toilet needs cleaning",
    "dirty campus area",
    "washroom cleaning is required",
    "trash is lying near the building",
    "campus is not properly cleaned",

    # Security
    "security guard is missing",
    "cctv camera is not working",
    "security problem on campus",
    "unauthorized entry into campus",
    "theft reported in hostel",
    "security camera is broken",
    "gate security is poor",
    "suspicious person on campus",
    "security guard is not available",
    "campus safety problem",

    # Infrastructure
    "classroom door is broken",
    "wall is damaged",
    "building needs repair",
    "roof is damaged",
    "classroom ceiling is damaged",
    "laboratory infrastructure is damaged",
    "broken window in classroom",
    "floor is damaged",
    "building structure needs repair",
    "classroom furniture is damaged",

    # Maintenance
    "equipment needs repair",
    "computer needs maintenance",
    "broken equipment needs repair",
    "laboratory equipment is not working",
    "printer needs repair",
    "projector is not working",
    "maintenance is required",
    "machine needs servicing",
    "broken chair needs repair",
    "repair work is required"
]


labels = [

    # Network
    "Network", "Network", "Network", "Network", "Network",
    "Network", "Network", "Network", "Network", "Network",

    # Electrical
    "Electrical", "Electrical", "Electrical", "Electrical", "Electrical",
    "Electrical", "Electrical", "Electrical", "Electrical", "Electrical",

    # Water
    "Water", "Water", "Water", "Water", "Water",
    "Water", "Water", "Water", "Water", "Water",

    # Cleanliness
    "Cleanliness", "Cleanliness", "Cleanliness", "Cleanliness", "Cleanliness",
    "Cleanliness", "Cleanliness", "Cleanliness", "Cleanliness", "Cleanliness",

    # Security
    "Security", "Security", "Security", "Security", "Security",
    "Security", "Security", "Security", "Security", "Security",

    # Infrastructure
    "Infrastructure", "Infrastructure", "Infrastructure", "Infrastructure",
    "Infrastructure", "Infrastructure", "Infrastructure", "Infrastructure",
    "Infrastructure", "Infrastructure",

    # Maintenance
    "Maintenance", "Maintenance", "Maintenance", "Maintenance", "Maintenance",
    "Maintenance", "Maintenance", "Maintenance", "Maintenance", "Maintenance"
]


# Convert text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(texts)


# Train ML classifier
model = LogisticRegression(
    max_iter=1000
)

model.fit(X, labels)


def predict_category(description):
    """
    Predict the campus problem category using ML.
    """
    text = vectorizer.transform([description])
    return model.predict(text)[0]


def predict_category_with_confidence(description):
    """
    Predict category and return confidence score.
    """
    text = vectorizer.transform([description])

    probabilities = model.predict_proba(text)[0]

    prediction = model.classes_[probabilities.argmax()]

    confidence = probabilities.max() * 100

    return prediction, round(confidence, 2)


def predict_priority(description):
    """
    Predict complaint priority.
    """
    text = description.lower()

    if any(word in text for word in [
        "emergency",
        "danger",
        "fire",
        "short circuit",
        "unsafe",
        "accident",
        "life threatening"
    ]):
        return "Critical"

    elif any(word in text for word in [
        "not working",
        "broken",
        "leak",
        "no internet",
        "power failure",
        "security",
        "urgent"
    ]):
        return "High"

    elif any(word in text for word in [
        "problem",
        "issue",
        "slow",
        "damaged",
        "dirty"
    ]):
        return "Medium"

    return "Low"


def recommend_department(category):
    """
    Recommend the responsible department.
    """

    departments = {
        "Network": "IT Department",
        "Electrical": "Electrical Department",
        "Water": "Maintenance Department",
        "Cleanliness": "Housekeeping",
        "Security": "Security Department",
        "Infrastructure": "Maintenance Department",
        "Maintenance": "Maintenance Department"
    }

    return departments.get(
        category,
        "Administration"
    )