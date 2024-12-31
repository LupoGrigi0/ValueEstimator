This is a project that uses chrome web driver automation to, partially, automate the use of a GPT 
Then useses OpenAI's API to processes those results using GPT4-o
The intput to the process is a spreadsheet in CSV format, and the output is also a spreadsheet in CSV format, 

This seample processes uses a GPT to find the resale value of an item described in a field in the input spreadsheet, also provide an explination how it came up with that valuation
The next step GPT4 is used to extract the lowest value from the estimation and then summarize the methodology, and return that as JSON
The final step is simple python code to merge the results from OpenAIProcess into the original spreadsheet and create the EstimatedItemValues.csv
This sample code shows how to use Selenium to automate logging into ChatGPT via GoogleOauth and driving a particular GPT, then processing the output 
Once the prompts have been responded to OpenAI's API is used to refine and format those results. 

BIG TODO for this checking, the OpenAI API is called once for each result, this is wasteful for small datasets, or even large datasets, 
The prompt could/should be changed to take a JSON file process the whole file, and return the resulting CSV file. Although this may take more handholding and fine tuning of the prompt, as well as "chunking" large datasets
