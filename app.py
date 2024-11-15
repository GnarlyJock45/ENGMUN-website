# app.py
from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)


# Load committee data once when the app starts
def load_committees():
    data_file = os.path.join(app.root_path, 'data', 'committees.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    committees = {committee['id']: committee for committee in data.get('committees', [])}
    return committees

committees = load_committees()

# Function to load team members data
def load_team_members():
    data_file = os.path.join(app.root_path, 'data', 'team_members.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        team_members_dict = {member['id']: member for member in data.get('team_members', [])}
        return team_members_dict
    except FileNotFoundError:
        print(f"Error: {data_file} not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}

team_members = load_team_members()


@app.route('/')
def home():
    return render_template('home.html', title='Home', committees=committees)

@app.route('/concert')
def concert():
    return render_template('concert.html', title='Concert Details')

@app.route('/team')
def team():
    return render_template('team.html', title='Our Team', team_members=team_members)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')


# @app.route('/committee/<committee_id>')
# def committee(committee_id):
#     # Fetch committee data based on committee_id
#     committee_data = {
#         'name': 'DISEC',
#         'full_name': 'Disarmament and International Security',
#         'level': 'Beginner',
#         'delegates': 30,
#         'experience': 'Not Required',
#         'description': 'Detailed description...',
#         'topics': [
#             {
#                 'title': 'Topic 1',
#                 'description': 'Description of topic 1...'
#             },
#             # More topics...
#         ],
#         'resources': [
#             {
#                 'title': 'Study Guide',
#                 'description': 'Complete guide for delegates',
#                 'url': '#'
#             },
#             # More resources...
#         ]
#     }
#     return render_template('committee.html', committee=committee_data)

@app.route('/committee/<committee_id>')
def committee(committee_id):
    committee_data = committees.get(committee_id)
    if not committee_data:
        abort(404)  # Committee not found
    return render_template('committee.html', committee=committee_data)


if __name__ == '__main__':
    app.run(debug=True,port=5001)
