document.addEventListener('DOMContentLoaded', function() {
    initDarkMode();
    initFileUpload();
    initSectionToggles();
    initCopyButtons();
    initCircularProgress();
});

function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Animation with safety check
            try {
                const icon = this.querySelector('span:not([style*="display: none"])');
                if (icon && typeof icon.animate === 'function') {
                    icon.animate([
                        { transform: 'scale(1)', opacity: 1 },
                        { transform: 'scale(0.5)', opacity: 0 },
                        { transform: 'scale(1.2)', opacity: 0.5 },
                        { transform: 'scale(1)', opacity: 1 }
                    ], { duration: 400 });
                }
            } catch (e) {
                console.warn('Animation failed but skipping gracefully', e);
            }
        });
    }
}

function initFileUpload() {
    const fileInput = document.getElementById('resume');
    const fileLabel = document.querySelector('.file-label');
    const fileText = document.querySelector('.file-text');
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                const fileName = e.target.files[0].name;
                fileText.textContent = `Selected: ${fileName}`;
                fileLabel.style.borderColor = 'var(--success-color)';
                fileLabel.style.background = 'rgba(67, 233, 123, 0.1)';
            } else {
                fileText.textContent = 'Choose PDF file or drag here';
                fileLabel.style.borderColor = 'var(--primary-color)';
                fileLabel.style.background = 'var(--bg-secondary)';
            }
        });
        
        fileLabel.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileLabel.style.borderColor = 'var(--secondary-color)';
            fileLabel.style.background = 'rgba(102, 126, 234, 0.1)';
        });
        
        fileLabel.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileLabel.style.borderColor = 'var(--primary-color)';
            fileLabel.style.background = 'var(--bg-secondary)';
        });
        
        fileLabel.addEventListener('drop', function(e) {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type === 'application/pdf') {
                fileInput.files = files;
                const fileName = files[0].name;
                fileText.textContent = `Selected: ${fileName}`;
                fileLabel.style.borderColor = 'var(--success-color)';
                fileLabel.style.background = 'rgba(67, 233, 123, 0.1)';
            } else {
                alert('Please upload a PDF file');
                fileLabel.style.borderColor = 'var(--error-color)';
            }
        });
    }
}

function initSectionToggles() {
    const sectionHeaders = document.querySelectorAll('.section-header');
    
    sectionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const sectionName = this.getAttribute('data-section');
            const content = document.getElementById(`section-${sectionName}`);
            
            this.classList.toggle('active');
            content.classList.toggle('active');
            
            if (content.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
            } else {
                content.style.maxHeight = '0';
            }
        });
    });
}

function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.btn-copy');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.textContent;
                this.textContent = '✓';
                this.style.background = 'var(--success-color)';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.background = 'var(--primary-color)';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                alert('Failed to copy to clipboard');
            });
        });
    });
}

function initCircularProgress() {
    const progressElement = document.querySelector('.circular-progress');
    
    if (progressElement) {
        const score = parseInt(progressElement.getAttribute('data-score'));
        const circle = document.querySelector('.progress-ring-circle');
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        
        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = circumference;
        
        const svgElement = document.querySelector('.progress-ring');
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'progressGradient');
        gradient.setAttribute('x1', '0%');
        gradient.setAttribute('y1', '0%');
        gradient.setAttribute('x2', '100%');
        gradient.setAttribute('y2', '100%');
        
        const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop1.setAttribute('offset', '0%');
        stop1.setAttribute('style', 'stop-color:#667eea;stop-opacity:1');
        
        const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop2.setAttribute('offset', '100%');
        stop2.setAttribute('style', 'stop-color:#764ba2;stop-opacity:1');
        
        gradient.appendChild(stop1);
        gradient.appendChild(stop2);
        defs.appendChild(gradient);
        svgElement.insertBefore(defs, svgElement.firstChild);
        
        setTimeout(() => {
            const offset = circumference - (score / 100) * circumference;
            circle.style.strokeDashoffset = offset;
        }, 100);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.upload-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('resume');
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select a PDF file to upload');
                return false;
            }
            
            const file = fileInput.files[0];
            if (file.type !== 'application/pdf') {
                e.preventDefault();
                alert('Only PDF files are allowed');
                return false;
            }
            
            const maxSize = 16 * 1024 * 1024;
            if (file.size > maxSize) {
                e.preventDefault();
                alert('File size must be less than 16MB');
                return false;
            }
            
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="btn-icon">⏳</span> Analyzing...';
            }
        });
    }
});
