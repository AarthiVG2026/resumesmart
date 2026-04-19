import random

def generate_interview_questions(text, role=None):
    """
    Generates tailored interview questions based on resume content.
    """
    questions = []
    
    # Technical Questions based on keywords
    tech_keywords = {
        'Python': ['Explain decorators in Python.', 'How do you manage memory in Python?', 'Difference between list and tuple.'],
        'React': ['What are React Hooks?', 'Explain the Virtual DOM.', 'Difference between functional and class components.'],
        'SQL': ['Explain JOINS in SQL.', 'What is normalization?', 'Difference between WHERE and HAVING.'],
        'Docker': ['What is a Docker container?', 'Difference between image and container.', 'What is Docker Compose?'],
        'JavaScript': ['Explain closures in JS.', 'Difference between let, const, and var.', 'What is an event loop?']
    }
    
    for kw, q_list in tech_keywords.items():
        if kw.lower() in text.lower():
            questions.append({
                'type': 'Technical',
                'topic': kw,
                'question': random.choice(q_list)
            })
            
    # Behavioral Questions
    behavioral_qs = [
        "Tell me about a time you faced a major challenge at work and how you handled it.",
        "Describe a situation where you had to work with a difficult team member.",
        "Tell me about a project you're most proud of and why.",
        "How do you handle tight deadlines or high-pressure situations?",
        "Describe a time you showed leadership even if you weren't in a leadership role."
    ]
    
    selected_behavioral = random.sample(behavioral_qs, 2)
    for q in selected_behavioral:
        questions.append({
            'type': 'Behavioral',
            'topic': 'Soft Skills',
            'question': q
        })
        
    return questions

def evaluate_answer(answer, context):
    """
    Simple evaluation of an interview answer (Confidence, Clarity, Relevance).
    """
    # In a real app, this would use an LLM. Here we use heuristics.
    words = answer.split()
    length_score = min(100, len(words) * 2) 
    
    clarity = 70 if len(words) > 20 else 40
    relevance = 80 if any(w in answer.lower() for w in ['result', 'achieved', 'because', 'specific']) else 50
    confidence = 90 if not any(w in answer.lower() for w in ['maybe', 'um', 'uh', 'i think']) else 60
    
    return {
        'clarity': clarity,
        'relevance': relevance,
        'confidence': confidence,
        'score': (clarity + relevance + confidence) / 3,
        'feedback': "Great structure!" if relevance > 70 else "Try to include more specific results using the STAR method."
    }

def get_heatmap_data(text):
    """
    Simulates a recruiter heatmap (absolute values for UI overlay).
    """
    # Sections to highlight: Top (Contact), Skills, Experience Headers, Metrics
    lines = text.split('\n')
    heatmap = []
    
    for i, line in enumerate(lines[:100]): # Sample first 100 lines
        intensity = 0
        if i < 5: intensity = 0.9 # Name/Contact
        if any(h in line.lower() for h in ['experience', 'skills', 'education']): intensity = 0.8
        if any(c in line for c in ['%', '$', '20']): intensity = 0.7
        
        heatmap.append({
            'line': i,
            'intensity': intensity
        })
        
    return heatmap
