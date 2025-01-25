from flask import Flask, render_template, request
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

app = Flask(__name__)

# Initialize the API wrapper
api_wrapper = TavilySearchAPIWrapper(tavily_api_key="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")
tool = TavilySearchResults(api_wrapper=api_wrapper)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    product_name = request.form['product_name']
    results = tool.invoke(f"""Search for "{product_name}" across the following websites: Flipkart, Amazon, Myntra, Reliance Digital, Snapdeal, and Croma. For each result, return:
    The URL of the product page. Sort the results by price in ascending order. Ensure the URLs are valid and the prices are accurate for the specified product.
    """)
    
    # Pass the results to the search results page
    return render_template('/searchresults.html', results=results, query=product_name)

# Add any other existing routes here

if __name__ == '__main__':
    app.run(debug=True)
