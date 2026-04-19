import re

def scan_job_description(jd_text):
    """
    Scans a Job Description for red flags, phishing, or scams.
    """
    flags = []
    
    # Red Flag 1: Suspicious Links
    suspicious_patterns = [
        r'bit\.ly', r'tinyurl\.com', r'goo\.gl', r't\.co',
        r'whatsapp\.me', r't\.me'
    ]
    
    links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', jd_text)
    for link in links:
        if any(re.search(p, link) for p in suspicious_patterns):
            flags.append({
                'type': 'Link Security',
                'severity': 'high',
                'title': 'Suspicious Shortened URL',
                'detail': f'Detected a shortened link: {link}. Scammers often use these to hide malicious destinations.'
            })
            
    # Red Flag 2: Generic Scam Keywords
    scam_keywords = {
        'payment': 'Request for payment or bank details early in the process.',
        'telegram': 'Instruction to move conversation to Telegram immediately.',
        'whatsapp': 'Instruction to move conversation to WhatsApp immediately.',
        'crypto': 'Unusual mentions of cryptocurrency or digital wallets.',
        'package': 'Offers related to "re-packaging" or "shipping" from home.'
    }
    
    for kw, description in scam_keywords.items():
        if kw in jd_text.lower():
            flags.append({
                'type': 'Content Trust',
                'severity': 'medium',
                'title': f'Scam Indicator: {kw.capitalize()}',
                'detail': description
            })
            
    # Red Flag 3: Personal Email Domains for Hiring
    free_email_providers = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b', jd_text)
    
    for domain in emails:
        if domain.lower() in free_email_providers:
            flags.append({
                'type': 'Professionalism',
                'severity': 'low',
                'title': 'Generic Email Domain',
                'detail': 'Job description uses a personal email address (Gmail/Yahoo) instead of a corporate domain. Exercise caution.'
            })

    trust_score = max(0, 100 - (len(flags) * 25))
    
    return {
        'trust_score': trust_score,
        'flags': flags,
        'status': 'Safe' if trust_score > 80 else 'Caution' if trust_score > 50 else 'High Risk'
    }
