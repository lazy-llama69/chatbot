import streamlit as st
import openai
from dotenv import load_dotenv
import os
from google_places import get_price_estimations

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def plan_my_trip():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1rem !important; /* Adjust the top padding */
                padding-left: 6rem;
                padding-right: 6rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center;'>Tell us your travel preferences</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Just provide some basic information, and our trip planner will generate a customized itinerary based on your preferences.</p>", unsafe_allow_html=True)

    left_space, form, right_space = st.columns([1, 4, 1])

    with form:
        # Destination input
        st.markdown("### What is your destination of choice?")
        destination = st.text_input("What is your destination of choice?", placeholder="Enter your destination", label_visibility="collapsed", key="destination_input")

        st.markdown("---")  # Horizontal separator

        # Travel date input
        st.markdown("### When are you planning to travel?")
        travel_date = st.date_input("When are you planning to travel?", format="YYYY-MM-DD", label_visibility="collapsed", key="travel_date_input")

        st.markdown("---")  # Horizontal separator

        # Number of travel days
        st.markdown("### How many days are you planning to travel?")
        num_days = st.number_input("How many days are you planning to travel?", min_value=1, max_value=60, value=7, label_visibility="collapsed", key="num_days_input")

        st.markdown("---")  # Horizontal separator

        # Budget selection
        st.markdown("### What is Your Budget?")
        budget = st.radio("What is Your Budget?", ["Low (0 - 1000 USD)", "Medium (1000 - 2500 USD)", "High (2500+ USD)"], horizontal=True, label_visibility="collapsed", key="budget_input")

        st.markdown("---")  # Horizontal separator

        # Travel companions selection
        st.markdown("### Who do you plan on traveling with on your next adventure?")
        companions = st.multiselect("Who do you plan on traveling with on your next adventure?", ["👤 Solo", "👫 Couple", "👨‍👩‍👧 Family", "👬 Friends"], label_visibility="collapsed", key="companions_input")

        st.markdown("---")  # Horizontal separator

        # Activity selection
        st.markdown("### Which activities are you interested in?")
        activities = st.multiselect(
            "Which activities are you interested in?",
            ["Beaches", "City Sightseeing", "Outdoor Adventures", "Festivals/Events", "Food Exploration", "Nightlife", "Shopping", "Spa Wellness"],
            key="activities_input"
        )

        st.markdown("---")  # Horizontal separator

        # Dietary preferences
        st.markdown("### Would you like to have these options?")
        dietary_options = st.multiselect(" Would you like to have these options?", ["Halal", "Vegetarian"],label_visibility="collapsed", key="dietary_options_input")

        st.markdown("---")  # Horizontal separator

        # Additional requirements section
        st.markdown("### Any additional requirements?")
        additional_requirements = st.text_area(
            "Enter any specific locations, allergens, or preferences:",
            placeholder="E.g., I want to visit the Eiffel Tower, avoid peanuts, need wheelchair accessibility...",
            label_visibility="collapsed", key="additional_requirements_input"
        )

        st.markdown("---")  # Horizontal separator

        # Submit button
        submit = st.button("Submit", key="submit_preferences", help="Generate your custom itinerary")

        if submit:
            # Collect all inputs
            user_preferences = {
                "destination": destination,
                "travel_date": travel_date.strftime("%Y-%m-%d"),
                "num_days": num_days,
                "budget": budget,
                "companions": companions,
                "activities": activities,
                "dietary_options": dietary_options,
                "additional_requirements": additional_requirements
            }

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant."},
                    {"role": "user", "content": f"Generate a custom travel itinerary based on the following preferences: {user_preferences}"}
                ],
                max_tokens=500
            )

            # Extract places from the response
            itinerary = response.choices[0].message["content"]
            places = extract_places(itinerary)

            # Get price estimations for each place
            price_estimations = get_price_estimations(places)

            # Display the generated itinerary with price estimations
            st.markdown("### Your Custom Itinerary")
            st.write(itinerary)
            st.markdown("### Price Estimations")
            st.write(price_estimations)

def extract_places(itinerary):
    # Implement a function to extract place names from the itinerary text
    # This is a placeholder implementation and should be replaced with actual logic
    return ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"]