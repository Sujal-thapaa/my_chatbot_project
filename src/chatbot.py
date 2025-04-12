import openai
import os
from database import read_all_data, load_data_from_csv

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY") or "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"

def analyze_data(data: str, user_instruction: str) -> str:
    """
    Send the data and instructions to the ChatGPT API and return the response.
    
    Args:
        data (str): The data content to analyze.
        user_instruction (str): The instruction/query for the chatbot.
        
    Returns:
        str: The response from the ChatGPT API.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that analyzes provided data."},
        {"role": "user", "content": f"Here is some data:\n{data}\n\nPlease {user_instruction}"}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or your chosen model
            messages=messages,
            max_tokens=250,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def compile_data():
    """
    Reads data from the database and compiles it into a single string.
    """
    rows = read_all_data()
    compiled = ""
    for row in rows:
        # Assuming each row is a tuple in (id, date, content) format
        compiled += f"Record ID {row[0]} (Date: {row[1]}): {row[2]}\n"
    return compiled

def main():
    # Load data from CSV to DB (if not already loaded)
    load_data_from_csv()

    # Compile all data from the DB
    stored_data = compile_data()
    
    # Example instruction
    user_instruction = "summarize the content and provide insights."
    result = analyze_data(stored_data, user_instruction)
    
    print("ChatGPT Analysis:")
    print(result)

if __name__ == "__main__":
    main()
