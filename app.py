from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for students
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    batch = db.Column(db.String(50), nullable=False)
    academic_performance = db.Column(db.Float, nullable=False)
    consistency = db.Column(db.Float, nullable=False)
    core_excellence = db.Column(db.Float, nullable=False)
    hackathon_participation = db.Column(db.Float, nullable=False)
    paper_presentations = db.Column(db.Float, nullable=False)
    contributions = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.calculate_score()
        }

    def calculate_score(self):
        # Simple scoring based on weighted factors
        weights = {
            'academic_performance': 0.3,
            'consistency': 0.2,
            'core_excellence': 0.2,
            'hackathon_participation': 0.1,
            'paper_presentations': 0.1,
            'contributions': 0.1
        }
        score = (
            weights['academic_performance'] * self.academic_performance +
            weights['consistency'] * self.consistency +
            weights['core_excellence'] * self.core_excellence +
            weights['hackathon_participation'] * self.hackathon_participation +
            weights['paper_presentations'] * self.paper_presentations +
            weights['contributions'] * self.contributions
        )
        return score

@app.before_first_request
def create_tables():
    db.create_all()  # Create database tables if they don't exist

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(
        name=data['name'],
        batch=data['batch'],
        academic_performance=data['academicPerformance'],
        consistency=data['consistency'],
        core_excellence=data['coreExcellence'],
        hackathon_participation=data['hackathonParticipation'],
        paper_presentations=data['paperPresentations'],
        contributions=data['contributions']
    )
    db.session.add(new_student)
    db.session.commit()  # Commit the new student to the database
    return jsonify({"message": "Student added successfully!"}), 201

@app.route('/api/students/top', methods=['GET'])
def get_top_students():
    students = Student.query.all()  # Query all students from the database
    student_scores = [student.to_dict() for student in students]
    
    # Sort by score and get top 3 students
    top_students = sorted(student_scores, key=lambda x: x['score'], reverse=True)[:3]
    return jsonify(top_students)  # Return the top 3 students as JSON

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
