import pandas as pd
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import streamlit as st

def show():
    # CSS code
    css_code = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .stCheckbox {
            margin-bottom: 15px;
        }
        .stSelectbox {
            margin-bottom: 15px;
        }
        .stNumberInput {
            margin-bottom: 20px;
        }
        .stWarning {
            color: #dc3545;
        }
        .stSuccess {
            color: #28a745;
        }
        .stInfo {
            color: #17a2b8;
        }
        .stSubheader {
            font-size: 24px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .stWrite {
            font-size: 18px;
            margin-bottom: 10px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .activity-container h2 {
            font-size: 22px;
            margin-bottom: 15px;
        }
        .activity-card {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
    </style>
    """

    st.markdown(css_code, unsafe_allow_html=True)  # Embed CSS

    # Load the data
    data = pd.read_csv('res maiti.csv')  # Update this path with your CSV file location

    # Data preprocessing: Handle missing values
    data = data.dropna(subset=['Latitude', 'Longitude', 'Total_score', 'Reviewscount'])

    # Normalize the rating score and review count
    scaler = MinMaxScaler()
    data[['Normalized_Score', 'Normalized_Reviews']] = scaler.fit_transform(
        data[['Total_score', 'Reviewscount']].fillna(0)
    )

    # Define a function to calculate distance between two locations
    def calculate_distance(user_location, place_location):
        return geodesic(user_location, place_location).kilometers

    # Function to filter and rank places based on location, review count, and rating
    def recommend_places(user_lat, user_lon, max_distance_km=5, top_n=10, min_reviews=10):
        user_location = (user_lat, user_lon)

        # Calculate distance of each place from user location
        data['Distance'] = data.apply(
            lambda row: calculate_distance(user_location, (row['Latitude'], row['Longitude'])), axis=1
        )

        # Filter places within the specified maximum distance
        nearby_places = data[data['Distance'] <= max_distance_km]

        if nearby_places.empty:
            return "No places found within the specified distance. Please try a larger distance."

        # Separate places based on review count
        popular_places = nearby_places[nearby_places['Reviewscount'] >= min_reviews]
        new_places = nearby_places[nearby_places['Reviewscount'] < min_reviews]

        if popular_places.empty and new_places.empty:
            return "No places found within the specified distance after filtering. Please try a larger distance."

        # Combine normalized score and review count into a single score for ranking
        popular_places['Combined_Score'] = (
            0.7 * popular_places['Normalized_Reviews'] + 0.3 * popular_places['Normalized_Score']
        )

        new_places['Combined_Score'] = (
            0.7 * new_places['Normalized_Reviews'] + 0.3 * new_places['Normalized_Score']
        )

        # Rank places by the combined score
        ranked_popular_places = popular_places.sort_values(by='Combined_Score', ascending=False).head(top_n)
        ranked_new_places = new_places.sort_values(by='Combined_Score', ascending=False).head(top_n)

        result = {}

        if not ranked_popular_places.empty:
            result['Recommended Places'] = ranked_popular_places[['Place_name', 'Address1', 'Total_score', 'Reviewscount', 'Distance']]

        if not ranked_new_places.empty:
            result['Try Newly Ones'] = ranked_new_places[['Place_name', 'Address1', 'Total_score', 'Reviewscount', 'Distance']]

        return result

    # Streamlit interface
    st.title("Place Recommendation System")

    # User input
    user_lat = st.number_input("Enter your latitude:", format="%.6f")
    user_lon = st.number_input("Enter your longitude:", format="%.6f")
    max_distance_km = st.number_input("Enter the maximum distance (in kilometers) to search for places:", min_value=0.0, step=0.1, format="%.1f")
    top_n = st.number_input("Enter the number of top places to recommend:", min_value=1, step=1)
    min_reviews = st.number_input("Enter the minimum number of reviews for a place to be considered popular:", min_value=0, step=1)

    if st.button("Get Recommendations"):
        if max_distance_km <= 0 or top_n <= 0 or min_reviews < 0:
            st.error("Distance, number of places, and minimum reviews must be positive values.")
        else:
            results = recommend_places(user_lat, user_lon, max_distance_km, top_n, min_reviews)

            if isinstance(results, dict):
                for section, df in results.items():
                    st.subheader(section)
                    st.dataframe(df)
            else:
                st.error(results)

if __name__ == "__main__":
    show()
