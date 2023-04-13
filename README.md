# Socialfy: Social Music Sharing Platform
Socialfy is a full-stack consumer-social web application designed to enhance the social experience of Spotify users. The platform allows users to share music recommendations, create profiles featuring their favorite music, generate socially-curated playlists, and interact with other users' music tastes. Socialfy aims to provide a seamless user experience for connecting Spotify profiles and engaging with others' musical preferences.

View a Evaluation copy of the program [here](http://socialfy.rogersconnor.com).

## Table of Contents
- Features
- Getting Started
- Prerequisites
- Installation
- Usage
- License


Connect your Spotify account and automatically import your listening data
Share music recommendations with your peers
Create and customize your profile, showcasing your favorite albums and songs
Generate socially-curated playlists
Interact with other users' music recommendations and playlists
Discover trending songs and albums within the community
Getting Started

These instructions will guide you through setting up the project locally and assume you have correctly deployed elasticsearch prior.

## Prerequisites
Python
React JS 
Elasticsearch

## Installation
Clone the repository:
```git clone https://github.com/marcussevero/socialfy.git```

Change directory to socailfy/flask_apps/socialfy folder:
```cd <your-repo_dir>/socailfy/flask_apps/socialfy```

Install backend dependencies:

```pip install -r requirements.txt```

Install frontend dependencies,repeact for both applications:

```cd <your-repo_dir>/frontend/<landing/socialfy>```
```npm install```
```npm run build```

Configure .env Based on the .env_template Template

Return to <your-repo_dir>/socailfy/flask_apps/socialfy and run
```python app.py ```

Open your browser and navigate to http://localhost:5000 to access the application


## Usage
Connect your Spotify account to Socialfy
Share music recommendations and interact with other users
Customize your profile with your favorite music
Discover new music through socially-curated playlists and trending songs


## License:

This project is licensed under the GNU GPL3.0 License. See the LICENSE.md file for details.
