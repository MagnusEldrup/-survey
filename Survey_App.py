import streamlit as st
import pandas as pd

# Set the title of the web application
st.title("Your Opinion on Redistribution")

st.write("In this section you will get the chance to make a decision on how we should pay two of the other participants in this study. Before you make your decision you please study the following information about the two other participants. The name are fictional but the income and tax information is correct.")

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'highest_cost' not in st.session_state:
    st.session_state.highest_cost = None
if 'highest_cost_2' not in st.session_state:
    st.session_state.highest_cost_2 = None
if 'response_1' not in st.session_state:
    st.session_state.response_1 = None
if 'response_2' not in st.session_state:
    st.session_state.response_2 = None
if 'amount_given_to_b' not in st.session_state:
    st.session_state.amount_given_to_b = None

# Layout with two columns for individuals A and B
if st.session_state.step == 1 or st.session_state.step >= 2 and st.session_state.step < 4:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Daniel")
        st.write("Earns 400,000 Ksh per year")
        st.write("- Does not pay taxes")
        st.image("Avatar.PNG", width=150)

    with col2:
        st.subheader("Michael")
        st.write("Earns 400,000 Ksh per year")
        st.write("- Pays 25,000 Ksh in taxes")
        st.image("Avatar.PNG", width=150)

    if st.session_state.step == 1:
        if st.button("Next", key='next_button'):
            st.session_state.step = 2

if st.session_state.step == 2:
    st.write("After the survey, we draw a random number between 0 and 1,000 Ksh. If you have indicated that the **highest acceptable cost** which is below that number, then no transfer will be made. Otherwise we will make the transfer imposing a cost equal to the number drawn")
    # Slider for user input
    st.session_state.highest_cost = st.slider(
        "Using the slider, please indicate the highest acceptable cost for which you think the transfer is still beneficial:",
        min_value=0,
        max_value=1000,
        value=st.session_state.highest_cost if st.session_state.highest_cost is not None else 250,
        step=50,
        key='highest_cost_slider'
    )

    # Calculate the amount given to B
    st.session_state.amount_given_to_b = 1000 - st.session_state.highest_cost

    # Display the selected highest cost and amount given to B
    amount_given_to_b = st.session_state.amount_given_to_b  # For convenience
    highest_cost = st.session_state.highest_cost
    st.write(f"<div style='text-align: center; font-weight: bold;'>We take 1,000 Ksh from Daniel and give at least {amount_given_to_b} Ksh to Michael</div><br>", unsafe_allow_html=True)
    st.write(f"The highest acceptable cost for the transfer is {highest_cost} Ksh")
    st.write(f"The amount given to Michael is at least {amount_given_to_b} Ksh")

    # Move to confirmation screen
    if st.button("Proceed to Confirmation", key='proceed_button'):
        st.session_state.step = 3

if st.session_state.step == 3:
    # Ensure the amount_given_to_b is recalculated from the previous step
    highest_cost = st.session_state.get('highest_cost', 250)
    amount_given_to_b = 1000 - highest_cost

    st.write("## Confirm Your Choices")

    # Question 1
    amount_given_to_michael_q1 = amount_given_to_b - 50 if amount_given_to_b > 5 else 0
    st.write(f"**It is good to take 1,000 Ksh from Daniel and give {amount_given_to_michael_q1} Ksh to Michael**")

    # Options for the radio buttons
    options = ("Agree", "Disagree")

    # Map stored responses to index
    index_response_1 = options.index(st.session_state.response_1) if st.session_state.response_1 in options else 0
    st.session_state.response_1 = st.radio(
        "Do you agree?",
        options,
        index=index_response_1,
        key="response_1_radio"
    )

    # Question 2
    amount_given_to_michael_q2 = amount_given_to_b + 50
    st.write(f"**It is good to take 1,000 Ksh from Daniel and give {amount_given_to_michael_q2} Ksh to Michael**")
    index_response_2 = options.index(st.session_state.response_2) if st.session_state.response_2 in options else 0
    st.session_state.response_2 = st.radio(
        "Do you agree?",
        options,
        index=index_response_2,
        key="response_2_radio"
    )

    # Confirm and save response
    if st.button("Confirm and Save Response", key='confirm_save_response_button') and st.session_state.step == 3:
        # Retrieve responses from session state
        response_1 = st.session_state.response_1
        response_2 = st.session_state.response_2

        if response_1 == 'Disagree' and response_2 == 'Agree':
            # Save responses to CSV
            data = {
                'Highest Cost (second)': [st.session_state.highest_cost_2 or 'N/A'],
                'Highest Cost (first)': [highest_cost],
                'Amount Given to B': [amount_given_to_b],
                'Response 1': [response_1],
                'Response 2': [response_2]
            }
            df = pd.DataFrame(data)
            df.to_csv('responses.csv', mode='a', header=False, index=False)
            st.success("Response saved successfully!")
            # Proceed to next step
            st.session_state.step = 4
        elif response_1 == 'Agree' and response_2 == 'Agree':
            st.error(f"**In the first question, you indicated that the highest acceptable cost was {highest_cost}. However, in the next question, you mentioned you'd accept a cost of {highest_cost + 50}. Please review and confirm your preference.**")
            # Ensure 'highest_cost_2' is initialized
            if st.session_state.highest_cost_2 is None:
                st.session_state.highest_cost_2 = highest_cost

            # Use a form to group the slider and submit button
            with st.form(key='highest_cost_2_form'):
                st.session_state.highest_cost_2 = st.slider(
                    "Using the slider, please indicate the highest acceptable cost for which you think the transfer is still beneficial:",
                    min_value=0,
                    max_value=1000,
                    value=st.session_state.highest_cost_2,
                    step=50,
                    key='highest_cost_2_slider'
                )
                confirm_submit = st.form_submit_button("Confirm and Submit")
                if confirm_submit:
                    # Save responses to CSV
                    data = {
                        'Highest Cost (second)': [st.session_state.highest_cost_2],
                        'Highest Cost (first)': [highest_cost],
                        'Response 1': [response_1],
                        'Response 2': [response_2]
                    }
                    df = pd.DataFrame(data)
                    df.to_csv('responses.csv', mode='a', header=False, index=False)
                    st.success("Response saved successfully!")
                    # Proceed to next step
                    st.session_state.step = 4
        else:
            st.error("Your responses are inconsistent. Please adjust your answers and try again.")
            # Allow the user to adjust inputs

if st.session_state.step == 4:
    st.write("Thank you for your participation. Your response has been recorded.")
    st.write("Please click the button below to exit the survey.")
    if st.button("Exit Survey", key='exit_button'):
        st.session_state.clear()  # Reset session state
        st.write("You have successfully exited the survey.")