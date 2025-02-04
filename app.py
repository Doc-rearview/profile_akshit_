from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy user data for login (replace with a database in production)
USERS = {
    "123": "123",
}

# Dummy data for skills and projects (replace with a database in production)
skills = []
projects = []
education = []
PROJECTS_UPLOAD_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], 'projects')
os.makedirs(PROJECTS_UPLOAD_FOLDER, exist_ok=True)


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def index():
    return render_template('index.html', skills=skills, projects=projects, education=education)

# Download CV route
@app.route('/download-cv')
def download_cv():
    cv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cv.pdf')
    if os.path.exists(cv_path):
        return send_file(cv_path, as_attachment=True)
    else:
        flash("CV not found!", "error")
        return redirect(url_for('index'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('profile_update'))
        else:
            flash("Invalid username or password!", "error")
    return render_template('index.html')

# Profile update route
@app.route('/profile', methods=['GET', 'POST'])
def profile_update():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle Education
        if 'add_education' in request.form:
            degree = request.form.get('degree')
            institution = request.form.get('institution')
            year = request.form.get('year')
            cgpa = request.form.get('cgpa')  # New field
            percentage = request.form.get('percentage')  # New field

            if degree and institution and year:
                education.append({
                    "degree": degree,
                    "institution": institution,
                    "year": year,
                    "cgpa": cgpa if cgpa else None,  
                    "percentage": percentage if percentage else None  
                })

        # Handle Profile Picture Upload
        if 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            if profile_pic and allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Handle CV Upload
        if 'cv_file' in request.files:
            cv_file = request.files['cv_file']
            if cv_file and allowed_file(cv_file.filename):
                filename = secure_filename(cv_file.filename)
                cv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Handle Skills
        skill_name = request.form.get('skill_name')
        skill_description = request.form.get('skill_description')
        skill_image = request.files.get('skill_image')

        if skill_name and skill_description:
            image_path = None
            if skill_image and allowed_file(skill_image.filename):
                filename = secure_filename(skill_image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                skill_image.save(image_path)

            skills.append({
                "name": skill_name,
                "description": skill_description,
                "image": image_path  
            })

        project_name = request.form.get('project_name')
        project_description = request.form.get('project_description')
        project_image = request.files.get('project_image')
        project_link = request.form.get('project_link', '#')

        if project_name and project_description:
            image_path = None
            if project_image and allowed_file(project_image.filename):
                # Save the image with the project name as the filename
                filename = secure_filename(f"{project_name}.{project_image.filename.rsplit('.', 1)[1].lower()}")
                image_path = os.path.join(PROJECTS_UPLOAD_FOLDER, filename)
                project_image.save(image_path)

            projects.append({
                "name": project_name,
                "description": project_description,
                "image": os.path.join('uploads/projects', filename) if image_path else None,
                "link": project_link
            })

        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile_update'))


    return render_template('profile_update.html', username=session['username'], skills=skills, projects=projects, education=education)

# Route to delete a skill
@app.route('/delete-skill/<int:skill_index>', methods=['POST'])
def delete_skill(skill_index):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 0 <= skill_index < len(skills):
        del skills[skill_index]
        flash("Skill deleted successfully!", "success")
    else:
        flash("Invalid skill index!", "error")

    return redirect(url_for('profile_update'))

# Route to delete a project
@app.route('/delete-project/<int:project_index>', methods=['POST'])
def delete_project(project_index):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 0 <= project_index < len(projects):
        del projects[project_index]
        flash("Project deleted successfully!", "success")
    else:
        flash("Invalid project index!", "error")

    return redirect(url_for('profile_update'))

# Route to delete education entry
@app.route('/delete-education/<int:edu_index>', methods=['POST'])
def delete_education(edu_index):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 0 <= edu_index < len(education):
        del education[edu_index]
        flash("Education entry deleted successfully!", "success")
    else:
        flash("Invalid education entry!", "error")

    return redirect(url_for('profile_update'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
