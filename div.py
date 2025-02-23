from yahooquery import Ticker
import nltk
from transformers import pipeline


def get_company_summary(symbol):
        stock = Ticker(symbol)
        summary = stock.asset_profile[symbol]['longBusinessSummary']
        return f"{summary}"

symbol = "NVDA"  

company_summary = get_company_summary(symbol)

nltk.download('punkt')

summarizer = pipeline("summarization")

def simple_summarizer(text):
    summary = summarizer(text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
    simpler_summarizer = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    summary = simpler_summarizer(f"Explain this in simple words: {summary}", max_length=30, min_length=5, do_sample=False)[0]['generated_text']
    
    return summary

summary = simple_summarizer(company_summary)
print(summary)