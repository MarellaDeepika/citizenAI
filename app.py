from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from clean_chat import get_ai_response
from models import db, User, Concern, Vote, Comment
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'citizen_ai.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Check if user is logged in
def login_required():
    return 'user_id' in session

# Home page - requires login
@app.route('/')
def home():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('index.html')

# About page - requires login
@app.route('/about')
def about():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('about.html')

# Chat page - requires login
@app.route('/chat')
def chat():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('chat.html')

# Chat API endpoint - requires login
@app.route('/chat', methods=['POST'])
def chat_api():
    if not login_required():
        return jsonify({'error': 'Authentication required'}), 401
    
    user_input = request.form.get('message')

    try:
        # 1. Generate AI reply
        ai_reply = get_ai_response(user_input)
    except Exception as e:
        # Return error message if AI service is unavailable
        return jsonify({'error': 'AI service is temporarily unavailable. Please try again later.'}), 503

    # 2. Simple sentiment (basic implementation)
    sentiment = "neutral"
    if any(word in user_input.lower() for word in ['angry', 'frustrated', 'upset', 'hate', 'terrible', 'awful']):
        sentiment = "negative"
    elif any(word in user_input.lower() for word in ['happy', 'great', 'excellent', 'love', 'amazing', 'wonderful']):
        sentiment = "positive"

    return jsonify({'reply': ai_reply, 'sentiment': sentiment})

# Dashboard page - requires login
# Login page - public access
@app.route('/login')
def login():
    return render_template('login.html')

# Register page - public access
@app.route('/register')
def register():
    return render_template('register.html')

# Login POST
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Simple authentication (you can improve this)
    if email and password:
        session['user_id'] = email  # Store user in session
        flash('Login successful!')
        return redirect(url_for('home'))
    else:
        flash('Please enter both email and password.')
        return redirect(url_for('login'))

# Register POST
@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    
    if email and password and name:
        session['user_id'] = email  # Auto-login after registration
        flash('Registration successful!')
        return redirect(url_for('home'))
    else:
        flash('Please fill in all fields.')
        return redirect(url_for('register'))

# Report Concerns page - requires login
@app.route('/concerns')
def concerns():
    if not login_required():
        return redirect(url_for('login'))
    
    # Try to get concerns from database, fall back to sample data if database issues
    try:
        concerns_list = Concern.query.order_by(Concern.created_at.desc()).all()
        
        # Convert to dictionary format for template
        concerns_data = []
        for concern in concerns_list:
            concern_data = {
                'id': concern.id,
                'title': concern.title,
                'description': concern.description,
                'location': getattr(concern, 'location', 'Location not specified'),
                'email': getattr(concern, 'email', 'No email provided'),
                'priority': getattr(concern, 'priority', 'medium'),
                'upvotes': concern.upvotes,
                'downvotes': concern.downvotes,
                'created_at': concern.created_at.strftime('%Y-%m-%d %H:%M'),
                'comments': [{'user': comment.user.email.split('@')[0], 'text': comment.text} 
                            for comment in concern.comments]
            }
            concerns_data.append(concern_data)
    
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to sample data if database has issues
        concerns_data = [
            {
                'id': 1,
                'title': 'Road Maintenance on Main Street',
                'description': 'Multiple dangerous potholes causing serious traffic issues and vehicle damage. This is an urgent safety concern that needs immediate attention.',
                'location': 'Main Street between 1st Ave and 3rd Ave',
                'email': 'citizen@email.com',
                'priority': 'high',
                'upvotes': 25,
                'downvotes': 3,
                'created_at': '2025-06-28 10:30',
                'comments': [
                    {'user': 'John D.', 'text': 'This is a serious safety issue! I saw two cars get flat tires yesterday.'},
                    {'user': 'Mary S.', 'text': 'I damaged my tire here yesterday and had to pay $200 for repairs.'},
                    {'user': 'City_Worker', 'text': 'We have scheduled this for emergency repair next week. Thank you for reporting.'}
                ]
            },
            {
                'id': 2,
                'title': 'Bus Schedule Delays',
                'description': 'Route 15 consistently running 10-15 minutes late during peak hours, causing inconvenience for daily commuters.',
                'location': 'Central Bus Terminal and University Campus',
                'email': 'commuter@email.com',
                'priority': 'medium',
                'upvotes': 18,
                'downvotes': 7,
                'created_at': '2025-06-28 09:15',
                'comments': [
                    {'user': 'Alex K.', 'text': 'Makes me late for work every day. Please fix the scheduling.'},
                    {'user': 'Student_Sarah', 'text': 'Missing classes because of these delays. Very frustrating!'}
                ]
            },
            {
                'id': 3,
                'title': 'Park Bench Replacement',
                'description': 'Some old park benches could be replaced with newer, more comfortable ones to enhance the park experience.',
                'location': 'Central Park - Main Walking Path',
                'email': 'parkuser@email.com',
                'priority': 'low',
                'upvotes': 8,
                'downvotes': 2,
                'created_at': '2025-06-28 08:45',
                'comments': [
                    {'user': 'Nature_Lover', 'text': 'The current benches are still functional but new ones would be nice.'},
                ]
            }
        ]
    
    return render_template('concerns.html', concerns=concerns_data)

# Submit new concern
@app.route('/submit_concern', methods=['POST'])
def submit_concern():
    if not login_required():
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get current user
    user_email = session['user_id']
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        # Create user if doesn't exist (for backward compatibility)
        user = User(email=user_email, password='temp')
        db.session.add(user)
        db.session.commit()
    
    title = request.json.get('title')
    description = request.json.get('description')
    location = request.json.get('location')
    email = request.json.get('email')
    priority = request.json.get('priority', 'medium')
    
    if not all([title, description, location, email]):
        return jsonify({'error': 'All fields are required'}), 400
    
    # Create new concern
    concern = Concern(
        title=title,
        description=description,
        location=location,
        email=email,
        priority=priority,
        user_id=user.id
    )
    
    db.session.add(concern)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'concern': {
            'id': concern.id,
            'title': concern.title,
            'description': concern.description,
            'location': concern.location,
            'email': concern.email,
            'priority': concern.priority,
            'upvotes': 0,
            'downvotes': 0,
            'comments': []
        }
    })

# Vote on concern
@app.route('/vote', methods=['POST'])
def vote():
    if not login_required():
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get current user
    user_email = session['user_id']
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        # Create user if doesn't exist
        user = User(email=user_email, password='temp')
        db.session.add(user)
        db.session.commit()
    
    concern_id = request.json.get('concern_id')
    vote_type = request.json.get('vote_type')  # 'up' or 'down'
    
    if not concern_id or vote_type not in ['up', 'down']:
        return jsonify({'error': 'Invalid parameters'}), 400
    
    # Check if user already voted on this concern
    existing_vote = Vote.query.filter_by(user_id=user.id, concern_id=concern_id).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # User clicked same vote type - remove vote
            db.session.delete(existing_vote)
            db.session.commit()
            action = 'removed'
        else:
            # User changed vote type - update vote
            existing_vote.vote_type = vote_type
            db.session.commit()
            action = 'changed'
    else:
        # New vote
        new_vote = Vote(user_id=user.id, concern_id=concern_id, vote_type=vote_type)
        db.session.add(new_vote)
        db.session.commit()
        action = 'added'
    
    # Get updated vote counts
    concern = Concern.query.get(concern_id)
    return jsonify({
        'success': True,
        'action': action,
        'upvotes': concern.upvotes,
        'downvotes': concern.downvotes
    })

# Add comment to concern
@app.route('/add_comment', methods=['POST'])
def add_comment():
    if not login_required():
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get current user
    user_email = session['user_id']
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        # Create user if doesn't exist
        user = User(email=user_email, password='temp')
        db.session.add(user)
        db.session.commit()
    
    concern_id = request.json.get('concern_id')
    comment_text = request.json.get('comment')
    
    if not concern_id or not comment_text:
        return jsonify({'error': 'Invalid parameters'}), 400
    
    # Create new comment
    comment = Comment(
        text=comment_text,
        user_id=user.id,
        concern_id=concern_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'comment': {
            'user': user.email.split('@')[0],
            'text': comment_text
        }
    })

# Trending Issues page - requires login  
@app.route('/trending')
def trending():
    if not login_required():
        return redirect(url_for('login'))
    
    # Sample trending issues with real-time AI-generated responses
    trending_issues_data = [
        {
            'title': 'Road Infrastructure Problems',
            'origin': 'Downtown District, Industrial Zone',
            'reports': 23,
            'trend': 'rising'
        },
        {
            'title': 'Public Transportation Efficiency',
            'origin': 'Central Business District, University Area',
            'reports': 18,
            'trend': 'stable'
        },
        {
            'title': 'Public Safety and Lighting',
            'origin': 'Residential Areas, Central Park District',
            'reports': 15,
            'trend': 'decreasing'
        }
    ]
    
    # Generate AI responses for each trending issue
    trending_issues = []
    for issue in trending_issues_data:
        try:
            # Create a prompt for a concise, professional response about the issue
            prompt = f"Provide a concise, professional response (150-200 words) about '{issue['title']}' reported in {issue['origin']}. Focus on actionable solutions and municipal response options."
            ai_response = get_ai_response(prompt)
            
            issue['ai_response'] = ai_response
            trending_issues.append(issue)
        except Exception as e:
            # If AI response fails, skip the AI response for this issue
            print(f"Failed to generate AI response for {issue['title']}: {e}")
            issue['ai_response'] = "AI response temporarily unavailable for this issue."
            trending_issues.append(issue)
    
    return render_template('trending.html', issues=trending_issues)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
