import praw
import pandas as pd
import time
import random
from datetime import datetime

# Replace these with your own credentials
client_id = 'your_client_Id'  # Your client ID
client_secret = 'your_client_secret'  # Your client secret
user_agent = 'user_agent'  # Custom user agent string

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Target subreddit
subreddit_name = 'any_topic'
posts = []

# Limit for the number of posts to collect
post_limit = 3000

# Fetch posts from the subreddit
subreddit = reddit.subreddit(subreddit_name)
count = 0

for submission in subreddit.new(limit=post_limit):
    if count >= post_limit:
        break

    # Collect post data
    post_data = {
        'title': submission.title,
        'score': submission.score,
        'id': submission.id,
        'url': submission.url,
        'num_comments': submission.num_comments,
        'created': datetime.fromtimestamp(submission.created_utc),
        'body': submission.selftext,
        'author': submission.author.name if submission.author else 'deleted'
    }

    # Collect author details if available
    if submission.author:
        try:
            author = reddit.redditor(submission.author.name)
            # Check if the attributes exist before accessing them
            post_data['post_karma'] = getattr(author, 'link_karma', None)
            post_data['comment_karma'] = getattr(author, 'comment_karma', None)
            post_data['cake_day'] = datetime.fromtimestamp(author.created_utc) if hasattr(author, 'created_utc') else None
        except Exception as e:
            print(f"Error fetching details for user {submission.author.name}: {e}")
            post_data['post_karma'] = None
            post_data['comment_karma'] = None
            post_data['cake_day'] = None
    else:
        post_data['post_karma'] = None
        post_data['comment_karma'] = None
        post_data['cake_day'] = None

    posts.append(post_data)
    count += 1

    # Random pause between 1 and 2 seconds
    time.sleep(random.uniform(1, 2))

# Create a DataFrame and save the data to a CSV file
df = pd.DataFrame(posts)
df.to_csv('reddit_posts.csv', index=False)

print("Data has been successfully saved to reddit_posts.csv")
