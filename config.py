"""
Configuration file for YouTube AI Content Analysis
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# YouTube API Configuration
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
MAX_RESULTS_PER_REQUEST = 50

# Analysis Configuration
MIN_VIEW_COUNT = 100000  # 100K views threshold
MIN_SUBSCRIBER_COUNT = 50000  # 50K subscribers for influencer consideration
MAX_VIDEOS_PER_CHANNEL = 20  # Maximum videos to analyze per channel

# Content Generation Settings
SCRIPT_MIN_LENGTH = 500  # Minimum script length in characters
SCRIPT_MAX_LENGTH = 2000  # Maximum script length in characters

# File Paths
OUTPUT_DIR = 'output'
AI_INFLUENCER_VIDEOS_FILE = f'{OUTPUT_DIR}/ai_influencer_videos.csv'
VIDEO_IDEAS_FILE = f'{OUTPUT_DIR}/video_ideas.csv'
VIDEO_SCRIPTS_FILE = f'{OUTPUT_DIR}/video_scripts.csv'

# AI Influencer Search Keywords
AI_KEYWORDS = [
    'artificial intelligence',
    'machine learning',
    'deep learning',
    'AI tutorial',
    'neural networks',
    'ChatGPT',
    'generative AI',
    'AI tools',
    'automation',
    'AI news'
]

# Popular AI Influencer Channel IDs (some examples - you can expand this list)
KNOWN_AI_INFLUENCERS = [
    'Two Minute Papers',
    'Lex Fridman',
    'AI Explained',
    'Machine Learning Street Talk',
    'Yannic Kilcher',
    'Jeremy Howard',
    'Sentdex',
    'Data School',
    'StatQuest',
    'Corey Schafer'
]

# Content categories for trend analysis
CONTENT_CATEGORIES = [
    'tutorials',
    'news',
    'reviews',
    'explanations',
    'interviews',
    'demonstrations',
    'predictions',
    'comparisons'
]