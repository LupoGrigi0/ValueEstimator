import openai
import csv
import json

# Set up OpenAI API key
openai.api_key = "PUT KEY HERE"


# Step 0. Initialize an empty list to hold formatted results
formatted_results = []

# Step 0.5. Load responses from the file
with open("responses.json", "r") as json_file:
    responses = json.load(json_file)

# Step 1-2. Iterate through responses and build prompts
for i, response in enumerate(responses, start=1):
    prompt = (
        f"Please process the following response:\n\n{response}\n\n"
        "Extract the lowest value mentioned, summarize the methodology used, "
        "and return the result in the following JSON format:\n"
        "{\n"
        "  \"low_value\": \"\",\n"
        "  \"methodology\": \"\"\n"
        "}\n"
    )
    print(f"Processing Response {i}...")

    # Step 3. Send prompt to OpenAI API
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that processes GPT responses."},
                {"role": "user", "content": prompt}
            ]
        )
        result = completion.choices[0].message.content.strip()

        # Step 4. Parse the result and add to the formatted results
        formatted_results.append({
            "Response Number": i,
            "Raw Response": response,
            "Formatted Result": result
        })
        print(f"Formatted Result for Response {i}: {result}")
    
    except Exception as e:
        print(f"Error processing Response {i}: {e}")
        formatted_results.append({
            "Response Number": i,
            "Raw Response": response,
            "Formatted Result": "Error"
        })

# Step 5. Write formatted results to a CSV file
with open("formatted_results.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Response Number", "Raw Response", "Formatted Result"])  # Headers
    for item in formatted_results:
        writer.writerow([item["Response Number"], item["Raw Response"], item["Formatted Result"]])
print("Formatted results saved to formatted_results.csv")

# Step 6. Print all formatted results
for item in formatted_results:
    print(f"Response Number: {item['Response Number']}")
    print(f"Formatted Result: {item['Formatted Result']}\n")
