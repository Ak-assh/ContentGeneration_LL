#!/usr/bin/env python3
"""
YouTube AI Content Analysis - Main Script
Automated analysis of AI influencers and content generation
"""
import os
import sys
import pandas as pd
from datetime import datetime
from typing import List, Dict

# Import our custom modules
from youtube_api_client import YouTubeAPIClient
from influencer_finder import AIInfluencerFinder
from content_generator import AIContentGenerator
import config


def create_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        print(f"📁 Created output directory: {config.OUTPUT_DIR}")


def save_to_csv(data: List[Dict], filename: str, description: str):
    """
    Save data to CSV file
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        description: Human-readable description
    """
    if not data:
        print(f"⚠️ No data to save for {description}")
        return
    
    try:
        df = pd.DataFrame(data)
        filepath = os.path.join(config.OUTPUT_DIR, filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"💾 Saved {len(data)} {description} to {filepath}")
    except Exception as e:
        print(f"❌ Error saving {description}: {e}")


def display_summary_stats(influencers: List[Dict], videos: List[Dict], 
                         content_ideas: List[Dict], scripts: List[Dict]):
    """
    Display summary statistics
    
    Args:
        influencers: List of influencer data
        videos: List of video data
        content_ideas: List of content ideas
        scripts: List of scripts
    """
    print("\n" + "="*60)
    print("📊 ANALYSIS SUMMARY")
    print("="*60)
    
    if influencers:
        print(f"🎯 AI Influencers Found: {len(influencers)}")
        print(f"📈 Total Subscribers: {sum(inf['subscriber_count'] for inf in influencers):,}")
        print(f"📹 Total Videos Analyzed: {len(videos)}")
        
        if videos:
            total_views = sum(video['view_count'] for video in videos)
            avg_views = total_views / len(videos)
            print(f"👀 Total Views Analyzed: {total_views:,}")
            print(f"📊 Average Views per Video: {avg_views:,.0f}")
    
    if content_ideas:
        print(f"💡 Content Ideas Generated: {len(content_ideas)}")
        categories = {}
        for idea in content_ideas:
            cat = idea['category']
            categories[cat] = categories.get(cat, 0) + 1
        print("📂 Ideas by Category:")
        for category, count in categories.items():
            print(f"   • {category.title()}: {count}")
    
    if scripts:
        print(f"📝 Scripts Generated: {len(scripts)}")
        total_words = sum(script['word_count'] for script in scripts)
        print(f"📖 Total Words in Scripts: {total_words:,}")
    
    print("="*60)


def main():
    """Main execution function"""
    print("🚀 Starting YouTube AI Content Analysis")
    print("="*60)
    
    # Check if API key is available
    if not config.YOUTUBE_API_KEY:
        print("❌ YouTube API key not found!")
        print("Please set YOUTUBE_API_KEY in your .env file")
        print("Get your API key from: https://console.cloud.google.com/apis/credentials")
        sys.exit(1)
    
    # Create output directory
    create_output_directory()
    
    try:
        # Step 1: Find AI Influencers
        print("\n🔍 STEP 1: Finding Top AI Influencers")
        print("-" * 40)
        
        influencer_finder = AIInfluencerFinder()
        influencers = influencer_finder.find_ai_influencers(limit=20)
        
        if not influencers:
            print("❌ No AI influencers found. Please check your API key and connection.")
            sys.exit(1)
        
        # Step 2: Analyze Influencer Videos
        print("\n📹 STEP 2: Analyzing Influencer Videos")
        print("-" * 40)
        
        videos = influencer_finder.analyze_influencer_videos(influencers)
        
        if not videos:
            print("⚠️ No high-performing videos found. Continuing with available data...")
        
        # Step 3: Extract Trends and Patterns
        print("\n📈 STEP 3: Extracting Trends and Patterns")
        print("-" * 40)
        
        trending_topics = influencer_finder.extract_trending_topics(videos)
        successful_hashtags = influencer_finder.get_successful_hashtags(videos)
        
        # Step 4: Generate Content Ideas
        print("\n💡 STEP 4: Generating Content Ideas")
        print("-" * 40)
        
        content_generator = AIContentGenerator()
        content_ideas = content_generator.generate_content_ideas(
            trending_topics=trending_topics,
            successful_hashtags=successful_hashtags,
            analyzed_videos=videos,
            num_ideas=50
        )
        
        # Step 5: Generate Video Scripts
        print("\n📝 STEP 5: Generating Video Scripts")
        print("-" * 40)
        
        scripts = content_generator.generate_video_scripts(
            content_ideas=content_ideas,
            num_scripts=25
        )
        
        # Step 6: Save All Data to CSV Files
        print("\n💾 STEP 6: Saving Data to CSV Files")
        print("-" * 40)
        
        # Prepare video data with influencer information
        videos_for_csv = []
        for video in videos:
            video_data = {
                'video_id': video['video_id'],
                'title': video['title'],
                'channel_title': video['channel_title'],
                'channel_id': video['channel_id'],
                'view_count': video['view_count'],
                'like_count': video['like_count'],
                'comment_count': video['comment_count'],
                'published_at': video['published_at'],
                'duration': video['duration'],
                'thumbnail_url': video['thumbnail_url'],
                'video_url': video['video_url'],
                'tags': ';'.join(video.get('tags', [])),
                'engagement_rate': round(video['engagement_rate'], 2),
                'performance_score': round(video['performance_score'], 2),
                'influencer_subscriber_count': video.get('influencer_subscriber_count', 0),
                'description_snippet': video.get('description', '')[:200] + '...' if video.get('description') else ''
            }
            videos_for_csv.append(video_data)
        
        # Prepare content ideas for CSV
        ideas_for_csv = []
        for idea in content_ideas:
            idea_data = {
                'id': idea['id'],
                'title': idea['title'],
                'category': idea['category'],
                'hashtags': ';'.join(idea['hashtags']),
                'thumbnail_concept': idea['thumbnail_concept'],
                'trend_score': idea['trend_score'],
                'estimated_views': idea['estimated_views'],
                'difficulty': idea['difficulty'],
                'target_audience': idea['target_audience'],
                'key_topics': ';'.join(idea['key_topics']),
                'created_at': idea['created_at']
            }
            ideas_for_csv.append(idea_data)
        
        # Prepare scripts for CSV
        scripts_for_csv = []
        for script in scripts:
            script_data = {
                'id': script['id'],
                'title': script['title'],
                'category': script['category'],
                'script': script['script'],
                'hashtags': ';'.join(script['hashtags']),
                'thumbnail_concept': script['thumbnail_concept'],
                'estimated_duration': script['estimated_duration'],
                'word_count': script['word_count'],
                'key_points': ';'.join(script['key_points']),
                'call_to_action': script['call_to_action'],
                'created_at': script['created_at']
            }
            scripts_for_csv.append(script_data)
        
        # Save all data
        save_to_csv(videos_for_csv, 'ai_influencer_videos.csv', 'influencer videos')
        save_to_csv(ideas_for_csv, 'video_ideas.csv', 'content ideas')
        save_to_csv(scripts_for_csv, 'video_scripts.csv', 'video scripts')
        
        # Save additional analysis data
        trending_topics_csv = [{'topic': topic, 'frequency': freq} for topic, freq in trending_topics.items()]
        save_to_csv(trending_topics_csv, 'trending_topics.csv', 'trending topics')
        
        hashtags_csv = [{'hashtag': hashtag, 'rank': i+1} for i, hashtag in enumerate(successful_hashtags)]
        save_to_csv(hashtags_csv, 'successful_hashtags.csv', 'successful hashtags')
        
        influencers_csv = []
        for inf in influencers:
            inf_data = {
                'channel_id': inf['channel_id'],
                'channel_title': inf['channel_title'],
                'subscriber_count': inf['subscriber_count'],
                'video_count': inf['video_count'],
                'view_count': inf['view_count'],
                'published_at': inf['published_at'],
                'growth_score': round(inf.get('growth_score', 0), 2),
                'ai_relevance_score': round(inf.get('ai_relevance_score', 0), 2),
                'thumbnail_url': inf.get('thumbnail_url', ''),
                'custom_url': inf.get('custom_url', ''),
                'country': inf.get('country', ''),
                'description_snippet': inf.get('description', '')[:200] + '...' if inf.get('description') else ''
            }
            influencers_csv.append(inf_data)
        
        save_to_csv(influencers_csv, 'ai_influencers.csv', 'AI influencers')
        
        # Display summary
        display_summary_stats(influencers, videos, content_ideas, scripts)
        
        # Success message
        print(f"\n🎉 SUCCESS! Analysis complete!")
        print(f"📁 All files saved to: {config.OUTPUT_DIR}/")
        print("\n📋 Generated Files:")
        print("   • ai_influencer_videos.csv - High-performing videos from AI influencers")
        print("   • video_ideas.csv - 50 new content ideas based on trends")
        print("   • video_scripts.csv - 25 complete video scripts")
        print("   • ai_influencers.csv - Top 20 AI influencers data")
        print("   • trending_topics.csv - Most popular AI topics")
        print("   • successful_hashtags.csv - High-performing hashtags")
        
        print("\n🚀 Ready to create viral AI content!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your API key and internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()