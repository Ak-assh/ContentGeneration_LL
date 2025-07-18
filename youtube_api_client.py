"""
YouTube API Client for fetching channel and video data
"""
import os
import time
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config


class YouTubeAPIClient:
    """YouTube Data API v3 client for fetching channel and video information"""
    
    def __init__(self):
        """Initialize the YouTube API client"""
        if not config.YOUTUBE_API_KEY:
            raise ValueError("YouTube API key not found. Please set YOUTUBE_API_KEY in .env file")
        
        self.youtube = build(
            config.YOUTUBE_API_SERVICE_NAME,
            config.YOUTUBE_API_VERSION,
            developerKey=config.YOUTUBE_API_KEY
        )
        self.request_count = 0
        self.max_requests_per_minute = 100  # YouTube API quota limit
    
    def _handle_rate_limit(self):
        """Handle API rate limiting"""
        self.request_count += 1
        if self.request_count >= self.max_requests_per_minute:
            print("Rate limit reached, waiting 60 seconds...")
            time.sleep(60)
            self.request_count = 0
    
    def search_channels(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search for channels based on a query
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of channel information dictionaries
        """
        try:
            self._handle_rate_limit()
            
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                type='channel',
                maxResults=min(max_results, config.MAX_RESULTS_PER_REQUEST),
                order='relevance'
            ).execute()
            
            channels = []
            for item in search_response['items']:
                channel_info = {
                    'channel_id': item['id']['channelId'],
                    'channel_title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails'].get('default', {}).get('url', '')
                }
                channels.append(channel_info)
            
            return channels
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    
    def get_channel_statistics(self, channel_ids: List[str]) -> List[Dict]:
        """
        Get detailed statistics for channels
        
        Args:
            channel_ids: List of channel IDs
            
        Returns:
            List of channel statistics dictionaries
        """
        try:
            self._handle_rate_limit()
            
            # YouTube API allows up to 50 channel IDs per request
            channel_stats = []
            for i in range(0, len(channel_ids), 50):
                batch_ids = channel_ids[i:i+50]
                
                response = self.youtube.channels().list(
                    part='snippet,statistics,brandingSettings',
                    id=','.join(batch_ids)
                ).execute()
                
                for item in response['items']:
                    stats = {
                        'channel_id': item['id'],
                        'channel_title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
                        'video_count': int(item['statistics'].get('videoCount', 0)),
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'thumbnail_url': item['snippet']['thumbnails'].get('default', {}).get('url', ''),
                        'country': item['snippet'].get('country', ''),
                        'custom_url': item['snippet'].get('customUrl', '')
                    }
                    channel_stats.append(stats)
            
            return channel_stats
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    
    def get_channel_videos(self, channel_id: str, max_results: int = 20) -> List[Dict]:
        """
        Get recent videos from a channel
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to fetch
            
        Returns:
            List of video information dictionaries
        """
        try:
            self._handle_rate_limit()
            
            # First, get the uploads playlist ID
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                return []
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from the uploads playlist
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                self._handle_rate_limit()
                
                playlist_response = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=min(config.MAX_RESULTS_PER_REQUEST, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
                video_details = self.get_video_details(video_ids)
                videos.extend(video_details)
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            return videos[:max_results]
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """
        Get detailed information for videos
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            List of video details dictionaries
        """
        try:
            self._handle_rate_limit()
            
            video_details = []
            
            # Process videos in batches of 50 (API limit)
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(batch_ids)
                ).execute()
                
                for item in response['items']:
                    video_info = {
                        'video_id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'channel_id': item['snippet']['channelId'],
                        'channel_title': item['snippet']['channelTitle'],
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'comment_count': int(item['statistics'].get('commentCount', 0)),
                        'duration': item['contentDetails'].get('duration', ''),
                        'thumbnail_url': item['snippet']['thumbnails'].get('maxres', 
                                       item['snippet']['thumbnails'].get('high', 
                                       item['snippet']['thumbnails'].get('medium', {}))).get('url', ''),
                        'tags': item['snippet'].get('tags', []),
                        'category_id': item['snippet'].get('categoryId', ''),
                        'default_language': item['snippet'].get('defaultLanguage', ''),
                        'video_url': f"https://www.youtube.com/watch?v={item['id']}"
                    }
                    video_details.append(video_info)
            
            return video_details
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    
    def search_videos(self, query: str, max_results: int = 50, published_after: str = None) -> List[Dict]:
        """
        Search for videos based on a query
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            published_after: RFC 3339 formatted date-time value (e.g., '2023-01-01T00:00:00Z')
            
        Returns:
            List of video information dictionaries
        """
        try:
            self._handle_rate_limit()
            
            search_params = {
                'q': query,
                'part': 'id,snippet',
                'type': 'video',
                'maxResults': min(max_results, config.MAX_RESULTS_PER_REQUEST),
                'order': 'relevance'
            }
            
            if published_after:
                search_params['publishedAfter'] = published_after
            
            search_response = self.youtube.search().list(**search_params).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            video_details = self.get_video_details(video_ids)
            
            return video_details
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    
    def get_trending_ai_videos(self, max_results: int = 100) -> List[Dict]:
        """
        Get trending AI-related videos
        
        Args:
            max_results: Maximum number of videos to return
            
        Returns:
            List of trending AI video dictionaries
        """
        all_videos = []
        
        for keyword in config.AI_KEYWORDS:
            videos = self.search_videos(
                query=keyword,
                max_results=max_results // len(config.AI_KEYWORDS)
            )
            all_videos.extend(videos)
        
        # Filter videos with high view counts and remove duplicates
        seen_video_ids = set()
        filtered_videos = []
        
        for video in all_videos:
            if (video['video_id'] not in seen_video_ids and 
                video['view_count'] >= config.MIN_VIEW_COUNT):
                seen_video_ids.add(video['video_id'])
                filtered_videos.append(video)
        
        # Sort by view count descending
        filtered_videos.sort(key=lambda x: x['view_count'], reverse=True)
        
        return filtered_videos[:max_results]