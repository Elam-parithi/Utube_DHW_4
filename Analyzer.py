import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


def analyze_sentiment(Input_txt):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(Input_txt)
    return sentiment_scores


if __name__ == '__main__':
    sample_texts = [
        "I love this product! It's absolutely wonderful.",
        "This is the worst experience I've ever had.",
        "I'm feeling okay about the results.",
        "The movie was not bad, but it wasn't great either."
    ]

    for text in sample_texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: {text}\nSentiment: {sentiment}\n")
