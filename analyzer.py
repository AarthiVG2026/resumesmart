import re
from PyPDF2 import PdfReader
from io import BytesIO

DEFAULT_KEYWORDS = [
    'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go',
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'asp.net',
    'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind',
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'ci/cd',
    'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas', 'numpy',
    'testing', 'unit testing', 'jest', 'pytest', 'selenium',
    'linux', 'bash', 'shell scripting', 'devops', 'terraform', 'ansible'
]

ACTION_VERBS = [
    'achieved', 'administered', 'analyzed', 'architected', 'automated', 'built', 'collaborated',
    'created', 'delivered', 'designed', 'developed', 'drove', 'enhanced', 'established',
    'executed', 'generated', 'implemented', 'improved', 'increased', 'initiated', 'launched',
    'led', 'managed', 'optimized', 'orchestrated', 'organized', 'pioneered', 'planned',
    'produced', 'reduced', 'redesigned', 'resolved', 'revamped', 'scaled', 'spearheaded',
    'streamlined', 'transformed', 'upgraded'
]

SECTION_HEADERS = {
    'education': ['education', 'academic', 'qualification', 'degree'],
    'experience': ['experience', 'employment', 'work history', 'professional experience', 'career'],
    'projects': ['projects', 'portfolio', 'personal projects'],
    'skills': ['skills', 'technical skills', 'competencies', 'expertise', 'technologies'],
    'certifications': ['certifications', 'certificates', 'licenses', 'accreditation'],
    'summary': ['summary', 'profile', 'objective', 'about me', 'introduction'],
    'achievements': ['achievements', 'accomplishments', 'awards', 'honors']
}

ROLE_SKILLS = {
    'Software Engineer': ['Python', 'Java', 'C++', 'Git', 'Agile', 'API', 'REST', 'Docker', 'Testing'],
    'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'TensorFlow', 'Analysis'],
    'UI/UX Designer': ['Figma', 'Adobe XD', 'User Research', 'Wireframing', 'Prototyping', 'Typography'],
    'DevOps Engineer': ['Docker', 'Kubernetes', 'Terraform', 'CI/CD', 'AWS', 'Linux', 'Ansible'],
    'Product Manager': ['Roadmapping', 'User Stories', 'Agile', 'Jira', 'Strategy', 'Stakeholder Management'],
    'Full Stack Developer': ['React', 'Node.js', 'Express', 'SQL', 'MongoDB', 'JavaScript', 'HTML', 'CSS'],
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'Responsive Design'],
    'Mobile Developer': ['Swift', 'Kotlin', 'React Native', 'Flutter', 'Android', 'iOS', 'Mobile App'],
    'System Administrator': ['Linux', 'Windows Server', 'Networking', 'Security', 'Scripting', 'Active Directory'],
    'Cybersecurity Analyst': ['Network Security', 'Pentesting', 'Vulnerability Assessment', 'Firewalls', 'SIEM']
}


def extract_email(text):
    regex = r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}'
    matches = re.findall(regex, text)
    return matches[0] if matches else None

def extract_name(text):
    lines = text.split('\n')
    for line in lines:
        line_clean = line.strip()
        if len(line_clean) > 2 and len(line_clean) < 40 and not any(char.isdigit() for char in line_clean) and '@' not in line_clean:
            return line_clean.title()
    return 'Professional Developer'


def extract_phone(text):
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{10}',
        r'\+91[-.\s]?\d{10}',
        r'\d{5}[-.\s]?\d{5}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            cleaned = re.sub(r'[^\d+]', '', phones[0])
            if len(cleaned) >= 10:
                return phones[0]
    return None


def split_into_sections(text):
    lines = text.split('\n')
    sections = {}
    current_section = 'other'
    current_content = []
    
    for line in lines:
        line_lower = line.lower().strip()
        
        matched_section = None
        for section_name, keywords in SECTION_HEADERS.items():
            for keyword in keywords:
                if keyword in line_lower and len(line.strip()) < 50:
                    matched_section = section_name
                    break
            if matched_section:
                break
        
        if matched_section:
            if current_content:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append('\n'.join(current_content))
            current_section = matched_section
            current_content = []
        else:
            if line.strip():
                current_content.append(line)
    
    if current_content:
        if current_section not in sections:
            sections[current_section] = []
        sections[current_section].append('\n'.join(current_content))
    
    return sections


def detect_skills(text, custom_keywords=None):
    keywords_list = custom_keywords if custom_keywords else DEFAULT_KEYWORDS
    text_lower = text.lower()
    
    found_skills = []
    for skill in keywords_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))


def detect_action_verbs(text):
    text_lower = text.lower()
    found_verbs = []
    
    for verb in ACTION_VERBS:
        if re.search(r'\b' + verb + r'\b', text_lower):
            found_verbs.append(verb)
    
    return list(set(found_verbs))


def compute_readability(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            'avg_sentence_length': 0,
            'total_sentences': 0,
            'score': 0,
            'recommendation': 'No readable content found'
        }
    
    total_words = sum(len(s.split()) for s in sentences)
    avg_length = total_words / len(sentences) if sentences else 0
    
    if avg_length < 10:
        score = 60
        recommendation = 'Sentences are too short. Add more detail to your accomplishments.'
    elif 10 <= avg_length <= 20:
        score = 100
        recommendation = 'Excellent readability! Sentences are clear and professional.'
    elif 20 < avg_length <= 30:
        score = 75
        recommendation = 'Good, but some sentences might be long. Consider breaking them up.'
    else:
        score = 50
        recommendation = 'Sentences are too long. Break complex sentences into simpler ones.'
    
    return {
        'avg_sentence_length': round(avg_length, 1),
        'total_sentences': len(sentences),
        'score': score,
        'recommendation': recommendation
    }


def compute_ats_score(metrics):
    score = 0
    max_score = 100
    
    if metrics.get('email'):
        score += 15
    if metrics.get('phone'):
        score += 15
    
    skills_count = len(metrics.get('skills_found', []))
    if skills_count >= 10:
        score += 25
    elif skills_count >= 5:
        score += 15
    elif skills_count >= 3:
        score += 10
    
    action_verbs_count = len(metrics.get('action_verbs', []))
    if action_verbs_count >= 10:
        score += 20
    elif action_verbs_count >= 5:
        score += 12
    elif action_verbs_count >= 3:
        score += 8
    
    sections = metrics.get('sections', {})
    required_sections = ['experience', 'education', 'skills']
    sections_found = sum(1 for sec in required_sections if sec in sections)
    score += sections_found * 8
    
    word_count = len(metrics.get('text', '').split())
    if 300 <= word_count <= 800:
        score += 7
    elif word_count > 200:
        score += 4
    
    return min(score, max_score)


def generate_suggestions(metrics):
    suggestions = []
    
    if not metrics.get('email'):
        suggestions.append({
            'priority': 'high',
            'title': 'Add Contact Email',
            'description': 'Include a professional email address at the top of your resume.'
        })
    
    if not metrics.get('phone'):
        suggestions.append({
            'priority': 'high',
            'title': 'Add Phone Number',
            'description': 'Include a contact phone number for recruiters to reach you.'
        })
    
    skills_count = len(metrics.get('skills_found', []))
    if skills_count < 5:
        suggestions.append({
            'priority': 'high',
            'title': 'Add More Technical Skills',
            'description': f'You have only {skills_count} skills listed. Add more relevant technologies and tools.'
        })
    
    action_verbs_count = len(metrics.get('action_verbs', []))
    if action_verbs_count < 5:
        suggestions.append({
            'priority': 'medium',
            'title': 'Use More Action Verbs',
            'description': 'Start bullet points with strong action verbs like "developed", "implemented", "led".'
        })
    
    readability = metrics.get('readability', {})
    if readability.get('avg_sentence_length', 0) > 25:
        suggestions.append({
            'priority': 'medium',
            'title': 'Improve Readability',
            'description': 'Break down long sentences into shorter, clearer statements.'
        })
    
    sections = metrics.get('sections', {})
    if 'projects' not in sections:
        suggestions.append({
            'priority': 'low',
            'title': 'Add Projects Section',
            'description': 'Showcase personal or professional projects to demonstrate your skills.'
        })
    
    if 'summary' not in sections and 'profile' not in sections:
        suggestions.append({
            'priority': 'medium',
            'title': 'Add Professional Summary',
            'description': 'Include a brief summary at the top highlighting your key strengths.'
        })
    
    word_count = len(metrics.get('text', '').split())
    if word_count < 200:
        suggestions.append({
            'priority': 'high',
            'title': 'Expand Content',
            'description': 'Your resume is too brief. Add more details about your experience and achievements.'
        })
    elif word_count > 800:
        suggestions.append({
            'priority': 'medium',
            'title': 'Reduce Content',
            'description': 'Your resume is too long. Focus on the most relevant and impactful information.'
        })
    
    missing_skills = metrics.get('missing_skills', [])
    if len(missing_skills) > 0:
        top_missing = ', '.join(missing_skills[:5])
        suggestions.append({
            'priority': 'high',
            'title': 'Add Missing Keywords',
            'description': f'Include these relevant keywords: {top_missing}'
        })
    
    return sorted(suggestions, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['priority']])[:6]


def generate_improved_bullets(text, skills_found, action_verbs):
    improved = []
    
    skill_1 = skills_found[0] if len(skills_found) > 0 else 'modern technologies'
    skill_2 = skills_found[1] if len(skills_found) > 1 else 'industry standards'
    skill_3 = skills_found[2] if len(skills_found) > 2 else 'best practices'
    
    verb_1 = action_verbs[0].capitalize() if len(action_verbs) > 0 else 'Architected'
    verb_2 = action_verbs[1].capitalize() if len(action_verbs) > 1 else 'Spearheaded'
    verb_3 = action_verbs[2].capitalize() if len(action_verbs) > 2 else 'Optimized'

    improved.append(f"{verb_1} scalable solutions using {skill_1} and {skill_2}, reducing system latency by 25%.")
    improved.append(f"{verb_2} a cross-functional initiative to integrate {skill_3}, which accelerated delivery timelines by [X] weeks.")
    improved.append(f"{verb_3} critical data workflows with {skill_1}, successfully supporting a [X]% increase in daily active users.")
    
    return improved


def analyze_resume(text, job_keywords=None, target_role=None):
    
    email = extract_email(text)
    phone = extract_phone(text)
    full_name = extract_name(text)
    sections = split_into_sections(text)
    
    custom_keywords = []
    if job_keywords:
        custom_keywords = [kw.strip().lower() for kw in re.split(r'[,\n]+', job_keywords) if kw.strip()]
    
    if target_role and target_role in ROLE_SKILLS:
        custom_keywords.extend([s.lower() for s in ROLE_SKILLS[target_role]])
    
    search_keywords = list(set(custom_keywords + [s.lower() for s in DEFAULT_KEYWORDS]))
    
    skills_found = detect_skills(text, search_keywords)
    action_verbs = detect_action_verbs(text)
    readability = compute_readability(text)
    
    missing_skills = []
    role_matching_score = 0
    
    if target_role and target_role in ROLE_SKILLS:
        role_req_skills = [s.lower() for s in ROLE_SKILLS[target_role]]
        missing_skills = [s for s in role_req_skills if s not in [sf.lower() for sf in skills_found]]
        
        if role_req_skills:
            matched_role_skills = len(role_req_skills) - len(missing_skills)
            role_matching_score = (matched_role_skills / len(role_req_skills)) * 100
    elif job_keywords:
        job_kw_list = [kw.strip().lower() for kw in re.split(r'[,\n]+', job_keywords) if kw.strip()]
        missing_skills = [kw for kw in job_kw_list if kw not in [s.lower() for s in skills_found]]
    
    metrics = {
        'text': text,
        'email': email,
        'phone': phone,
        'sections': sections,
        'skills_found': skills_found,
        'action_verbs': action_verbs,
        'readability': readability,
        'missing_skills': missing_skills,
        'target_role': target_role
    }
    
    ats_score = compute_ats_score(metrics)
    
    # Adjust ATS score based on role matching if applicable
    if target_role and target_role in ROLE_SKILLS:
        # A completely irrelevant resume should score very poorly, regardless of format.
        # Health is 40%, Role Relevance is 60%.
        ats_score = (ats_score * 0.4) + (role_matching_score * 0.6)
    
    suggestions = generate_suggestions(metrics)
    
    experience_text = '\n'.join(sections.get('experience', [])) if 'experience' in sections else text[:500]
    improved_bullets = generate_improved_bullets(experience_text, skills_found, action_verbs)
    
    return {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'sections': sections,
        'skills_found': skills_found,
        'missing_skills': missing_skills,
        'action_verbs': action_verbs,
        'readability': readability,
        'ats_score': round(ats_score, 1),
        'suggestions': suggestions,
        'improved_bullets': improved_bullets,
        'word_count': len(text.split()),
        'target_role': target_role,
        'role_match_score': round(role_matching_score, 1) if target_role else None
    }
