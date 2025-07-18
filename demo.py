#!/usr/bin/env python3
"""
Demo Script for YouTube AI Content Analysis
Demonstrates functionality with sample data (no API key required)
"""
import os
import pandas as pd
from datetime import datetime
from content_generator import AIContentGenerator


def create_sample_data():
    """Create sample data for demonstration"""
    
    # Sample trending topics (from real AI YouTube content)
    trending_topics = {
        'chatgpt': 150,
        'ai': 120,
        'machine learning': 95,
        'python': 85,
        'tutorial': 80,
        'deep learning': 70,
        'automation': 65,
        'coding': 60,
        'tensorflow': 55,
        'openai': 50,
        'neural network': 45,
        'programming': 40,
        'data science': 38,
        'computer vision': 35,
        'nlp': 32,
        'robotics': 30,
        'artificial intelligence': 28,
        'pytorch': 25,
        'algorithm': 22,
        'future': 20
    }
    
    # Sample successful hashtags
    successful_hashtags = [
        '#AI', '#MachineLearning', '#Python', '#Tech', '#Programming',
        '#ChatGPT', '#OpenAI', '#DeepLearning', '#Coding', '#Tutorial',
        '#DataScience', '#TensorFlow', '#PyTorch', '#Automation',
        '#ComputerVision', '#NLP', '#Robotics', '#Algorithm',
        '#ArtificialIntelligence', '#TechNews', '#Innovation',
        '#SoftwareDevelopment', '#WebDev', '#JavaScript', '#React'
    ]
    
    # Sample analyzed videos
    analyzed_videos = [
        {
            'video_id': 'demo1',
            'title': 'ChatGPT Changed Everything: Complete Tutorial',
            'channel_title': 'AI Explained',
            'view_count': 250000,
            'like_count': 12000,
            'comment_count': 850,
            'published_at': '2024-01-15T10:00:00Z',
            'tags': ['chatgpt', 'ai', 'tutorial', 'openai'],
            'engagement_rate': 5.14,
            'performance_score': 85.2
        },
        {
            'video_id': 'demo2',
            'title': 'Build AI App in 10 Minutes with Python',
            'channel_title': 'Code With AI',
            'view_count': 180000,
            'like_count': 9500,
            'comment_count': 620,
            'published_at': '2024-01-20T14:30:00Z',
            'tags': ['python', 'ai', 'coding', 'tutorial'],
            'engagement_rate': 5.62,
            'performance_score': 78.9
        },
        {
            'video_id': 'demo3',
            'title': 'AI vs Human: The Future of Programming',
            'channel_title': 'Tech Future',
            'view_count': 320000,
            'like_count': 15800,
            'comment_count': 1200,
            'published_at': '2024-01-18T16:45:00Z',
            'tags': ['ai', 'programming', 'future', 'prediction'],
            'engagement_rate': 5.31,
            'performance_score': 92.7
        }
    ]
    
    return trending_topics, successful_hashtags, analyzed_videos


def run_demo():
    """Run the demo with sample data"""
    print("🎬 YouTube AI Content Analysis - DEMO MODE")
    print("="*60)
    print("📝 This demo shows the system functionality using sample data")
    print("🔑 No API key required for this demonstration")
    print("="*60)
    
    # Create sample data
    trending_topics, successful_hashtags, analyzed_videos = create_sample_data()
    
    print(f"\n📊 Sample Data Loaded:")
    print(f"   • Trending Topics: {len(trending_topics)}")
    print(f"   • Successful Hashtags: {len(successful_hashtags)}")
    print(f"   • Analyzed Videos: {len(analyzed_videos)}")
    
    # Show trending topics
    print(f"\n🔥 Top 10 Trending Topics:")
    for i, (topic, count) in enumerate(list(trending_topics.items())[:10], 1):
        print(f"   {i:2d}. {topic}: {count} mentions")
    
    # Show successful hashtags
    print(f"\n🏷️ Top 10 Successful Hashtags:")
    for i, hashtag in enumerate(successful_hashtags[:10], 1):
        print(f"   {i:2d}. {hashtag}")
    
    # Generate content ideas
    print(f"\n💡 Generating Content Ideas...")
    content_generator = AIContentGenerator()
    
    content_ideas = content_generator.generate_content_ideas(
        trending_topics=trending_topics,
        successful_hashtags=successful_hashtags,
        analyzed_videos=analyzed_videos,
        num_ideas=10  # Generate fewer for demo
    )
    
    # Show top content ideas
    print(f"\n🚀 Top 5 Generated Content Ideas:")
    for i, idea in enumerate(content_ideas[:5], 1):
        print(f"\n   {i}. {idea['title']}")
        print(f"      Category: {idea['category'].title()}")
        print(f"      Trend Score: {idea['trend_score']}")
        print(f"      Estimated Views: {idea['estimated_views']:,}")
        print(f"      Difficulty: {idea['difficulty']}")
        print(f"      Target Audience: {idea['target_audience']}")
        print(f"      Hashtags: {', '.join(idea['hashtags'][:5])}")
    
    # Generate scripts for top ideas
    print(f"\n📝 Generating Video Scripts...")
    scripts = content_generator.generate_video_scripts(
        content_ideas=content_ideas[:3],  # Generate scripts for top 3 ideas
        num_scripts=3
    )
    
    # Show sample script
    if scripts:
        sample_script = scripts[0]
        print(f"\n📜 Sample Generated Script:")
        print(f"   Title: {sample_script['title']}")
        print(f"   Category: {sample_script['category'].title()}")
        print(f"   Duration: {sample_script['estimated_duration']}")
        print(f"   Word Count: {sample_script['word_count']}")
        print(f"   Call to Action: {sample_script['call_to_action']}")
        
        # Show script preview (first 500 characters)
        script_preview = sample_script['script'][:500] + "..."
        print(f"\n   Script Preview:")
        print("   " + "-" * 50)
        for line in script_preview.split('\n')[:10]:
            if line.strip():
                print(f"   {line.strip()}")
        print("   " + "-" * 50)
        print("   [Script continues...]")
    
    # Create output directory and save sample data
    output_dir = 'demo_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save demo data to CSV files
    print(f"\n💾 Saving Demo Data to CSV Files...")
    
    # Content ideas
    ideas_df = pd.DataFrame([{
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
    } for idea in content_ideas])
    
    ideas_df.to_csv(f'{output_dir}/demo_video_ideas.csv', index=False)
    print(f"   ✅ Saved {len(content_ideas)} content ideas to demo_video_ideas.csv")
    
    # Scripts
    if scripts:
        scripts_df = pd.DataFrame([{
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
        } for script in scripts])
        
        scripts_df.to_csv(f'{output_dir}/demo_video_scripts.csv', index=False)
        print(f"   ✅ Saved {len(scripts)} video scripts to demo_video_scripts.csv")
    
    # Trending topics
    topics_df = pd.DataFrame([
        {'topic': topic, 'frequency': freq} 
        for topic, freq in trending_topics.items()
    ])
    topics_df.to_csv(f'{output_dir}/demo_trending_topics.csv', index=False)
    print(f"   ✅ Saved {len(trending_topics)} trending topics to demo_trending_topics.csv")
    
    # Successful hashtags
    hashtags_df = pd.DataFrame([
        {'hashtag': hashtag, 'rank': i+1} 
        for i, hashtag in enumerate(successful_hashtags)
    ])
    hashtags_df.to_csv(f'{output_dir}/demo_successful_hashtags.csv', index=False)
    print(f"   ✅ Saved {len(successful_hashtags)} hashtags to demo_successful_hashtags.csv")
    
    print(f"\n🎉 Demo Complete!")
    print(f"📁 Demo files saved to: {output_dir}/")
    print(f"\n📋 Generated Demo Files:")
    print(f"   • demo_video_ideas.csv - {len(content_ideas)} content ideas")
    print(f"   • demo_video_scripts.csv - {len(scripts)} video scripts")
    print(f"   • demo_trending_topics.csv - {len(trending_topics)} trending topics")
    print(f"   • demo_successful_hashtags.csv - {len(successful_hashtags)} hashtags")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Review the generated content ideas")
    print(f"   2. Examine the sample scripts")
    print(f"   3. Set up your YouTube API key in .env")
    print(f"   4. Run 'python main.py' for real analysis")
    
    print(f"\n💡 Ready to create viral AI content!")


if __name__ == "__main__":
    run_demo()