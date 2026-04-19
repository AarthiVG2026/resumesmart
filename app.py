from flask import Flask, render_template, request, session, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from io import BytesIO

# Legacy and Shared Imports
from analyzer import ROLE_SKILLS as LEGACY_ROLE_SKILLS 

# Premium Service Imports
from services.parser import extract_text_from_pdf, split_into_sections
from services.analyzer import deep_analyze
from services.simulator import generate_interview_questions, evaluate_answer, get_heatmap_data
from services.generator import generate_portfolio_html, get_role_optimizations
from services.security import scan_job_description
from services.copilot import get_copilot_response
from resume_generator import generate_pdf_resume, generate_analysis_report

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'premium-ai-career-secret-2024')

UPLOAD_FOLDER = 'uploads'
ANALYSIS_FOLDER = 'analysis_cache'
ALLOWED_EXTENSIONS = {'pdf'}

for folder in [UPLOAD_FOLDER, ANALYSIS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def log_request_info():
    if request.method == 'POST':
        print(f"--- POST Request to {request.path} ---")

@app.route('/')
def index():
    return render_template('index.html', roles=list(LEGACY_ROLE_SKILLS.keys()))

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return render_template('index.html', error='No file uploaded')
    
    file = request.files['resume']
    if file.filename == '' or not allowed_file(file.filename):
        return render_template('index.html', error='Invalid file format')
    
    try:
        # 1. Parse & Deep Analyze
        text = extract_text_from_pdf(file)
        target_role = request.form.get('target_role')
        jd_text = request.form.get('job_keywords', '')
        
        # Security Scan for Job Description
        security_results = scan_job_description(jd_text) if jd_text else None
        
        # Advanced Analysis
        from analyzer import analyze_resume as legacy_analyze # Keep for basic metrics
        basic_metrics = legacy_analyze(text, jd_text, target_role)
        
        deep_metrics = deep_analyze(text, target_role)
        
        # Merge results
        analysis_result = {**basic_metrics, **deep_metrics}
        analysis_result['security_scan'] = security_results
        analysis_result['full_text'] = text # For simulation
        
        # 2. Generate Intelligent Suggestions/Roadmap
        analysis_result['roadmap'] = [
            "Complete a project in " + (analysis_result['missing_skills'][0] if analysis_result['missing_skills'] else "General Tech"),
            "Update resume summary using the STAR method suggestions provided.",
            "Take an advanced course on " + (analysis_result['skills_found'][0] if analysis_result['skills_found'] else "Industry Standards")
        ]
        
        # 3. Cache for session
        analysis_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        cache_path = os.path.join(ANALYSIS_FOLDER, f'{analysis_id}.json')
        with open(cache_path, 'w') as f:
            # We don't save the full text to cache to keep it small, but you can if needed
            json.dump(analysis_result, f)
            
        session['analysis_id'] = analysis_id
        session['current_analysis'] = analysis_result # Store in session for copilot
        
        return render_template('result.html', result=analysis_result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template('index.html', error=f'Error: {str(e)}')

@app.route('/interview/generate')
def interview_generate():
    analysis = session.get('current_analysis')
    if not analysis: return redirect('/')
    
    questions = generate_interview_questions(analysis['full_text'], analysis.get('target_role'))
    return jsonify(questions)

@app.route('/interview/evaluate', methods=['POST'])
def interview_evaluate():
    data = request.json
    evaluation = evaluate_answer(data.get('answer'), data.get('question'))
    return jsonify(evaluation)

@app.route('/copilot/chat', methods=['POST'])
def copilot_chat():
    data = request.json
    analysis = session.get('current_analysis', {})
    response = get_copilot_response(data.get('message'), analysis)
    return jsonify({'response': response})

@app.route('/download_report')
def download_report():
    analysis = session.get('current_analysis')
    if not analysis:
        return "Analysis not found", 404
        
    buffer = generate_analysis_report(analysis)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'resumesmart_report_{datetime.now().strftime("%Y%m%d")}.pdf',
        mimetype='application/pdf'
    )

@app.route('/export/portfolio')
def export_portfolio():
    analysis = session.get('current_analysis')
    if not analysis: return "Analysis not found", 404
    
    # Map analysis to full portfolio data
    resume_data = {
        'full_name': analysis.get('full_name', 'Professional'),
        'email': analysis.get('email', 'not-found@example.com'),
        'phone': analysis.get('phone', ''),
        'summary': analysis.get('improved_bullets', ['Professional Portfolio'])[0],
        'skills': analysis.get('skills_found', []),
        'experience': analysis.get('sections', {}).get('experience', []),
        'education': analysis.get('sections', {}).get('education', []),
        'projects': analysis.get('sections', {}).get('projects', [])
    }
    
    html_content = generate_portfolio_html(resume_data)
    
    buffer = BytesIO()
    buffer.write(html_content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='my_portfolio.html',
        mimetype='text/html'
    )

@app.route('/builder')
def builder():
    return render_template('builder.html')

@app.route('/templates')
def templates():
    return render_template('templates.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    try:
        template_id = request.form.get('template_id', 'modern')
        buffer = generate_pdf_resume(request.form, template_id)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'resume_tailored_{datetime.now().strftime("%Y%m%d")}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
