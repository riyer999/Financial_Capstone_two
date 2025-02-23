from yahooquery import Ticker
import nltk
from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration

def get_company_summary(symbol):
        stock = Ticker(symbol)
        summary = stock.asset_profile[symbol]['longBusinessSummary']
        return f"{summary}"

symbol = "AAPL"  

company_summary = get_company_summary(symbol)


nltk.download('punkt')

summarizer = pipeline("summarization", model="human-centered-summarization/financial-summarization-pegasus")

def simple_summarizer(text):
    summary = summarizer(text, max_length=150, min_length=10, do_sample=False)[0]['summary_text']
    
    
    
    return summary

summary = simple_summarizer(company_summary)
print(summary)