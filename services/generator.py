import json

def get_role_optimizations(resume_data, role):
    """
    Simulates AI optimization for specific roles.
    """
    optimizations = {
        'Software Developer': {
            'priority': 'technical',
            'top_skills': ['algorithms', 'system design', 'cloud'],
            'summary_addition': 'Highly focused on scalable architecture and code quality.'
        },
        'Data Analyst': {
            'priority': 'analytical',
            'top_skills': ['visualization', 'statistics', 'insight'],
            'summary_addition': 'Passionate about translating complex data into actionable business insights.'
        },
        'Internship': {
            'priority': 'learning',
            'top_skills': ['foundation', 'communication', 'dedication'],
            'summary_addition': 'Quick learner eager to contribute to real-world industrial projects.'
        }
    }
    
    return optimizations.get(role, optimizations['Software Developer'])

def generate_portfolio_html(resume_data):
    """
    Generates a premium personal portfolio HTML based on resume data.
    """
    name = resume_data.get('full_name', 'Professional')
    email = resume_data.get('email', '')
    phone = resume_data.get('phone', '')
    summary = resume_data.get('summary', 'Passionate professional.')
    skills = resume_data.get('skills', [])
    experience_list = resume_data.get('experience', [])
    education_list = resume_data.get('education', [])
    projects_list = resume_data.get('projects', [])

    def format_list(items):
        if not items: return "<p style='color:#a3a3a3'>Not specified.</p>"
        return "".join([f"<div class='timeline-item'><p>{item}</p></div>" for item in items if len(item.strip()) > 3])
    
    skills_html = "".join([f'<span class="skill-tag">{s.strip()}</span>' for s in skills if s.strip()]) if skills else "<p>No technical skills parsed.</p>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | Developer Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --surface: #18181b;
            --primary: #6366f1;
            --secondary: #a855f7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #27272a;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }}
        body {{ background: var(--bg); color: var(--text-main); line-height: 1.6; padding-bottom: 4rem; overflow-x: hidden; }}
        
        .nav {{ position: fixed; top: 0; width: 100%; background: rgba(9, 9, 11, 0.8); backdrop-filter: blur(10px); padding: 1.5rem 5%; z-index: 100; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
        .nav-logo {{ font-weight: 800; font-size: 1.4rem; background: linear-gradient(90deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .nav-links a {{ color: var(--text-main); text-decoration: none; margin-left: 2rem; font-size: 0.95rem; font-weight: 600; transition: color 0.3s; }}
        .nav-links a:hover {{ color: var(--primary); }}
        
        .hero {{ padding: 12rem 5% 5rem; max-width: 1200px; margin: 0 auto; min-height: 80vh; display: flex; flex-direction: column; justify-content: center; }}
        .hero h1 {{ font-size: clamp(3rem, 5vw, 5rem); font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; letter-spacing: -0.02em; }}
        .hero h1 span {{ background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .hero p {{ font-size: 1.25rem; color: var(--text-muted); max-width: 700px; margin-bottom: 3rem; line-height: 1.8; }}
        .hero-contact {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
        
        .btn {{ padding: 0.8rem 2.2rem; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 1rem; transition: transform 0.3s, box-shadow 0.3s; }}
        .btn-primary {{ background: var(--primary); color: white; box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }}
        .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 0 30px rgba(99, 102, 241, 0.5); }}
        .btn-outline {{ border: 1px solid var(--border); color: var(--text-main); }}
        .btn-outline:hover {{ border-color: var(--primary); color: var(--primary); }}

        .section {{ padding: 6rem 5%; max-width: 1000px; margin: 0 auto; }}
        .section-title {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 3.5rem; display: flex; align-items: center; gap: 1rem; }}
        .section-title::after {{ content: ''; height: 1px; background: var(--border); flex: 1; }}

        .skills-grid {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
        .skill-tag {{ background: var(--surface); border: 1px solid var(--border); padding: 0.8rem 1.8rem; border-radius: 50px; color: var(--text-main); font-weight: 600; font-size: 0.95rem; transition: transform 0.3s, border-color 0.3s, color 0.3s; }}
        .skill-tag:hover {{ transform: translateY(-3px); border-color: var(--primary); color: var(--primary); }}

        .timeline {{ border-left: 2px solid var(--border); padding-left: 2.5rem; margin-left: 1rem; }}
        .timeline-item {{ position: relative; margin-bottom: 3.5rem; background: var(--surface); border: 1px solid var(--border); padding: 2rem; border-radius: 12px; }}
        .timeline-item::before {{ content: ''; position: absolute; left: -2.9rem; top: 2rem; width: 14px; height: 14px; border-radius: 50%; background: var(--primary); box-shadow: 0 0 15px var(--primary); }}
        .timeline-item p {{ white-space: pre-wrap; color: var(--text-muted); line-height: 1.8; font-size: 1.05rem; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-logo">{name}</div>
        <div class="nav-links">
            <a href="#about">About</a>
            <a href="#skills">Skills</a>
            <a href="#experience">Experience</a>
            <a href="#projects">Projects</a>
            <a href="#education">Education</a>
        </div>
    </nav>

    <header class="hero" id="about">
        <h1>Hi, I'm <br><span>{name}</span>.</h1>
        <p>{summary}</p>
        <div class="hero-contact">
            <a href="mailto:{email}" class="btn btn-primary">Email Me</a>
            <a href="tel:{phone}" class="btn btn-outline" style="{'display:none' if not phone else ''}">Call Me</a>
        </div>
    </header>

    <section class="section" id="skills">
        <h2 class="section-title">Technical Expertise</h2>
        <div class="skills-grid">
            {skills_html}
        </div>
    </section>

    <section class="section" id="experience">
        <h2 class="section-title">Work Experience</h2>
        <div class="timeline">
            {format_list(experience_list)}
        </div>
    </section>

    <section class="section" id="projects">
        <h2 class="section-title">Featured Projects</h2>
        <div class="timeline">
            {format_list(projects_list)}
        </div>
    </section>

    <section class="section" id="education">
        <h2 class="section-title">Education</h2>
        <div class="timeline">
            {format_list(education_list)}
        </div>
    </section>
</body>
</html>"""
    return html
