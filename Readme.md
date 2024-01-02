# FastAPI Reddit Comments Sentiment Analysis

This FastAPI application provides an interface to analyze the sentiment of comments in a given Feddit subfeddit. The sentiment analysis is performed using the TextBlob library.

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SaiManoj2003/reddit-sentiment-analysis.git
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the FastAPI application:**

    ```bash
    uvicorn a:app --reload
    ```

4. The FastAPI application should now be accessible at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI documentation and [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for ReDoc documentation.

## Endpoints

### Get Comments for a Subfeddit

- **Endpoint:** `/comments/{subfeddit_name}`
- **Parameters:**
  - `subfeddit_name` (path parameter): The name of the subfeddit for which you want to retrieve comments.
  - `start_date` (query parameter, optional): Start date for filtering comments (Human-readable Timestamp - "YYYY-MM-DD HH:MM:SS").
  - `end_date` (query parameter, optional): End date for filtering comments (Human-readable Timestamp - "YYYY-MM-DD HH:MM:SS").
  - `sort_by_polarity` (query parameter, optional): Boolean flag to sort comments by polarity score.
- **Response:** List of comments with the following details:
  - `id`: Unique identifier of the comment.
  - `text`: Content of the comment.
  - `polarity_score`: Sentiment polarity score.
  - `classification`: Sentiment classification ("positive" or "negative").

## Important Notes

- Ensure that the Feddit API is running. If the Feddit API is on a different host or port, update the `feddit_api_url` variable in the `get_comments` function accordingly.