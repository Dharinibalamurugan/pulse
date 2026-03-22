import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_devfolio():
    opportunities = []
    try:
        url = "https://devfolio.co/hackathons"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all("div", class_="HackathonCard__StyledCard", limit=5)
        for card in cards:
            title = card.find("h2")
            if title:
                opportunities.append({
                    "title": title.text.strip(),
                    "org": "Devfolio",
                    "type": "Hackathon",
                    "prize": "Varies",
                    "match": 88,
                    "badge": "Hot",
                    "time": datetime.now().strftime("%I:%M %p")
                })
    except:
        pass
    return opportunities

def get_github_bounties():
    opportunities = []
    try:
        url = "https://api.github.com/search/issues?q=bounty+label:bounty+state:open&sort=created&order=desc&per_page=5"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
        for item in data.get("items", [])[:5]:
            opportunities.append({
                "title": item["title"][:60],
                "org": "GitHub",
                "type": "Open Source Bounty",
                "prize": "$100–$1,000",
                "match": 91,
                "badge": "New",
                "time": datetime.now().strftime("%I:%M %p")
            })
    except:
        pass
    return opportunities

def get_fallback_opportunities():
    return [
        {"title": "Google Summer of Code 2026 — ML Track", "org": "Google", "type": "Open Source", "prize": "$3,000–$6,600", "match": 94, "badge": "New", "time": "just now"},
        {"title": "Acumen Fellows Program", "org": "Acumen", "type": "Fellowship", "prize": "Fully Funded", "match": 88, "badge": "Hot", "time": "2m ago"},
        {"title": "Stripe Open Source Grant", "org": "Stripe", "type": "Grant", "prize": "$5,000", "match": 91, "badge": "Closing", "time": "5m ago"},
        {"title": "NASA Open Source Contributor", "org": "NASA", "type": "Internship", "prize": "$4,500", "match": 85, "badge": "New", "time": "8m ago"},
        {"title": "MLH Fellowship — Spring 2026", "org": "MLH", "type": "Fellowship", "prize": "$5,000 stipend", "match": 96, "badge": "Hot", "time": "12m ago"},
        {"title": "UN Youth Climate Innovation Grant", "org": "United Nations", "type": "Grant", "prize": "$10,000", "match": 79, "badge": "New", "time": "15m ago"},
    ]

def get_all_opportunities():
    all_opps = []
    all_opps.extend(get_github_bounties())
    all_opps.extend(scrape_devfolio())
    if len(all_opps) < 3:
        all_opps.extend(get_fallback_opportunities())
    return all_opps

if __name__ == "__main__":
    opps = get_all_opportunities()
    print(f"Found {len(opps)} opportunities:")
    for o in opps:
        print(f"  - {o['title']} ({o['org']})")