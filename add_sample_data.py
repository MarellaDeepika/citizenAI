#!/usr/bin/env python3
"""
Add sample concerns and votes for testing the new features
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from app import app
from models import db, User, Concern, Vote, Comment

def add_sample_data():
    """Add sample concerns, votes, and comments for testing"""
    
    print("🧪 Adding sample data for testing voting and commenting features...")
    
    with app.app_context():
        try:
            # Get existing users
            users = User.query.all()
            if len(users) < 2:
                print("❌ Need at least 2 users to create sample data. Please register more users first.")
                return False
            
            sample_concerns = [
                {
                    "title": "Broken Street Lights on Main Street",
                    "description": "Several street lights have been out for weeks on Main Street between 5th and 8th Avenue. This creates safety concerns for pedestrians and drivers, especially during evening hours. The area has become poorly lit and potentially dangerous.",
                    "category": "Infrastructure",
                    "priority": "High"
                },
                {
                    "title": "Need More Public Transportation Routes",
                    "description": "The current bus routes don't adequately serve the east side of the city. Many residents have to walk over a mile to reach the nearest bus stop. Adding more routes would help reduce traffic congestion and provide better access to public transit.",
                    "category": "Transportation", 
                    "priority": "Medium"
                },
                {
                    "title": "Community Park Needs Maintenance",
                    "description": "Central Park playground equipment is becoming unsafe with rust and broken swings. The park also needs better landscaping and maintenance. Families with children are concerned about safety.",
                    "category": "Infrastructure",
                    "priority": "Medium"
                },
                {
                    "title": "Air Quality Issues Near Industrial Zone",
                    "description": "Residents living near the industrial district report poor air quality and frequent odors. This is affecting quality of life and potentially health. We need environmental monitoring and regulations.",
                    "category": "Environment",
                    "priority": "High"
                },
                {
                    "title": "Limited Healthcare Clinic Hours",
                    "description": "The local community health clinic only operates 3 days per week, creating access issues for residents who need medical care. Extended hours or additional staff would greatly help the community.",
                    "category": "Healthcare",
                    "priority": "Medium"
                }
            ]
            
            # Create sample concerns
            created_concerns = []
            for i, concern_data in enumerate(sample_concerns):
                # Check if concern already exists
                existing = Concern.query.filter_by(title=concern_data["title"]).first()
                if existing:
                    created_concerns.append(existing)
                    continue
                    
                concern = Concern(
                    user_id=users[i % len(users)].id,
                    title=concern_data["title"],
                    description=concern_data["description"],
                    category=concern_data["category"],
                    priority=concern_data["priority"],
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    upvotes=0,
                    downvotes=0,
                    view_count=random.randint(10, 100)
                )
                
                db.session.add(concern)
                created_concerns.append(concern)
                print(f"✅ Created concern: {concern_data['title']}")
            
            db.session.flush()  # Flush to get IDs
            
            # Add sample votes
            vote_count = 0
            for concern in created_concerns:
                # Randomly assign votes from different users
                num_votes = random.randint(3, 15)
                voters = random.sample(users, min(num_votes, len(users)))
                
                for voter in voters:
                    # Skip if vote already exists
                    existing_vote = Vote.query.filter_by(user_id=voter.id, concern_id=concern.id).first()
                    if existing_vote:
                        continue
                        
                    # Random vote type (more likely to be upvote for realistic data)
                    vote_type = 'upvote' if random.random() > 0.3 else 'downvote'
                    
                    vote = Vote(
                        user_id=voter.id,
                        concern_id=concern.id,
                        vote_type=vote_type
                    )
                    
                    db.session.add(vote)
                    
                    # Update concern vote counts
                    if vote_type == 'upvote':
                        concern.upvotes += 1
                    else:
                        concern.downvotes += 1
                    
                    vote_count += 1
            
            # Add sample comments
            sample_comments = [
                "I completely agree with this issue. It affects our daily lives.",
                "This has been a problem for months. Glad someone reported it.",
                "I live in this area and can confirm this is a serious concern.",
                "The city should prioritize this issue immediately.",
                "Has anyone contacted the local council about this?",
                "This problem is getting worse each day.",
                "I support this initiative. Count me in!",
                "We need community action on this matter.",
                "Similar issues exist in our neighborhood too.",
                "Thank you for bringing this to attention."
            ]
            
            comment_count = 0
            for concern in created_concerns[:3]:  # Add comments to first 3 concerns
                num_comments = random.randint(2, 5)
                commenters = random.sample(users, min(num_comments, len(users)))
                
                for commenter in commenters:
                    comment = Comment(
                        user_id=commenter.id,
                        concern_id=concern.id,
                        content=random.choice(sample_comments)
                    )
                    
                    db.session.add(comment)
                    comment_count += 1
            
            db.session.commit()
            
            print(f"✅ Sample data created successfully!")
            print(f"   - {len(created_concerns)} concerns")
            print(f"   - {vote_count} votes")
            print(f"   - {comment_count} comments")
            print(f"   - Ready for testing!")
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            db.session.rollback()
            return False
            
    return True

if __name__ == '__main__':
    print("🧪 CitizenAI Sample Data Generator")
    print("=" * 40)
    
    success = add_sample_data()
    
    if success:
        print("\n🎉 Sample data added! You can now test:")
        print("   ✅ Voting on concerns")
        print("   ✅ Commenting on issues")
        print("   ✅ Trending issues page")
        print("   ✅ Concern browsing and filtering")
        print("\nℹ️  Visit http://127.0.0.1:5000/concerns to start testing!")
    else:
        print("\n❌ Failed to add sample data. Please check the errors above.")
        sys.exit(1)
