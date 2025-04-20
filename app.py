import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAwKSd_btVhnDcxyKHETPfcAMvaK2uqOzY"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main():
  st.set_page_config(page_title="SQL Data Agent", page_icon=":robot_face:")
  st.markdown(
    """

        <div style="text-align: center;">
              <h1>SQL Data Agent 🤖</h1>
              <h4>I am your AI-powered Data Agent to assist you in SQL queries</h4>
              <h5>I am powered by Chain-Of-Thought to generate explanations as well !!!</h5> 
        </div>
    """,
    unsafe_allow_html=True,
  )
  
  text_input = st.text_area("Enter your query here:")

  submit = st.button("Generate")

  if submit:
    with st.spinner("Generating Response ..."):
      
      template = """ Given an input question {text_input}, think step by step and create a syntactically correct query to run.
      Return only the generated query """

      template_formatted = template.format(text_input=text_input)

      response = model.generate_content(template_formatted)
      sql_query = response.text
      # sql_query = sql_query.strip().lstrip("'''sql").rstrip("'''")

      
      expected_output = """ What would be the expected output given the following SQL Query : {sql_query} 
      Return only the tabular result wihtout any explanation """

      expected_output_formatted = expected_output.format(sql_query=sql_query)
      eoutput = model.generate_content(expected_output_formatted)
      gen_eoutput = eoutput.text
    

      explanation = """ Given an input question {text_input}, you thought step by step and returned the query {sql_query}
      as answer. Explain the steps you took to reach the answer. """

      explanation_formatted = explanation.format(text_input=text_input, sql_query=sql_query)
      explanation_output = model.generate_content(explanation_formatted)
      gen_explanation = explanation_output.text
    


      with st.container():
        st.success("Your SQL Query is successfully generated:")
        st.write(sql_query)

        st.success("Expected output of this SQL Query will be:")
        st.markdown(gen_eoutput)

        st.success("Explanation for this query is:")
        st.markdown(gen_explanation)



main()