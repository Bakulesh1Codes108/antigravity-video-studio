import json

# Curated high-impact WTF-style bilingual / English subtitle chunks aligned with the user speech timestamps:
# Spoken timing:
# 0.7 - 3.4: "GUYS, WHAT IF I TOLD YOU..."
# 3.5 - 5.7: "WHILE WORKING YOUR DAILY JOB..."
# 5.8 - 7.6: "YOU CAN EARN ₹10K - ₹20K FROM HOME?"
# 7.7 - 9.3: "WOULD YOU BELIEVE ME?"
# 9.5 - 12.3: "LOOK CLOSELY AT THIS..."
# 12.4 - 15.2: "AI CANNOT AUTOMATE THIS!"
# 15.3 - 17.0: "COMPUTERS CAN NEVER REPLACE IT!"
# 17.1 - 19.2: "IT ONLY REQUIRES YOUR HANDS!"
# 19.4 - 22.5: "PRODUCTION COST? ONLY 60 PAISE!"
# 22.6 - 26.0: "AND SELLS FOR MASSIVE PROFIT!"
# 26.1 - 27.5: "YOU MAKE HUGE MONEY!"
# 27.6 - 30.8: "THERE ARE 3 PROVEN CATEGORIES..."
# 31.0 - 33.5: "THAT GENERATE REAL CASHFLOW ASSETS!"
# 33.8 - 36.2: "IF YOU WANT TO MASTER THIS SKILL..."
# 36.3 - 39.5: "REGISTER FOR MY MASTERCLASS NOW!"
# 41.0 - 43.5: "THIS DEMAND WILL NEVER DIE!"
# 43.6 - 45.8: "BUYERS WILL ALWAYS COME TO YOU!"
# 45.9 - 48.5: "AND NO AI CAN EVER AUTOMATE THIS!"
# 48.6 - 51.5: "A 100% BULLETPROOF BUSINESS!"
# 51.8 - 54.7: "ONCE YOU MAKE A SMALL INVESTMENT..."
# 54.8 - 57.0: "YOU GET 10X RETURNS ON PROFIT!"
# 57.2 - 59.8: "JOIN MY CLASS RIGHT NOW..."
# 59.9 - 61.2: "TODAY!"

captions = [
    {
        "start": 0.70, "end": 3.40,
        "words": [
            {"text": "GUYS,", "highlight": False, "start": 0.70, "end": 1.40},
            {"text": "WHAT", "highlight": False, "start": 1.40, "end": 1.90},
            {"text": "IF", "highlight": False, "start": 1.90, "end": 2.30},
            {"text": "I", "highlight": False, "start": 2.30, "end": 2.70},
            {"text": "TOLD", "highlight": True, "color": "#FFE600", "start": 2.70, "end": 3.05},
            {"text": "YOU...", "highlight": True, "color": "#FFE600", "start": 3.05, "end": 3.40}
        ]
    },
    {
        "start": 3.45, "end": 5.65,
        "words": [
            {"text": "WHILE", "highlight": False, "start": 3.45, "end": 3.90},
            {"text": "WORKING", "highlight": False, "start": 3.90, "end": 4.40},
            {"text": "YOUR", "highlight": False, "start": 4.40, "end": 4.80},
            {"text": "DAILY", "highlight": True, "color": "#22C55E", "start": 4.80, "end": 5.20},
            {"text": "JOB...", "highlight": True, "color": "#22C55E", "start": 5.20, "end": 5.65}
        ]
    },
    {
        "start": 5.70, "end": 7.60,
        "words": [
            {"text": "YOU", "highlight": False, "start": 5.70, "end": 6.00},
            {"text": "CAN", "highlight": False, "start": 6.00, "end": 6.30},
            {"text": "EARN", "highlight": False, "start": 6.30, "end": 6.70},
            {"text": "₹10,000", "highlight": True, "color": "#FFE600", "start": 6.70, "end": 7.15},
            {"text": "TO", "highlight": False, "start": 7.15, "end": 7.30},
            {"text": "₹20,000", "highlight": True, "color": "#FFE600", "start": 7.30, "end": 7.60}
        ]
    },
    {
        "start": 7.65, "end": 9.30,
        "words": [
            {"text": "SITTING", "highlight": False, "start": 7.65, "end": 8.10},
            {"text": "AT", "highlight": False, "start": 8.10, "end": 8.40},
            {"text": "HOME,", "highlight": True, "color": "#22C55E", "start": 8.40, "end": 8.80},
            {"text": "BELIEVE", "highlight": True, "color": "#FFE600", "start": 8.80, "end": 9.10},
            {"text": "IT?", "highlight": True, "color": "#FFE600", "start": 9.10, "end": 9.30}
        ]
    },
    {
        "start": 9.40, "end": 12.20,
        "words": [
            {"text": "LOOK", "highlight": True, "color": "#FFE600", "start": 9.40, "end": 10.00},
            {"text": "CLOSELY", "highlight": True, "color": "#FFE600", "start": 10.00, "end": 10.80},
            {"text": "AT", "highlight": False, "start": 10.80, "end": 11.40},
            {"text": "THIS...", "highlight": False, "start": 11.40, "end": 12.20}
        ]
    },
    {
        "start": 12.30, "end": 15.20,
        "words": [
            {"text": "AI", "highlight": True, "color": "#EF4444", "start": 12.30, "end": 12.90},
            {"text": "CANNOT", "highlight": True, "color": "#EF4444", "start": 12.90, "end": 13.60},
            {"text": "AUTOMATE", "highlight": True, "color": "#FFE600", "start": 13.60, "end": 14.40},
            {"text": "THIS!", "highlight": True, "color": "#FFE600", "start": 14.40, "end": 15.20}
        ]
    },
    {
        "start": 15.25, "end": 17.00,
        "words": [
            {"text": "COMPUTERS", "highlight": False, "start": 15.25, "end": 15.90},
            {"text": "CAN", "highlight": False, "start": 15.90, "end": 16.30},
            {"text": "NEVER", "highlight": True, "color": "#EF4444", "start": 16.30, "end": 16.65},
            {"text": "REPLACE", "highlight": True, "color": "#EF4444", "start": 16.65, "end": 17.00}
        ]
    },
    {
        "start": 17.05, "end": 19.30,
        "words": [
            {"text": "IT", "highlight": False, "start": 17.05, "end": 17.50},
            {"text": "ONLY", "highlight": False, "start": 17.50, "end": 18.00},
            {"text": "TAKES", "highlight": False, "start": 18.00, "end": 18.45},
            {"text": "YOUR", "highlight": True, "color": "#22C55E", "start": 18.45, "end": 18.85},
            {"text": "HANDS!", "highlight": True, "color": "#22C55E", "start": 18.85, "end": 19.30}
        ]
    },
    {
        "start": 19.40, "end": 22.50,
        "words": [
            {"text": "PRODUCTION", "highlight": False, "start": 19.40, "end": 20.20},
            {"text": "COST?", "highlight": False, "start": 20.20, "end": 20.80},
            {"text": "ONLY", "highlight": True, "color": "#FFE600", "start": 20.80, "end": 21.40},
            {"text": "60", "highlight": True, "color": "#22C55E", "start": 21.40, "end": 21.90},
            {"text": "PAISE!", "highlight": True, "color": "#22C55E", "start": 21.90, "end": 22.50}
        ]
    },
    {
        "start": 22.60, "end": 26.00,
        "words": [
            {"text": "AND", "highlight": False, "start": 22.60, "end": 23.20},
            {"text": "SELLS", "highlight": True, "color": "#FFE600", "start": 23.20, "end": 23.90},
            {"text": "AT", "highlight": False, "start": 23.90, "end": 24.40},
            {"text": "MASSIVE", "highlight": True, "color": "#22C55E", "start": 24.40, "end": 25.10},
            {"text": "MARGINS!", "highlight": True, "color": "#22C55E", "start": 25.10, "end": 26.00}
        ]
    },
    {
        "start": 26.10, "end": 27.50,
        "words": [
            {"text": "YOU", "highlight": False, "start": 26.10, "end": 26.45},
            {"text": "MAKE", "highlight": False, "start": 26.45, "end": 26.80},
            {"text": "SERIOUS", "highlight": True, "color": "#FFE600", "start": 26.80, "end": 27.15},
            {"text": "MONEY!", "highlight": True, "color": "#FFE600", "start": 27.15, "end": 27.50}
        ]
    },
    {
        "start": 27.55, "end": 30.80,
        "words": [
            {"text": "THERE", "highlight": False, "start": 27.55, "end": 28.10},
            {"text": "ARE", "highlight": False, "start": 28.10, "end": 28.50},
            {"text": "3", "highlight": True, "color": "#FFE600", "start": 28.50, "end": 29.10},
            {"text": "PROVEN", "highlight": True, "color": "#FFE600", "start": 29.10, "end": 29.80},
            {"text": "MODELS...", "highlight": False, "start": 29.80, "end": 30.80}
        ]
    },
    {
        "start": 30.90, "end": 33.50,
        "words": [
            {"text": "THAT", "highlight": False, "start": 30.90, "end": 31.40},
            {"text": "BUILD", "highlight": False, "start": 31.40, "end": 31.90},
            {"text": "REAL", "highlight": True, "color": "#22C55E", "start": 31.90, "end": 32.50},
            {"text": "CASHFLOW", "highlight": True, "color": "#FFE600", "start": 32.50, "end": 33.00},
            {"text": "ASSETS!", "highlight": True, "color": "#FFE600", "start": 33.00, "end": 33.50}
        ]
    },
    {
        "start": 33.70, "end": 36.20,
        "words": [
            {"text": "WANT", "highlight": False, "start": 33.70, "end": 34.20},
            {"text": "TO", "highlight": False, "start": 34.20, "end": 34.60},
            {"text": "LEARN", "highlight": True, "color": "#FFE600", "start": 34.60, "end": 35.20},
            {"text": "THIS", "highlight": False, "start": 35.20, "end": 35.60},
            {"text": "SKILL?", "highlight": True, "color": "#FFE600", "start": 35.60, "end": 36.20}
        ]
    },
    {
        "start": 36.30, "end": 39.50,
        "words": [
            {"text": "REGISTER", "highlight": True, "color": "#22C55E", "start": 36.30, "end": 37.10},
            {"text": "FOR", "highlight": False, "start": 37.10, "end": 37.50},
            {"text": "MY", "highlight": False, "start": 37.50, "end": 37.90},
            {"text": "MASTERCLASS!", "highlight": True, "color": "#FFE600", "start": 37.90, "end": 39.50}
        ]
    },
    {
        "start": 40.80, "end": 43.40,
        "words": [
            {"text": "THIS", "highlight": False, "start": 40.80, "end": 41.30},
            {"text": "DEMAND", "highlight": True, "color": "#FFE600", "start": 41.30, "end": 42.00},
            {"text": "WILL", "highlight": False, "start": 42.00, "end": 42.40},
            {"text": "NEVER", "highlight": True, "color": "#EF4444", "start": 42.40, "end": 42.90},
            {"text": "DIE!", "highlight": True, "color": "#EF4444", "start": 42.90, "end": 43.40}
        ]
    },
    {
        "start": 43.50, "end": 45.70,
        "words": [
            {"text": "BUYERS", "highlight": True, "color": "#FFE600", "start": 43.50, "end": 44.10},
            {"text": "WILL", "highlight": False, "start": 44.10, "end": 44.50},
            {"text": "ALWAYS", "highlight": False, "start": 44.50, "end": 45.00},
            {"text": "FIND", "highlight": True, "color": "#22C55E", "start": 45.00, "end": 45.35},
            {"text": "YOU!", "highlight": True, "color": "#22C55E", "start": 45.35, "end": 45.70}
        ]
    },
    {
        "start": 45.80, "end": 48.50,
        "words": [
            {"text": "NO", "highlight": True, "color": "#EF4444", "start": 45.80, "end": 46.30},
            {"text": "AI", "highlight": True, "color": "#EF4444", "start": 46.30, "end": 46.80},
            {"text": "CAN", "highlight": False, "start": 46.80, "end": 47.20},
            {"text": "EVER", "highlight": True, "color": "#FFE600", "start": 47.20, "end": 47.80},
            {"text": "AUTOMATE", "highlight": True, "color": "#FFE600", "start": 47.80, "end": 48.50}
        ]
    },
    {
        "start": 48.60, "end": 51.50,
        "words": [
            {"text": "IT'S", "highlight": False, "start": 48.60, "end": 49.10},
            {"text": "A", "highlight": False, "start": 49.10, "end": 49.40},
            {"text": "PROVEN,", "highlight": True, "color": "#22C55E", "start": 49.40, "end": 50.10},
            {"text": "REAL-WORLD", "highlight": True, "color": "#FFE600", "start": 50.10, "end": 50.80},
            {"text": "BUSINESS!", "highlight": True, "color": "#FFE600", "start": 50.80, "end": 51.50}
        ]
    },
    {
        "start": 51.70, "end": 54.60,
        "words": [
            {"text": "ONCE", "highlight": False, "start": 51.70, "end": 52.20},
            {"text": "YOU", "highlight": False, "start": 52.20, "end": 52.60},
            {"text": "INVEST", "highlight": True, "color": "#FFE600", "start": 52.60, "end": 53.30},
            {"text": "JUST", "highlight": False, "start": 53.30, "end": 53.80},
            {"text": "ONCE...", "highlight": True, "color": "#FFE600", "start": 53.80, "end": 54.60}
        ]
    },
    {
        "start": 54.70, "end": 57.00,
        "words": [
            {"text": "YOU", "highlight": False, "start": 54.70, "end": 55.10},
            {"text": "GET", "highlight": False, "start": 55.10, "end": 55.50},
            {"text": "10X", "highlight": True, "color": "#22C55E", "start": 55.50, "end": 56.10},
            {"text": "RETURNS", "highlight": True, "color": "#22C55E", "start": 56.10, "end": 56.55},
            {"text": "BACK!", "highlight": True, "color": "#FFE600", "start": 56.55, "end": 57.00}
        ]
    },
    {
        "start": 57.10, "end": 59.70,
        "words": [
            {"text": "JOIN", "highlight": True, "color": "#FFE600", "start": 57.10, "end": 57.60},
            {"text": "MY", "highlight": False, "start": 57.60, "end": 58.00},
            {"text": "MASTERCLASS", "highlight": True, "color": "#22C55E", "start": 58.00, "end": 59.00},
            {"text": "TODAY...", "highlight": True, "color": "#FFE600", "start": 59.00, "end": 59.70}
        ]
    },
    {
        "start": 59.80, "end": 61.20,
        "words": [
            {"text": "START", "highlight": True, "color": "#22C55E", "start": 59.80, "end": 60.40},
            {"text": "NOW!", "highlight": True, "color": "#FFE600", "start": 60.40, "end": 61.20}
        ]
    }
]

with open("/Users/brane/Downloads/antigravity-video-studio-transfer/projects/nikhil-kamath-wtf-style/assets/captions.json", "w") as f:
    json.dump(captions, f, indent=2)

print("Saved WTF style kinetic captions!")
