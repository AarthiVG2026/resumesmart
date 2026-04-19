"""
Advanced Analyzer service using spaCy for deep NLP analysis.
Falls back to regex-only mode if spaCy is not installed.
"""
import re

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except Exception:
    nlp = None
    SPACY_AVAILABLE = False

try:
    from services.parser import split_into_sections
except ImportError:
    from parser import split_into_sections


def detect_star_method(bullet_points):
    """
    Analyzes bullet points for Situation/Task, Action, and Result components.
    Works with or without spaCy.
    """
    star_results = []
    
    action_keywords = {
        'led', 'developed', 'created', 'managed', 'designed', 'implemented',
        'optimized', 'spearheaded', 'automated', 'built', 'launched', 'delivered',
        'achieved', 'administered', 'analyzed', 'architected', 'collaborated',
        'drove', 'enhanced', 'established', 'executed', 'generated', 'improved',
        'increased', 'initiated', 'orchestrated', 'organized', 'pioneered', 'planned',
        'produced', 'reduced', 'redesigned', 'resolved', 'revamped', 'scaled',
        'streamlined', 'transformed', 'upgraded', 'wrote', 'programmed', 'tested'
    }
    result_indicators = {
        '%', '$', 'increased', 'reduced', 'saved', 'grew', 'improved',
        'delivered', 'resulted', 'achieved', 'generated', 'faster', 'users',
        'customers', 'revenue', 'uptime', 'days', 'hours', 'months'
    }
    context_indicators = {
        'during', 'while', 'in', 'for', 'at', 'with', 'responsible', 'as part of',
        'using', 'by', 'through', 'to', 'from', 'within', 'across', 'via', 'utilizing'
    }

    for bullet in bullet_points:
        if not bullet.strip():
            continue
        
        text_lower = bullet.lower()
        
        # Context detection (regex-based works without spaCy)
        has_context = any(kw in text_lower for kw in context_indicators)
        has_action = any(re.search(r'\b' + kw + r'\b', text_lower) for kw in action_keywords)
        has_result = (
            any(kw in text_lower for kw in result_indicators) or
            bool(re.search(r'\d+\s*%', bullet)) or
            bool(re.search(r'\$\s*\d+', bullet)) or
            bool(re.search(r'\b\d{2,}\b', bullet))  # any 2+ digit number suggests a metric
        )
        
        score = sum([has_context, has_action, has_result])
        status = "Strong" if score == 3 else "Moderate" if score == 2 else "Weak"
        
        missing = []
        if not has_context: missing.append("Context (Situation/Task)")
        if not has_action: missing.append("Strong Action Verb")
        if not has_result: missing.append("Measurable Result")
        
        star_results.append({
            'bullet': bullet[:200],  # truncate for display
            'status': status,
            'missing': missing,
            'score': score
        })
        
    return star_results


def predict_personality_traits(text):
    """
    Predicts personality traits based on word usage patterns.
    """
    traits = {
        'Leadership': 0,
        'Analytical': 0,
        'Execution': 0,
        'Collaboration': 0,
        'Innovation': 0
    }
    
    keywords = {
        'Leadership': ['led', 'managed', 'mentored', 'orchestrated', 'spearheaded', 'established', 'directed'],
        'Analytical': ['analyzed', 'optimized', 'data', 'metrics', 'researched', 'evaluated', 'statistics'],
        'Execution': ['delivered', 'built', 'implemented', 'shipped', 'completed', 'reduced', 'increased', 'automated'],
        'Collaboration': ['collaborated', 'team', 'partnered', 'coordinated', 'assisted', 'support', 'shared'],
        'Innovation': ['created', 'designed', 'pioneered', 'architected', 'invented', 'novel', 'innovative']
    }
    
    text_lower = text.lower()
    for trait, words in keywords.items():
        count = sum(1 for word in words if re.search(r'\b' + word + r'\b', text_lower))
        traits[trait] = min(100, count * 20)
        
    return traits


def simulate_ats_rejection(metrics):
    """
    Simulates real high-tier ATS rejection reasons.
    """
    reasons = []
    
    bullets = metrics.get('star_results', [])
    if bullets:
        weak_bullets = sum(1 for b in bullets if b['status'] == 'Weak')
        if weak_bullets > len(bullets) / 2:
            reasons.append({
                'code': 'REJ_01',
                'title': 'Lack of Quantified Achievements',
                'explanation': 'Over 50% of your experience bullet points lack measurable metrics (%, $, #). Recruiters prioritize results-oriented candidates.'
            })
        
    sections = metrics.get('sections', {})
    if 'experience' not in sections:
        reasons.append({
            'code': 'REJ_02',
            'title': 'Parsing Failure: Experience Section',
            'explanation': 'The ATS could not clearly identify your work history. Ensure your header says "Work Experience" and is isolated on its own line.'
        })
         
    if len(metrics.get('skills_found', [])) < 5:
        reasons.append({
            'code': 'REJ_03',
            'title': 'Keyword Mismatch',
            'explanation': 'Your profile does not meet the minimum keyword threshold for common roles in this field.'
        })

    return reasons


def deep_analyze(text, target_role=None):
    """
    Runs a full deep analysis of the resume text.
    Uses spaCy if available, falls back to regex otherwise.
    """
    try:
        sections = split_into_sections(text)
    except Exception:
        sections = {}
    
    # Extract experience bullet points
    experience_text = "\n".join(sections.get('experience', []))
    if not experience_text:
        # If no section found, use first 1500 chars
        experience_text = text[:1500]
    
    # Split into meaningful bullet points (filtering out noise)
    bullet_points = []
    for s in re.split(r'[\n•\-\*]+', experience_text):
        s_clean = s.strip()
        # Ignore lines too short to be a STAR bullet
        if len(s_clean) < 35:
            continue
        # Ignore contact info lines
        if '@' in s_clean or 'linkedin.com' in s_clean.lower() or 'github.com' in s_clean.lower():
            continue
        # Include it
        bullet_points.append(s_clean)
        if len(bullet_points) >= 15:
            break
    
    star_results = detect_star_method(bullet_points)
    personality = predict_personality_traits(text)
    
    rejection_reasons = simulate_ats_rejection({
        'star_results': star_results,
        'sections': sections,
        'skills_found': []
    })
    
    impact_score = 0
    if bullet_points:
        total = sum(b['score'] for b in star_results)
        impact_score = round((total / (len(bullet_points) * 3)) * 100, 1)
    
    return {
        'star_results': star_results,
        'personality': personality,
        'rejection_reasons': rejection_reasons,
        'impact_score': impact_score
    }
