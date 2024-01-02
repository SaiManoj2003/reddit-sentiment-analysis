from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from textblob import TextBlob  # Ensure you have TextBlob installed
from datetime import datetime

app = FastAPI()

class Comment(BaseModel):
    id: int
    text: str
    polarity_score: float
    classification: str

def get_subfeddit_id(subfeddits, subfeddit_name):
    for subfeddit in subfeddits:
        if subfeddit["title"] == subfeddit_name:
            return subfeddit["id"]
    return None  # Return None if subfeddit name is not found

def filter_comments_by_time_range(comments: List[dict], start_time: int, end_time: int) -> List[dict]:
    filtered_comments = []
    for comment in comments:
        if start_time <= comment["created_at"] <= end_time:
            filtered_comments.append(comment)
    return filtered_comments

@app.get("/comments/{subfeddit_name}")
async def get_comments(
    subfeddit_name: str,
    start_date: str = Query(None, title="Start Date", description="Human-readable Timestamp (YYYY-MM-DD HH:MM:SS)"),
    end_date: str = Query(None, title="End Date", description="Human-readable Timestamp (YYYY-MM-DD HH:MM:SS)"),
    sort_by_polarity: bool = False
) -> List[Comment]:
    # Fetch subfeddits from Feddit API
    subfeddits_response = requests.get("http://localhost:8080/api/v1/subfeddits/?skip=0&limit=10")
    subfeddits = subfeddits_response.json()["subfeddits"]

    # Convert subfeddit name to id
    subfeddit_id = get_subfeddit_id(subfeddits, subfeddit_name)
    if subfeddit_id is None:
        raise HTTPException(status_code=404, detail="Subfeddit not found")

    # Assuming Feddit API provides an endpoint for subfeddit comments using subfeddit_id
    feddit_api_url = f"http://localhost:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&skip=0&limit=10"
    
    params = {"skip": 0, "limit": 25}
    
    # Convert human-readable start_date and end_date to Unix timestamps
    if start_date is not None:
        start_time = int(datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").timestamp())
        params["start_date"] = start_time
    if end_date is not None:
        end_time = int(datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").timestamp())
        params["end_date"] = end_time
    
    # Fetch comments from Feddit API
    response = requests.get(feddit_api_url, params=params)
    feddit_comments = response.json()["comments"]
    
    # Filter comments by time range if specified
    if start_date is not None and end_date is not None:
        feddit_comments = filter_comments_by_time_range(feddit_comments, start_time, end_time)
    
    # Perform sentiment analysis and classify comments using TextBlob
    for comment in feddit_comments:
        blob = TextBlob(comment["text"])
        comment["polarity_score"] = blob.sentiment.polarity
        comment["classification"] = 'positive' if comment["polarity_score"] >= 0 else 'negative'
    
    # Sort comments by polarity if specified
    if sort_by_polarity:
        feddit_comments.sort(key=lambda x: x["polarity_score"], reverse=True)
    
    # Convert Feddit comment format to the desired output format
    result_comments = [
        Comment(
            id=comment["id"],
            text=comment["text"],
            polarity_score=comment["polarity_score"],
            classification=comment["classification"]
        )
        for comment in feddit_comments
    ]
    
    return result_comments
