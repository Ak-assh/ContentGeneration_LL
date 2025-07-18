#!/usr/bin/env python3
"""
Command Line Interface for YouTube AI Content Analysis
"""
import argparse
import sys
import os
from typing import List

# Import our modules
from youtube_api_client import YouTubeAPIClient
from influencer_finder import AIInfluencerFinder
from content_generator import AIContentGenerator
import config


def run_quick_analysis(num_influencers: int = 5, num_ideas: int = 10):
    """Run a quick analysis with fewer influencers and ideas"""
    print(f"🚀 Running Quick Analysis")
    print(f"   • Finding {num_influencers} influencers")
    print(f"   • Generating {num_ideas} content ideas")
    print("-" * 40)
    
    try:
        # Find influencers
        finder = AIInfluencerFinder()
        influencers = finder.find_ai_influencers(limit=num_influencers)
        
        if not influencers:
            print("❌ No influencers found")
            return
        
        # Analyze videos
        videos = finder.analyze_influencer_videos(influencers)
        
        # Extract trends
        trending_topics = finder.extract_trending_topics(videos)
        hashtags = finder.get_successful_hashtags(videos)
        
        # Generate content
        generator = AIContentGenerator()
        ideas = generator.generate_content_ideas(
            trending_topics=trending_topics,
            successful_hashtags=hashtags,
            analyzed_videos=videos,
            num_ideas=num_ideas
        )
        
        # Display results
        print(f"\n✅ Quick Analysis Complete!")
        print(f"   • Found {len(influencers)} influencers")
        print(f"   • Analyzed {len(videos)} videos")
        print(f"   • Generated {len(ideas)} content ideas")
        
        # Show top 3 ideas
        print(f"\n🔝 Top 3 Content Ideas:")
        for i, idea in enumerate(ideas[:3], 1):
            print(f"   {i}. {idea['title']}")
            print(f"      Category: {idea['category']} | Score: {idea['trend_score']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def search_specific_topic(topic: str, num_videos: int = 10):
    """Search for videos on a specific topic"""
    print(f"🔍 Searching for '{topic}' videos...")
    
    try:
        client = YouTubeAPIClient()
        videos = client.search_videos(topic, max_results=num_videos)
        
        if not videos:
            print("❌ No videos found")
            return
        
        print(f"\n📹 Found {len(videos)} videos:")
        for i, video in enumerate(videos, 1):
            print(f"   {i}. {video['title']}")
            print(f"      Channel: {video['channel_title']}")
            print(f"      Views: {video['view_count']:,}")
            print(f"      URL: {video['video_url']}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")


def generate_ideas_only(num_ideas: int = 20):
    """Generate content ideas using pre-defined trending topics"""
    print(f"💡 Generating {num_ideas} content ideas...")
    
    # Use sample trending topics
    trending_topics = {
        'chatgpt': 100, 'ai': 95, 'machine learning': 80,
        'python': 75, 'tutorial': 70, 'automation': 65
    }
    
    hashtags = ['#AI', '#MachineLearning', '#Python', '#Tech', '#Programming']
    
    try:
        generator = AIContentGenerator()
        ideas = generator.generate_content_ideas(
            trending_topics=trending_topics,
            successful_hashtags=hashtags,
            analyzed_videos=[],
            num_ideas=num_ideas
        )
        
        print(f"\n🚀 Generated {len(ideas)} content ideas:")
        for i, idea in enumerate(ideas, 1):
            print(f"   {i:2d}. {idea['title']}")
            print(f"       Category: {idea['category']} | Score: {idea['trend_score']}")
            if i % 5 == 0:
                print()
        
    except Exception as e:
        print(f"❌ Error: {e}")


def check_api_status():
    """Check if YouTube API is working"""
    print("🔧 Checking API status...")
    
    if not config.YOUTUBE_API_KEY:
        print("❌ YouTube API key not found in .env file")
        return False
    
    try:
        client = YouTubeAPIClient()
        # Try a simple search
        videos = client.search_videos("AI", max_results=1)
        
        if videos:
            print("✅ YouTube API is working")
            print(f"   API Key: {config.YOUTUBE_API_KEY[:10]}...")
            return True
        else:
            print("⚠️ API responded but no results found")
            return False
            
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False


def list_trending_keywords():
    """List current trending AI keywords"""
    print("🔥 Current AI Keywords for Analysis:")
    print("-" * 40)
    
    for i, keyword in enumerate(config.AI_KEYWORDS, 1):
        print(f"   {i:2d}. {keyword}")
    
    print(f"\n📊 Total keywords: {len(config.AI_KEYWORDS)}")
    print("💡 Edit config.py to add more keywords")


def show_config():
    """Show current configuration"""
    print("⚙️ Current Configuration:")
    print("-" * 40)
    print(f"   Min View Count: {config.MIN_VIEW_COUNT:,}")
    print(f"   Min Subscriber Count: {config.MIN_SUBSCRIBER_COUNT:,}")
    print(f"   Max Videos per Channel: {config.MAX_VIDEOS_PER_CHANNEL}")
    print(f"   AI Keywords: {len(config.AI_KEYWORDS)}")
    print(f"   Output Directory: {config.OUTPUT_DIR}")
    print()
    print("💡 Edit config.py to modify these settings")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="YouTube AI Content Analysis CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --quick                    # Quick analysis (5 influencers, 10 ideas)
  python cli.py --search "ChatGPT"        # Search for ChatGPT videos
  python cli.py --ideas 30                # Generate 30 content ideas
  python cli.py --check-api               # Test API connection
  python cli.py --keywords                # List AI keywords
  python cli.py --config                  # Show configuration
        """
    )
    
    parser.add_argument('--quick', action='store_true',
                        help='Run quick analysis (5 influencers, 10 ideas)')
    
    parser.add_argument('--search', type=str, metavar='TOPIC',
                        help='Search for videos on specific topic')
    
    parser.add_argument('--videos', type=int, default=10, metavar='N',
                        help='Number of videos to fetch (default: 10)')
    
    parser.add_argument('--ideas', type=int, metavar='N',
                        help='Generate N content ideas using sample data')
    
    parser.add_argument('--influencers', type=int, default=5, metavar='N',
                        help='Number of influencers for quick analysis (default: 5)')
    
    parser.add_argument('--check-api', action='store_true',
                        help='Check if YouTube API is working')
    
    parser.add_argument('--keywords', action='store_true',
                        help='List current AI keywords')
    
    parser.add_argument('--config', action='store_true',
                        help='Show current configuration')
    
    args = parser.parse_args()
    
    # Show help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    print("🎬 YouTube AI Content Analysis CLI")
    print("="*50)
    
    # Execute commands
    if args.check_api:
        check_api_status()
    
    elif args.keywords:
        list_trending_keywords()
    
    elif args.config:
        show_config()
    
    elif args.quick:
        run_quick_analysis(args.influencers, 10)
    
    elif args.search:
        search_specific_topic(args.search, args.videos)
    
    elif args.ideas:
        generate_ideas_only(args.ideas)
    
    else:
        print("⚠️ No action specified. Use --help for available options.")


if __name__ == "__main__":
    main()