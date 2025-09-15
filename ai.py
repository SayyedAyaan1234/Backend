import random

def analyze_image(image_path):
    # Replace this with real model prediction later
    phytos = random.randint(20, 80)
    zoos = random.randint(0, 30)
    total = phytos + zoos
    counts = {"phytoplankton": phytos, "zooplankton": zoos, "total": total}
    meta = {"note": "Mock result - replace with real AI model"}
    return counts, meta
