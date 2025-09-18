# YouTube AI Content Analysis System

🚀 **Automated YouTube AI Content Analysis and Generation Pipeline**

This system automatically identifies top AI influencers on YouTube, analyzes their most successful videos, extracts trending patterns, and generates new content ideas with complete scripts based on data-driven insights.

## 🎯 Features

### 🔍 **AI Influencer Discovery**
- Automatically finds top 20 rapidly growing AI influencers
- Analyzes subscriber count, engagement rates, and content quality
- Filters channels based on AI relevance and growth metrics

### 📊 **Video Analysis**
- Fetches metadata from high-performing videos (100K+ views)
- Extracts titles, descriptions, tags, thumbnails, and engagement metrics
- Calculates performance scores and engagement rates
- Identifies trending topics and successful hashtags

### 💡 **Content Generation**
- Generates 50 new content ideas based on trending patterns
- Creates complete video scripts for top ideas
- Suggests optimal hashtags and thumbnail concepts
- Estimates potential views and target audience

### 📁 **Structured Output**
- `ai_influencer_videos.csv` - High-performing videos data
- `video_ideas.csv` - Generated content ideas
- `video_scripts.csv` - Complete video scripts
- `ai_influencers.csv` - Top influencer profiles
- `trending_topics.csv` - Most popular AI topics
- `successful_hashtags.csv` - High-performing hashtags

## 🛠 Installation

### Prerequisites
- Python 3.8+
- YouTube Data API v3 key
- Internet connection

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youtube-ai-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your YouTube API key
   ```

4. **Get YouTube API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API Key)
   - Add the key to your `.env` file

## 🚀 Usage

### Run Complete Analysis
```bash
python main.py
```

This will:
1. 🔍 Find top 20 AI influencers
2. 📹 Analyze their high-performing videos
3. 📈 Extract trending topics and hashtags
4. 💡 Generate 50 content ideas
5. 📝 Create 25 complete video scripts
6. 💾 Save all data to CSV files

### Custom Analysis
```python
from influencer_finder import AIInfluencerFinder
from content_generator import AIContentGenerator

# Find influencers
finder = AIInfluencerFinder()
influencers = finder.find_ai_influencers(limit=10)

# Analyze videos
videos = finder.analyze_influencer_videos(influencers)

# Generate content
generator = AIContentGenerator()
ideas = generator.generate_content_ideas(
    trending_topics=finder.extract_trending_topics(videos),
    successful_hashtags=finder.get_successful_hashtags(videos),
    analyzed_videos=videos,
    num_ideas=20
)
```

## 📊 Output Files

### `ai_influencer_videos.csv`
High-performing videos from AI influencers with:
- Video metadata (title, views, likes, comments)
- Channel information
- Engagement metrics
- Performance scores
- Thumbnail URLs

### `video_ideas.csv`
Generated content ideas including:
- Trending titles
- Content categories
- Hashtag suggestions
- Thumbnail concepts
- Estimated views and difficulty

### `video_scripts.csv`
Complete video scripts with:
- Full script text
- Estimated duration
- Key talking points
- Call-to-action suggestions
- Word count

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Analysis thresholds
MIN_VIEW_COUNT = 100000  # Minimum views for analysis
MIN_SUBSCRIBER_COUNT = 50000  # Minimum subscribers for influencers
MAX_VIDEOS_PER_CHANNEL = 20  # Videos to analyze per channel

# Content generation
SCRIPT_MIN_LENGTH = 500  # Minimum script length
SCRIPT_MAX_LENGTH = 2000  # Maximum script length

# Keywords for AI content discovery
AI_KEYWORDS = [
    'artificial intelligence',
    'machine learning',
    'deep learning',
    'ChatGPT',
    'AI tools'
    # Add more keywords as needed
]
```

## 🎬 Content Categories

The system generates content in 6 categories:

1. **📚 Tutorials** - Step-by-step guides and how-tos
2. **📰 News** - Latest AI developments and updates
3. **⚖️ Comparisons** - Tool and technology comparisons
4. **🧠 Explanations** - Complex concepts simplified
5. **🔮 Predictions** - Future trends and forecasts
6. **⭐ Reviews** - Product and service reviews

## 📈 Analytics Features

### Trend Analysis
- Identifies recurring themes in successful videos
- Tracks keyword frequency and performance
- Analyzes optimal video lengths and formats

### Engagement Metrics
- Calculates like-to-view ratios
- Measures comment engagement
- Scores overall video performance

### Growth Indicators
- Channel growth rates
- Video performance trends
- Audience engagement patterns

## 🔧 API Rate Limits

The system handles YouTube API quotas automatically:
- Built-in rate limiting (100 requests/minute)
- Automatic retry logic
- Efficient batch processing
- Progress tracking and logging

## 📝 Example Output

```
🎯 AI Influencers Found: 20
📈 Total Subscribers: 15,234,567
📹 Total Videos Analyzed: 387
👀 Total Views Analyzed: 89,456,123
📊 Average Views per Video: 231,247

💡 Content Ideas Generated: 50
📂 Ideas by Category:
   • Tutorial: 12
   • News: 10
   • Comparison: 8
   • Explanation: 8
   • Prediction: 7
   • Review: 5

📝 Scripts Generated: 25
📖 Total Words in Scripts: 45,678
```

## 🚨 Important Notes

### API Limitations
- YouTube API has daily quotas (10,000 units/day for free tier)
- Each video analysis uses ~5-10 quota units
- Monitor usage in Google Cloud Console

### Data Privacy
- Only analyzes public YouTube data
- No personal information collected
- Respects YouTube's Terms of Service

### Rate Limiting
- Built-in delays prevent API throttling
- Large analyses may take 30-60 minutes
- Progress updates provided throughout

## 🛡️ Error Handling

The system includes robust error handling:
- API connection failures
- Invalid or expired API keys
- Network timeouts
- Data parsing errors
- File I/O issues

All errors are logged with helpful messages for debugging.

## 🔄 Updates and Maintenance

### Regular Updates Needed
- AI keyword lists (trends change rapidly)
- Influencer discovery queries
- Content templates
- Hashtag relevance

### Performance Optimization
- Cache frequently accessed data
- Batch API requests efficiently
- Monitor quota usage
- Update to latest API versions

## 📞 Support

### Common Issues

**No influencers found:**
- Check API key validity
- Verify internet connection
- Ensure sufficient API quota

**Low-quality content ideas:**
- Update AI keyword lists
- Adjust minimum view thresholds
- Expand influencer search terms

**API quota exceeded:**
- Wait for quota reset (daily)
- Optimize query parameters
- Consider premium API tier

## 🎯 Best Practices

### For Content Creation
1. **Focus on high-trend-score ideas** (>50)
2. **Adapt scripts to your voice and style**
3. **Verify information in news-type content**
4. **Test thumbnail concepts before production**
5. **Monitor performance and iterate**

### For Analysis
1. **Run weekly for fresh trends**
2. **Expand keyword lists regularly**
3. **Include new AI influencers**
4. **Track seasonal content patterns**
5. **Compare performance across categories**

## 🚀 Next Steps

After running the analysis:

1. **Review generated content ideas** in `video_ideas.csv`
2. **Select high-scoring scripts** from `video_scripts.csv`
3. **Research trending topics** from `trending_topics.csv`
4. **Implement successful hashtags** from `successful_hashtags.csv`
5. **Study top-performing videos** for inspiration
6. **Create and publish content** based on insights
7. **Track performance** and refine strategy

## 📄 License

This project is provided as-is for educational and research purposes. Please ensure compliance with YouTube's Terms of Service and API guidelines when using this tool.

---

**Happy content creating! 🎬✨**
