# Import Dependencies
import streamlit as st
from openai import OpenAI

class ExcelBot:
    def __init__(self, api_key: str) -> None:
        # Initialize the OpenAI client with the provided API key and base URL
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )

    def get_formula(self, prompt: str, platform: str) -> str:
        """
        Fetches an Excel formula based on the user's query and selected platform.

        :param prompt: User's query for the formula
        :param platform: Selected platform (e.g., Excel, Google Sheets)
        :return: Generated formula as a string
        """
        system_content: str = (
            "You're a Bot developed by Ansh Gupta. You can provide formulas for any query given by the user. "
            "Remember you only need to return the formula without any extra documentation or explanation.\n"
            f"Platform: {platform}"
        )

        # Send the query to the OpenAI model and return the generated formula
        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Combine all chunks of the response into a single string
        return " ".join([chunk.choices[0].delta.content or "" for chunk in completion])

# Initialize the bot with your API key
bot = ExcelBot("YOUR_API_KEY")

# Streamlit UI components
st.title("ExcelBot")
prompt = st.text_input("Enter your query: ")
platform = st.radio("Select the platform: ", ["Excel", "Google Sheets", "Airtable"])

# Generate formula when the button is clicked
if st.button("Generate Formula"):
    if prompt:
        formula = bot.get_formula(prompt, platform)
        if formula:
            st.text_area("Generated Formula:", value=formula, height=100)
        else:
            st.text_area("Unable to generate formula.", height=100)
    else:
        st.error("Please enter a query.")
