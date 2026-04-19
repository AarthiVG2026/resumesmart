def get_copilot_response(user_query, analysis_context):
    """
    Career Copilot logic to handle user queries based on their resume analysis.
    """
    query = user_query.lower()
    ats_score = analysis_context.get('ats_score', 0)
    missing_skills = analysis_context.get('missing_skills', [])
    
    if 'how' in query and 'score' in query:
        return f"Your current ATS score is {ats_score}/100. You can improve it by adding these skills: {', '.join(missing_skills[:3])}."
    
    if 'skill' in query or 'missing' in query or 'include' in query or 'add' in query or 'improve' in query:
        if missing_skills:
            return f"I've identified {len(missing_skills)} missing skills. Top 3 to add: {', '.join(missing_skills[:3])}. Getting familiar with these will easily boost your ATS score!"
        return "Your skill section is looking solid compared to the standard requirements! Just make sure you are clearly mentioning your impact."
    
    if 'interview' in query:
        return "You can practice in our Interview Simulator! I recommend focusing on the Behavioral questions first to build confidence."
    
    if 'portfolio' in query:
        return "I can generate a professional portfolio for you! Click the 'Export Portfolio' button in the dashboard to download it as a ready-to-deploy HTML file."

    if 'job' in query or 'apply' in query:
        return "Based on your profile, you're a strong match for 'Junior Software Engineer' roles. Try searching for these on LinkedIn or Indeed."

    if ats_score < 50:
        return f"Based on your score of {ats_score}/100, the best way to improve right now is to ensure you add more quantifiable metrics (%, $) and ensure your core skills like {missing_skills[0] if missing_skills else 'Java'} are explicitly listed."
    elif ats_score < 80:
        return f"You have a solid foundation with {ats_score}/100! To cross the 80+ threshold, try exporting the AI Portfolio and make sure your bullet points follow the STAR method."
    else:
        return f"Your resume is extremely strong ({ats_score}/100). Focus on interview prep! Click 'Open Resume Builder' if you want to try different templates, or practice with the Simulator."
