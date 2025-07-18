"""
AI Influencer Finder and Analyzer
"""
import re
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import pandas as pd
from youtube_api_client import YouTubeAPIClient
import config


class AIInfluencerFinder:
    """Find and analyze top AI influencers on YouTube"""
    
    def __init__(self):
        """Initialize the influencer finder"""
        self.youtube_client = YouTubeAPIClient()
        self.influencers = []
        self.analyzed_videos = []
    
    def find_ai_influencers(self, limit: int = 20) -> List[Dict]:
        """
        Find top AI influencers based on multiple criteria
        
        Args:
            limit: Maximum number of influencers to return
            
        Returns:
            List of influencer information dictionaries
        """
        print("🔍 Searching for AI influencers...")
        
        all_channels = []
        
        # Search using AI-related keywords
        for keyword in config.AI_KEYWORDS:
            print(f"Searching for channels with keyword: {keyword}")
            channels = self.youtube_client.search_channels(keyword, max_results=20)
            all_channels.extend(channels)
        
        # Remove duplicates
        unique_channels = {}
        for channel in all_channels:
            channel_id = channel['channel_id']
            if channel_id not in unique_channels:
                unique_channels[channel_id] = channel
        
        channel_ids = list(unique_channels.keys())
        print(f"Found {len(channel_ids)} unique channels")
        
        # Get detailed statistics for all channels
        print("📊 Getting channel statistics...")
        channel_stats = self.youtube_client.get_channel_statistics(channel_ids)
        
        # Filter channels based on subscriber count and AI relevance
        ai_influencers = []
        for stats in channel_stats:
            if (stats['subscriber_count'] >= config.MIN_SUBSCRIBER_COUNT and
                self._is_ai_related_channel(stats)):
                
                # Calculate growth rate and engagement metrics
                stats['growth_score'] = self._calculate_growth_score(stats)
                stats['ai_relevance_score'] = self._calculate_ai_relevance_score(stats)
                ai_influencers.append(stats)
        
        # Sort by combined score (subscriber count + growth + relevance)
        ai_influencers.sort(key=lambda x: (
            x['subscriber_count'] * 0.4 + 
            x['growth_score'] * 0.3 + 
            x['ai_relevance_score'] * 0.3
        ), reverse=True)
        
        top_influencers = ai_influencers[:limit]
        
        print(f"✅ Found {len(top_influencers)} top AI influencers")
        for i, influencer in enumerate(top_influencers[:10], 1):
            print(f"{i}. {influencer['channel_title']} - {influencer['subscriber_count']:,} subscribers")
        
        self.influencers = top_influencers
        return top_influencers
    
    def _is_ai_related_channel(self, channel_stats: Dict) -> bool:
        """
        Check if a channel is AI-related based on title and description
        
        Args:
            channel_stats: Channel statistics dictionary
            
        Returns:
            True if channel is AI-related, False otherwise
        """
        text_to_check = (
            channel_stats.get('channel_title', '').lower() + ' ' +
            channel_stats.get('description', '').lower()
        )
        
        ai_indicators = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'ai', 'ml', 'data science', 'computer vision',
            'natural language processing', 'nlp', 'robotics', 'automation',
            'chatgpt', 'openai', 'tensorflow', 'pytorch', 'kaggle',
            'algorithm', 'programming', 'coding', 'tech', 'technology'
        ]
        
        score = 0
        for indicator in ai_indicators:
            if indicator in text_to_check:
                score += 1
        
        return score >= 2  # At least 2 AI-related terms
    
    def _calculate_growth_score(self, channel_stats: Dict) -> float:
        """
        Calculate a growth score based on video count and channel age
        
        Args:
            channel_stats: Channel statistics dictionary
            
        Returns:
            Growth score (higher is better)
        """
        try:
            published_date = datetime.fromisoformat(
                channel_stats['published_at'].replace('Z', '+00:00')
            )
            channel_age_days = (datetime.now().replace(tzinfo=published_date.tzinfo) - published_date).days
            
            if channel_age_days > 0:
                videos_per_day = channel_stats['video_count'] / channel_age_days
                views_per_video = channel_stats['view_count'] / max(channel_stats['video_count'], 1)
                
                # Normalize scores
                growth_score = (videos_per_day * 365 * 10) + (views_per_video / 10000)
                return min(growth_score, 1000)  # Cap at 1000
            
        except Exception:
            pass
        
        return 0.0
    
    def _calculate_ai_relevance_score(self, channel_stats: Dict) -> float:
        """
        Calculate AI relevance score based on keywords in title and description
        
        Args:
            channel_stats: Channel statistics dictionary
            
        Returns:
            AI relevance score (0-100)
        """
        text_to_check = (
            channel_stats.get('channel_title', '').lower() + ' ' +
            channel_stats.get('description', '').lower()
        )
        
        high_value_keywords = ['artificial intelligence', 'machine learning', 'deep learning', 'ai', 'ml']
        medium_value_keywords = ['data science', 'programming', 'tech', 'computer science', 'automation']
        low_value_keywords = ['tutorial', 'coding', 'software', 'algorithm', 'python']
        
        score = 0
        for keyword in high_value_keywords:
            if keyword in text_to_check:
                score += 20
        
        for keyword in medium_value_keywords:
            if keyword in text_to_check:
                score += 10
        
        for keyword in low_value_keywords:
            if keyword in text_to_check:
                score += 5
        
        return min(score, 100)  # Cap at 100
    
    def analyze_influencer_videos(self, influencers: List[Dict] = None) -> List[Dict]:
        """
        Analyze videos from top AI influencers
        
        Args:
            influencers: List of influencer dictionaries (uses self.influencers if None)
            
        Returns:
            List of analyzed video dictionaries
        """
        if influencers is None:
            influencers = self.influencers
        
        if not influencers:
            print("No influencers found. Please run find_ai_influencers() first.")
            return []
        
        print("📹 Analyzing influencer videos...")
        
        all_videos = []
        for i, influencer in enumerate(influencers, 1):
            print(f"Analyzing videos from {influencer['channel_title']} ({i}/{len(influencers)})")
            
            videos = self.youtube_client.get_channel_videos(
                influencer['channel_id'],
                max_results=config.MAX_VIDEOS_PER_CHANNEL
            )
            
            # Add influencer info to each video
            for video in videos:
                video['influencer_subscriber_count'] = influencer['subscriber_count']
                video['influencer_total_views'] = influencer['view_count']
                
                # Calculate engagement metrics
                video['engagement_rate'] = self._calculate_engagement_rate(video)
                video['performance_score'] = self._calculate_performance_score(video, influencer)
                
                all_videos.append(video)
        
        # Filter high-performing videos
        high_performing_videos = [
            video for video in all_videos 
            if video['view_count'] >= config.MIN_VIEW_COUNT
        ]
        
        # Sort by performance score
        high_performing_videos.sort(key=lambda x: x['performance_score'], reverse=True)
        
        print(f"✅ Analyzed {len(all_videos)} total videos, {len(high_performing_videos)} high-performing")
        
        self.analyzed_videos = high_performing_videos
        return high_performing_videos
    
    def _calculate_engagement_rate(self, video: Dict) -> float:
        """
        Calculate video engagement rate
        
        Args:
            video: Video information dictionary
            
        Returns:
            Engagement rate (0-100)
        """
        view_count = max(video['view_count'], 1)
        like_count = video['like_count']
        comment_count = video['comment_count']
        
        engagement_rate = ((like_count + comment_count * 2) / view_count) * 100
        return min(engagement_rate, 100)  # Cap at 100%
    
    def _calculate_performance_score(self, video: Dict, influencer: Dict) -> float:
        """
        Calculate overall video performance score
        
        Args:
            video: Video information dictionary
            influencer: Influencer information dictionary
            
        Returns:
            Performance score
        """
        # Normalize view count relative to channel size
        view_ratio = video['view_count'] / max(influencer['subscriber_count'], 1)
        
        # Consider engagement rate
        engagement_score = video['engagement_rate']
        
        # Consider recency (newer videos get slight boost)
        try:
            published_date = datetime.fromisoformat(
                video['published_at'].replace('Z', '+00:00')
            )
            days_old = (datetime.now().replace(tzinfo=published_date.tzinfo) - published_date).days
            recency_score = max(0, 365 - days_old) / 365  # Score from 0-1
        except Exception:
            recency_score = 0
        
        # Combined score
        performance_score = (
            view_ratio * 1000 +  # Views relative to subscriber count
            engagement_score * 10 +  # Engagement rate
            recency_score * 100  # Recency bonus
        )
        
        return performance_score
    
    def extract_trending_topics(self, videos: List[Dict] = None) -> Dict[str, int]:
        """
        Extract trending topics from video titles and descriptions
        
        Args:
            videos: List of video dictionaries (uses self.analyzed_videos if None)
            
        Returns:
            Dictionary of topics and their frequency
        """
        if videos is None:
            videos = self.analyzed_videos
        
        if not videos:
            print("No videos to analyze. Please run analyze_influencer_videos() first.")
            return {}
        
        print("🔍 Extracting trending topics...")
        
        # Combine all text content
        all_text = []
        for video in videos:
            text = (video['title'] + ' ' + video.get('description', '')).lower()
            # Add tags if available
            if video.get('tags'):
                text += ' ' + ' '.join(video['tags']).lower()
            all_text.append(text)
        
        # Extract topics using keyword matching and frequency analysis
        topics = {}
        
        # AI-specific topics to track
        ai_topics = [
            'chatgpt', 'gpt', 'openai', 'claude', 'gemini', 'bard',
            'machine learning', 'deep learning', 'neural network',
            'computer vision', 'nlp', 'natural language processing',
            'tensorflow', 'pytorch', 'transformers', 'llm', 'large language model',
            'artificial intelligence', 'automation', 'robotics',
            'data science', 'python', 'coding', 'programming',
            'tutorial', 'explained', 'guide', 'how to', 'beginner',
            'ai tools', 'ai news', 'future', 'prediction', 'breakthrough'
        ]
        
        for text in all_text:
            for topic in ai_topics:
                if topic in text:
                    topics[topic] = topics.get(topic, 0) + 1
        
        # Sort by frequency
        sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
        
        print(f"✅ Found {len(sorted_topics)} trending topics")
        for topic, count in list(sorted_topics.items())[:10]:
            print(f"  {topic}: {count} mentions")
        
        return sorted_topics
    
    def get_successful_hashtags(self, videos: List[Dict] = None, min_views: int = None) -> List[str]:
        """
        Extract hashtags from successful videos
        
        Args:
            videos: List of video dictionaries (uses self.analyzed_videos if None)
            min_views: Minimum view count for videos to consider
            
        Returns:
            List of successful hashtags
        """
        if videos is None:
            videos = self.analyzed_videos
        
        if min_views is None:
            min_views = config.MIN_VIEW_COUNT
        
        if not videos:
            return []
        
        print("🏷️ Extracting successful hashtags...")
        
        hashtags = {}
        hashtag_pattern = r'#(\w+)'
        
        for video in videos:
            if video['view_count'] >= min_views:
                # Extract hashtags from title and description
                text = video['title'] + ' ' + video.get('description', '')
                found_hashtags = re.findall(hashtag_pattern, text, re.IGNORECASE)
                
                for hashtag in found_hashtags:
                    hashtag = hashtag.lower()
                    if hashtag not in hashtags:
                        hashtags[hashtag] = {'count': 0, 'total_views': 0, 'videos': []}
                    
                    hashtags[hashtag]['count'] += 1
                    hashtags[hashtag]['total_views'] += video['view_count']
                    hashtags[hashtag]['videos'].append(video['video_id'])
        
        # Calculate average views per hashtag
        for hashtag in hashtags:
            hashtags[hashtag]['avg_views'] = (
                hashtags[hashtag]['total_views'] / hashtags[hashtag]['count']
            )
        
        # Sort by average views and frequency
        sorted_hashtags = sorted(
            hashtags.items(),
            key=lambda x: (x[1]['avg_views'] * x[1]['count']),
            reverse=True
        )
        
        successful_hashtags = [f"#{hashtag}" for hashtag, _ in sorted_hashtags[:50]]
        
        print(f"✅ Found {len(successful_hashtags)} successful hashtags")
        return successful_hashtags