from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

# Database Models
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(200))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(200))
    link = db.Column(db.String(200))

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50))
    cgpa = db.Column(db.String(50))
    percentage = db.Column(db.String(50))

# Create the database tables
with app.app_context():
    db.create_all()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def index():
    skills = Skill.query.all()
    projects = Project.query.all()
    education = Education.query.all()
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
            course=request.form.get('Course')
            cgpa = request.form.get('cgpa')
            percentage = request.form.get('percentage')

            if degree and institution and year:
                new_education = Education(degree=degree, institution=institution, course=course, year=year, cgpa=cgpa, percentage=percentage)
                db.session.add(new_education)
                db.session.commit()
                flash("Education added successfully!", "success")

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

            new_skill = Skill(name=skill_name, description=skill_description, image=image_path)
            db.session.add(new_skill)
            db.session.commit()
            flash("Skill added successfully!", "success")

        # Handle Projects
        project_name = request.form.get('project_name')
        project_description = request.form.get('project_description')
        project_image = request.files.get('project_image')
        project_link = request.form.get('project_link', '#')

        if project_name and project_description:
            image_path = None
            if project_image and allowed_file(project_image.filename):
                filename = secure_filename(f"{project_name}.{project_image.filename.rsplit('.', 1)[1].lower()}")
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                project_image.save(image_path)

            new_project = Project(name=project_name, description=project_description, image=image_path, link=project_link)
            db.session.add(new_project)
            db.session.commit()
            flash("Project added successfully!", "success")

    skills = Skill.query.all()
    projects = Project.query.all()
    education = Education.query.all()
    return render_template('profile_update.html', username=session['username'], skills=skills, projects=projects, education=education)

# Route to delete a skill
@app.route('/delete-skill/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    skill = Skill.query.get_or_404(skill_id)
    if skill.image and os.path.exists(skill.image):
        os.remove(skill.image)  # Delete the associated image file
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted successfully!", "success")
    return redirect(url_for('profile_update'))

# Route to delete a project
@app.route('/delete-project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    project = Project.query.get_or_404(project_id)
    if project.image and os.path.exists(project.image):
        os.remove(project.image)  # Delete the associated image file
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for('profile_update'))

# Route to delete education entry
@app.route('/delete-education/<int:edu_id>', methods=['POST'])
def delete_education(edu_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    education = Education.query.get_or_404(edu_id)
    db.session.delete(education)
    db.session.commit()
    flash("Education entry deleted successfully!", "success")
    return redirect(url_for('profile_update'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
