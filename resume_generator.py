from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from io import BytesIO

def generate_pdf_resume(data, template_id='modern'):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()

    # Define common styles
    name_style = ParagraphStyle('NameStyle', parent=styles['Heading1'], fontSize=24, spaceAfter=4)
    job_title_style = ParagraphStyle('JobTitle', parent=styles['Normal'], fontSize=14, textColor=colors.grey, spaceAfter=12)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=16, spaceBefore=12, spaceAfter=6, borderPadding=2, borderThickness=1, borderColor=colors.grey, borderStroke=1)
    content_style = styles['Normal']

    # Template-specific adjustments
    if template_id == 'modern':
        name_style.textColor = colors.HexColor('#667eea')
        heading_style.textColor = colors.HexColor('#764ba2')
        heading_style.borderWidth = 0
        heading_style.backColor = colors.HexColor('#f8f9ff')
    elif template_id == 'tech':
        name_style.textColor = colors.HexColor('#43e97b')
        name_style.fontName = 'Helvetica-Bold'
        heading_style.textColor = colors.HexColor('#43e97b')
        # Dark theme simulation is harder in basic ReportLab, but we can change colors
    elif template_id == 'creative':
        name_style.fontSize = 32
        name_style.alignment = 1 # Center
    
    # 1. Header
    story.append(Paragraph(data.get('full_name', 'Your Name').upper(), name_style))
    story.append(Paragraph(data.get('email', '') + " | " + data.get('phone', '') + " | " + data.get('location', ''), styles['Normal']))
    if data.get('links'):
        story.append(Paragraph(data.get('links', ''), styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # 2. Summary
    if data.get('summary'):
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        story.append(Paragraph(data.get('summary', ''), content_style))
        story.append(Spacer(1, 0.1 * inch))

    # 3. Experience
    exp_titles = data.getlist('exp_title[]')
    exp_companies = data.getlist('exp_company[]')
    exp_durations = data.getlist('exp_duration[]')
    exp_descs = data.getlist('exp_desc[]')

    if exp_titles:
        story.append(Paragraph("WORK EXPERIENCE", heading_style))
        for i in range(len(exp_titles)):
            story.append(Paragraph(f"<b>{exp_titles[i]}</b>", styles['Normal']))
            story.append(Paragraph(f"<i>{exp_companies[i]} | {exp_durations[i]}</i>", styles['Normal']))
            story.append(Paragraph(exp_descs[i], content_style))
            story.append(Spacer(1, 0.1 * inch))

    # 4. Education
    edu_degrees = data.getlist('edu_degree[]')
    edu_schools = data.getlist('edu_school[]')
    edu_years = data.getlist('edu_year[]')

    if edu_degrees:
        story.append(Paragraph("EDUCATION", heading_style))
        for i in range(len(edu_degrees)):
            story.append(Paragraph(f"<b>{edu_degrees[i]}</b>", styles['Normal']))
            story.append(Paragraph(f"{edu_schools[i]} | {edu_years[i]}", styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

    # 5. Skills
    if data.get('skills'):
        story.append(Paragraph("SKILLS", heading_style))
        story.append(Paragraph(data.get('skills', ''), content_style))

    # 6. Projects
    proj_titles = data.getlist('proj_title[]')
    proj_descs = data.getlist('proj_desc[]')

    if proj_titles:
        story.append(Paragraph("PROJECTS", heading_style))
        for i in range(len(proj_titles)):
            story.append(Paragraph(f"<b>{proj_titles[i]}</b>", styles['Normal']))
            story.append(Paragraph(proj_descs[i], content_style))
            story.append(Spacer(1, 0.1 * inch))

    try:
        doc.build(story)
    except Exception as e:
        # Fallback if building fails (e.g. invalid characters)
        print(f"PDF build error: {e}")
        story = [Paragraph("Error generating content. Please check for special characters.", styles['Heading1'])]
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_analysis_report(analysis):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    title_style = styles['Heading1']
    title_style.alignment = 1

    story.append(Paragraph("ResumeSmart Analysis Report", title_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"<b>ATS Master Score:</b> {analysis.get('ats_score', 0)} / 100", styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph(f"<b>Top Missing Skills:</b> {', '.join(analysis.get('missing_skills', [])[:5]) or 'None identified!'}", styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>Top Suggestions:</b>", styles['Heading3']))
    
    for sug in analysis.get('suggestions', [])[:4]:
        story.append(Paragraph(f"• <b>{sug['title']}:</b> {sug['description']}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
