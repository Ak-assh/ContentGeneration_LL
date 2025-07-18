"""
AI Content Generator for YouTube Videos
"""
import random
import re
from typing import List, Dict, Tuple
from datetime import datetime
import config


class AIContentGenerator:
    """Generate new content ideas and scripts based on successful AI video patterns"""
    
    def __init__(self):
        """Initialize the content generator"""
        self.trending_topics = {}
        self.successful_hashtags = []
        self.analyzed_videos = []
        self.content_templates = self._load_content_templates()
    
    def _load_content_templates(self) -> Dict[str, List[str]]:
        """
        Load content templates for different video types
        
        Returns:
            Dictionary of content templates by category
        """
        return {
            'tutorial': [
                "How to Build {} in {} Minutes",
                "Complete {} Tutorial for Beginners",
                "Master {} in {} Steps",
                "{} Explained Simply",
                "Build Your First {} Project"
            ],
            'news': [
                "Breaking: {} Changes Everything",
                "Latest {} Updates You Need to Know",
                "{} News This Week",
                "Why {} is Trending Now",
                "The Future of {} is Here"
            ],
            'comparison': [
                "{} vs {}: Which is Better?",
                "Comparing {} and {} in {}",
                "{} or {}? The Ultimate Guide",
                "Why {} Beats {} Every Time",
                "The Truth About {} vs {}"
            ],
            'explanation': [
                "{} Explained in {} Minutes",
                "What is {}? Everything You Need to Know",
                "Understanding {} Once and For All",
                "The Science Behind {}",
                "How {} Actually Works"
            ],
            'prediction': [
                "Why {} Will Dominate {}",
                "The Future of {} in {}",
                "{} Predictions for {}",
                "What's Next for {}?",
                "How {} Will Change {}"
            ],
            'review': [
                "I Tested {} for {} Days",
                "{} Review: Is It Worth It?",
                "Honest {} Review After {} Months",
                "The Truth About {}",
                "{} Deep Dive Review"
            ]
        }
    
    def generate_content_ideas(self, 
                             trending_topics: Dict[str, int], 
                             successful_hashtags: List[str],
                             analyzed_videos: List[Dict],
                             num_ideas: int = 50) -> List[Dict]:
        """
        Generate new content ideas based on trending patterns
        
        Args:
            trending_topics: Dictionary of trending topics and their frequencies
            successful_hashtags: List of successful hashtags
            analyzed_videos: List of analyzed video dictionaries
            num_ideas: Number of content ideas to generate
            
        Returns:
            List of content idea dictionaries
        """
        print(f"🚀 Generating {num_ideas} content ideas...")
        
        self.trending_topics = trending_topics
        self.successful_hashtags = successful_hashtags
        self.analyzed_videos = analyzed_videos
        
        content_ideas = []
        
        # Get top trending topics
        top_topics = list(trending_topics.keys())[:20]
        
        for i in range(num_ideas):
            category = random.choice(list(self.content_templates.keys()))
            template = random.choice(self.content_templates[category])
            
            # Generate title based on template and trending topics
            title = self._generate_title_from_template(template, top_topics)
            
            # Select hashtags
            hashtags = self._select_hashtags_for_topic(title, successful_hashtags)
            
            # Generate thumbnail concept
            thumbnail_concept = self._generate_thumbnail_concept(title, category)
            
            # Calculate trend score
            trend_score = self._calculate_trend_score(title, trending_topics)
            
            content_idea = {
                'id': i + 1,
                'title': title,
                'category': category,
                'hashtags': hashtags,
                'thumbnail_concept': thumbnail_concept,
                'trend_score': trend_score,
                'estimated_views': self._estimate_views(trend_score, category),
                'difficulty': self._estimate_difficulty(category, title),
                'target_audience': self._identify_target_audience(title),
                'key_topics': self._extract_key_topics(title),
                'created_at': datetime.now().isoformat()
            }
            
            content_ideas.append(content_idea)
        
        # Sort by trend score
        content_ideas.sort(key=lambda x: x['trend_score'], reverse=True)
        
        print(f"✅ Generated {len(content_ideas)} content ideas")
        return content_ideas
    
    def _generate_title_from_template(self, template: str, topics: List[str]) -> str:
        """
        Generate a title from a template and trending topics
        
        Args:
            template: Title template with placeholders
            topics: List of trending topics
            
        Returns:
            Generated title string
        """
        # Count placeholders in template
        placeholder_count = template.count('{}')
        
        if placeholder_count == 0:
            return template
        
        # Select random topics and numbers for placeholders
        selected_topics = random.sample(topics, min(placeholder_count, len(topics)))
        
        # Fill placeholders
        title = template
        for i, topic in enumerate(selected_topics):
            if '{}' in title:
                # Capitalize topic appropriately
                formatted_topic = self._format_topic(topic)
                title = title.replace('{}', formatted_topic, 1)
        
        # Fill any remaining placeholders with numbers or generic terms
        while '{}' in title:
            if 'minutes' in title.lower() or 'steps' in title.lower():
                title = title.replace('{}', str(random.choice([5, 10, 15, 20, 30])), 1)
            elif 'days' in title.lower():
                title = title.replace('{}', str(random.choice([7, 14, 30, 60, 90])), 1)
            elif 'months' in title.lower():
                title = title.replace('{}', str(random.choice([1, 3, 6, 12])), 1)
            else:
                title = title.replace('{}', random.choice(['2024', '2025', 'Today', 'Now']), 1)
        
        return title
    
    def _format_topic(self, topic: str) -> str:
        """
        Format a topic for use in titles
        
        Args:
            topic: Raw topic string
            
        Returns:
            Formatted topic string
        """
        # Handle common abbreviations
        abbreviations = {
            'ai': 'AI',
            'ml': 'Machine Learning',
            'nlp': 'NLP',
            'gpt': 'GPT',
            'llm': 'Large Language Models'
        }
        
        if topic.lower() in abbreviations:
            return abbreviations[topic.lower()]
        
        # Capitalize properly
        return ' '.join(word.capitalize() for word in topic.split())
    
    def _select_hashtags_for_topic(self, title: str, hashtags: List[str], max_hashtags: int = 15) -> List[str]:
        """
        Select relevant hashtags for a given title
        
        Args:
            title: Video title
            hashtags: List of all successful hashtags
            max_hashtags: Maximum number of hashtags to return
            
        Returns:
            List of selected hashtags
        """
        title_lower = title.lower()
        relevant_hashtags = []
        
        # Score hashtags based on relevance to title
        hashtag_scores = {}
        for hashtag in hashtags:
            hashtag_clean = hashtag.replace('#', '').lower()
            score = 0
            
            # Direct match in title
            if hashtag_clean in title_lower:
                score += 10
            
            # Partial matches
            for word in hashtag_clean.split():
                if word in title_lower:
                    score += 5
            
            # Topic relevance
            if any(keyword in hashtag_clean for keyword in ['ai', 'ml', 'tech', 'coding', 'tutorial']):
                score += 3
            
            if score > 0:
                hashtag_scores[hashtag] = score
        
        # Sort by score and select top hashtags
        sorted_hashtags = sorted(hashtag_scores.items(), key=lambda x: x[1], reverse=True)
        relevant_hashtags = [hashtag for hashtag, _ in sorted_hashtags[:max_hashtags]]
        
        # Add some popular AI hashtags if not enough relevant ones
        popular_ai_hashtags = ['#AI', '#MachineLearning', '#Tech', '#Programming', '#Tutorial', '#Coding']
        while len(relevant_hashtags) < 8 and popular_ai_hashtags:
            hashtag = popular_ai_hashtags.pop(0)
            if hashtag not in relevant_hashtags:
                relevant_hashtags.append(hashtag)
        
        return relevant_hashtags
    
    def _generate_thumbnail_concept(self, title: str, category: str) -> str:
        """
        Generate a thumbnail concept for a video
        
        Args:
            title: Video title
            category: Video category
            
        Returns:
            Thumbnail concept description
        """
        thumbnail_concepts = {
            'tutorial': [
                "Split-screen showing before/after code results",
                "Person pointing at code on a large screen",
                "Step-by-step visual progress bars",
                "Hand typing on keyboard with code overlay"
            ],
            'news': [
                "Breaking news style with bold red background",
                "Tech headlines with shocked expression",
                "Trending arrows and news ticker style",
                "Professional news anchor setup"
            ],
            'comparison': [
                "Split-screen VS layout with logos",
                "Two products side by side with checkmarks",
                "Battle-style confrontation design",
                "Pros and cons visual comparison"
            ],
            'explanation': [
                "Complex diagram simplified with arrows",
                "Teacher-style whiteboard explanation",
                "Lightbulb moment with clear graphics",
                "Step-by-step visual breakdown"
            ],
            'prediction': [
                "Futuristic crystal ball or fortune teller",
                "Timeline with future milestones",
                "Rocket ship or upward trending charts",
                "Calendar with highlighted future dates"
            ],
            'review': [
                "Product with star ratings overlay",
                "Thumbs up/down with product image",
                "Before and after user experience",
                "Honest review with serious expression"
            ]
        }
        
        concepts = thumbnail_concepts.get(category, ["Clean, professional design with clear text"])
        base_concept = random.choice(concepts)
        
        # Add title-specific elements
        if 'chatgpt' in title.lower():
            base_concept += " with ChatGPT logo"
        elif 'ai' in title.lower():
            base_concept += " with AI/robot elements"
        elif 'python' in title.lower():
            base_concept += " with Python logo"
        
        return base_concept
    
    def _calculate_trend_score(self, title: str, trending_topics: Dict[str, int]) -> float:
        """
        Calculate trend score for a title based on trending topics
        
        Args:
            title: Video title
            trending_topics: Dictionary of trending topics and frequencies
            
        Returns:
            Trend score (0-100)
        """
        title_lower = title.lower()
        score = 0
        
        for topic, frequency in trending_topics.items():
            if topic in title_lower:
                # Weight by topic frequency
                score += frequency * 2
        
        # Bonus for trending keywords
        trending_keywords = ['2024', '2025', 'new', 'latest', 'breakthrough', 'future']
        for keyword in trending_keywords:
            if keyword in title_lower:
                score += 5
        
        return min(score, 100)  # Cap at 100
    
    def _estimate_views(self, trend_score: float, category: str) -> int:
        """
        Estimate potential views based on trend score and category
        
        Args:
            trend_score: Calculated trend score
            category: Video category
            
        Returns:
            Estimated view count
        """
        base_views = {
            'tutorial': 150000,
            'news': 200000,
            'comparison': 180000,
            'explanation': 120000,
            'prediction': 250000,
            'review': 100000
        }
        
        base = base_views.get(category, 150000)
        multiplier = 1 + (trend_score / 100)
        estimated = int(base * multiplier * random.uniform(0.5, 1.5))
        
        return estimated
    
    def _estimate_difficulty(self, category: str, title: str) -> str:
        """
        Estimate content creation difficulty
        
        Args:
            category: Video category
            title: Video title
            
        Returns:
            Difficulty level (Easy/Medium/Hard)
        """
        difficulty_map = {
            'tutorial': 'Medium',
            'news': 'Easy',
            'comparison': 'Medium',
            'explanation': 'Hard',
            'prediction': 'Medium',
            'review': 'Easy'
        }
        
        base_difficulty = difficulty_map.get(category, 'Medium')
        
        # Adjust based on title complexity
        if any(word in title.lower() for word in ['deep', 'advanced', 'complex', 'science']):
            if base_difficulty == 'Easy':
                return 'Medium'
            elif base_difficulty == 'Medium':
                return 'Hard'
        
        return base_difficulty
    
    def _identify_target_audience(self, title: str) -> str:
        """
        Identify target audience based on title
        
        Args:
            title: Video title
            
        Returns:
            Target audience description
        """
        title_lower = title.lower()
        
        if 'beginner' in title_lower or 'first' in title_lower:
            return 'Beginners'
        elif 'advanced' in title_lower or 'expert' in title_lower:
            return 'Advanced users'
        elif 'tutorial' in title_lower or 'how to' in title_lower:
            return 'Learners/Students'
        elif 'news' in title_lower or 'update' in title_lower:
            return 'AI enthusiasts'
        elif 'review' in title_lower:
            return 'Potential buyers'
        else:
            return 'General tech audience'
    
    def _extract_key_topics(self, title: str) -> List[str]:
        """
        Extract key topics from a title
        
        Args:
            title: Video title
            
        Returns:
            List of key topics
        """
        # Common AI/tech keywords to look for
        ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'deep learning',
            'chatgpt', 'gpt', 'openai', 'neural network', 'automation',
            'python', 'coding', 'programming', 'data science', 'tensorflow',
            'pytorch', 'computer vision', 'nlp', 'robotics'
        ]
        
        title_lower = title.lower()
        found_topics = []
        
        for keyword in ai_keywords:
            if keyword in title_lower:
                found_topics.append(keyword.title())
        
        return found_topics[:5]  # Limit to 5 key topics
    
    def generate_video_scripts(self, content_ideas: List[Dict], num_scripts: int = 20) -> List[Dict]:
        """
        Generate video scripts for content ideas
        
        Args:
            content_ideas: List of content idea dictionaries
            num_scripts: Number of scripts to generate
            
        Returns:
            List of video script dictionaries
        """
        print(f"📝 Generating {num_scripts} video scripts...")
        
        scripts = []
        
        # Select top content ideas for script generation
        top_ideas = content_ideas[:num_scripts]
        
        for i, idea in enumerate(top_ideas, 1):
            script = self._generate_script_for_idea(idea)
            
            script_data = {
                'id': i,
                'title': idea['title'],
                'category': idea['category'],
                'script': script,
                'hashtags': idea['hashtags'],
                'thumbnail_concept': idea['thumbnail_concept'],
                'estimated_duration': self._estimate_script_duration(script),
                'word_count': len(script.split()),
                'key_points': self._extract_script_key_points(script),
                'call_to_action': self._generate_call_to_action(idea['category']),
                'created_at': datetime.now().isoformat()
            }
            
            scripts.append(script_data)
        
        print(f"✅ Generated {len(scripts)} video scripts")
        return scripts
    
    def _generate_script_for_idea(self, idea: Dict) -> str:
        """
        Generate a script for a content idea
        
        Args:
            idea: Content idea dictionary
            
        Returns:
            Generated script text
        """
        category = idea['category']
        title = idea['title']
        
        # Script templates by category
        if category == 'tutorial':
            return self._generate_tutorial_script(title)
        elif category == 'news':
            return self._generate_news_script(title)
        elif category == 'comparison':
            return self._generate_comparison_script(title)
        elif category == 'explanation':
            return self._generate_explanation_script(title)
        elif category == 'prediction':
            return self._generate_prediction_script(title)
        elif category == 'review':
            return self._generate_review_script(title)
        else:
            return self._generate_general_script(title)
    
    def _generate_tutorial_script(self, title: str) -> str:
        """Generate a tutorial script"""
        return f"""
Welcome back to the channel! Today we're going to {title.lower()}.

If you're new here, I'm your host and I help people master AI and technology. Make sure to subscribe and hit the notification bell for more content like this.

Let's dive right in. In this tutorial, I'll walk you through everything step by step.

First, let me show you what we're building today. [SHOW DEMO]

Now, let's break this down into manageable steps:

Step 1: Setting Up Your Environment
Before we begin, you'll need to have the following installed...

Step 2: Understanding the Basics
Let me explain the core concepts we'll be using...

Step 3: Implementation
Now let's start coding. I'll explain each line as we go...

Step 4: Testing and Debugging
Let's run our code and see what happens...

Step 5: Optimization and Best Practices
Here are some ways to improve and optimize what we've built...

And that's it! You've successfully completed this tutorial. 

If you found this helpful, please give it a thumbs up and subscribe for more AI tutorials. Drop a comment below if you have any questions or if there's something specific you'd like me to cover next.

Thanks for watching, and I'll see you in the next video!
"""
    
    def _generate_news_script(self, title: str) -> str:
        """Generate a news script"""
        return f"""
What's up everyone! Today I have some incredible news to share with you about {title.lower()}.

Before we jump in, make sure you're subscribed because AI news moves fast and you don't want to miss anything important.

So here's what happened...

This is huge for several reasons. First, it means...

Second, this could completely change how we...

But here's what really caught my attention...

Now, you might be wondering what this means for you. Well...

Looking at the broader implications, this could lead to...

Industry experts are saying...

My take on this is...

What do you think about this development? Let me know in the comments below. Are you excited about this? Concerned? I want to hear your thoughts.

If you enjoyed this breakdown, hit that like button and subscribe for more AI news and analysis. I'll be covering more developments as they happen.

Thanks for watching, and I'll catch you in the next one!
"""
    
    def _generate_comparison_script(self, title: str) -> str:
        """Generate a comparison script"""
        return f"""
Hey everyone! Today we're settling the debate once and for all: {title}

This is one of the most requested comparisons I've gotten, so let's break it down systematically.

First, let me give you a quick overview of both options...

Now, let's compare them across several key criteria:

Performance:
Let me show you some real-world tests...

Ease of Use:
From a user experience perspective...

Cost:
Here's the pricing breakdown...

Features:
Let's look at what each one offers...

Use Cases:
When would you choose one over the other?

Based on all of this testing and analysis, here's my verdict...

The winner depends on your specific needs. If you're looking for X, go with option A. If you need Y, option B is your best bet.

What's your experience been with these tools? Drop a comment and let me know which one you prefer and why.

Don't forget to like this video if it helped you make a decision, and subscribe for more tech comparisons and reviews.

See you next time!
"""
    
    def _generate_explanation_script(self, title: str) -> str:
        """Generate an explanation script"""
        return f"""
Have you ever wondered about {title.lower()}? Today we're going to break it down in simple terms that anyone can understand.

Welcome back to the channel where we make complex technology accessible to everyone. If you're new here, subscribe for more explanations like this.

Let's start with the basics. What exactly is...?

To understand this better, let's use an analogy...

Now, here's where it gets interesting...

The key components are...

Here's how it all works together...

But why does this matter? Well...

The real-world applications are incredible...

Some common misconceptions people have are...

Looking toward the future...

I hope this explanation helped clarify things for you. If you have any questions, drop them in the comments and I'll do my best to answer them.

Like this video if you learned something new, and subscribe for more deep dives into technology and AI.

Thanks for watching!
"""
    
    def _generate_prediction_script(self, title: str) -> str:
        """Generate a prediction script"""
        return f"""
What if I told you that {title.lower()}? 

Today we're looking into the future and I'm going to share some predictions that might surprise you.

Make sure you're subscribed because predicting the future of AI is what we do here, and you don't want to miss what's coming next.

Based on current trends and developments, here's what I see happening...

The evidence for this prediction comes from several sources...

Major companies are already positioning themselves for this shift...

The timeline I'm predicting is...

Here are the key indicators to watch for...

Now, this could go a few different ways...

Scenario 1: If everything goes as expected...

Scenario 2: If there are major breakthroughs...

Scenario 3: If we hit unexpected obstacles...

What does this mean for you? How should you prepare?

My advice is...

Remember, these are predictions based on current data and trends. The future is never certain, but being prepared gives you an advantage.

What do you think? Do you agree with my predictions? Share your thoughts in the comments.

Hit like if you enjoy these future-focused videos, and subscribe for more AI predictions and analysis.

Until next time, keep looking forward!
"""
    
    def _generate_review_script(self, title: str) -> str:
        """Generate a review script"""
        return f"""
I've been using this for weeks now, and today I'm giving you my honest review of {title.lower()}.

Before we start, quick reminder to subscribe if you want more honest tech reviews without the hype.

First impressions when I started using this...

Here's what I love about it...

But here's what frustrated me...

Let me show you how it performs in real-world scenarios...

[DEMO/SCREEN RECORDING]

Pricing and value for money...

How does it compare to alternatives?

Who is this really for?

My final verdict...

Pros:
- [List key advantages]

Cons:
- [List main drawbacks]

Overall rating: X out of 10

Would I recommend it? Here's my take...

That's my honest review. What questions do you have? Drop them in the comments and I'll answer them.

If this review helped you make a decision, please like and subscribe for more honest tech reviews.

Thanks for watching!
"""
    
    def _generate_general_script(self, title: str) -> str:
        """Generate a general script"""
        return f"""
Today we're talking about {title}, and I think you're going to find this really interesting.

Welcome back to the channel! If you're new here, I create content about AI and technology. Make sure to subscribe for more videos like this.

Let me start by explaining why this topic matters...

Here's what most people don't realize...

Let me break this down for you...

The implications of this are huge because...

Here's a real example to illustrate this point...

Now, you might be thinking...

What does this mean for the future?

My take on all of this is...

I'd love to hear your thoughts on this topic. Let me know in the comments what you think.

If you found this video valuable, please give it a like and subscribe for more content about AI and technology.

Thanks for watching, and I'll see you in the next video!
"""
    
    def _estimate_script_duration(self, script: str) -> str:
        """
        Estimate video duration based on script length
        
        Args:
            script: Script text
            
        Returns:
            Estimated duration string
        """
        word_count = len(script.split())
        # Average speaking rate is about 150-160 words per minute
        minutes = word_count / 155
        
        if minutes < 1:
            return "< 1 minute"
        elif minutes < 5:
            return f"{int(minutes)}-{int(minutes)+1} minutes"
        elif minutes < 10:
            return f"{int(minutes)}-{int(minutes)+2} minutes"
        else:
            return f"{int(minutes)}-{int(minutes)+3} minutes"
    
    def _extract_script_key_points(self, script: str) -> List[str]:
        """
        Extract key points from a script
        
        Args:
            script: Script text
            
        Returns:
            List of key points
        """
        # Look for numbered steps, bullet points, or clear sections
        lines = script.split('\n')
        key_points = []
        
        for line in lines:
            line = line.strip()
            if (line.startswith('Step ') or 
                line.startswith('1.') or 
                line.startswith('First,') or
                line.startswith('Second,') or
                line.startswith('Finally,')):
                key_points.append(line)
        
        # If no structured points found, extract sentences with key phrases
        if not key_points:
            sentences = script.split('.')
            for sentence in sentences:
                if any(phrase in sentence.lower() for phrase in 
                      ['important', 'key', 'main', 'crucial', 'essential']):
                    key_points.append(sentence.strip())
        
        return key_points[:5]  # Limit to 5 key points
    
    def _generate_call_to_action(self, category: str) -> str:
        """
        Generate appropriate call-to-action for video category
        
        Args:
            category: Video category
            
        Returns:
            Call-to-action text
        """
        cta_templates = {
            'tutorial': "Try building this yourself and share your results in the comments!",
            'news': "What do you think about this development? Share your thoughts below!",
            'comparison': "Which option do you prefer? Let me know in the comments!",
            'explanation': "Did this help clarify the concept for you? Ask any questions below!",
            'prediction': "Do you agree with my predictions? Share your thoughts!",
            'review': "Are you planning to try this? Let me know what you think!"
        }
        
        return cta_templates.get(category, "What are your thoughts? Share them in the comments!")