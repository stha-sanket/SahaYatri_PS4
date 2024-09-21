import streamlit as st
import base64

# Define the min and max costs for each category
# Chitwan
chitwan_activities = {
    "Jungle Safari": (100, 200),
    "Elephant Ride": (30, 150),
    "Canoeing": (30, 50),
    "Fishing": (10, 50),
    "Tharu Museum": (5, 10)
}

chitwan_guides = {
    "Full-time Guide": (400, 600),
    "Cultural Guide": (250, 300),
    "Trekking Guide": (350, 500)
}

chitwan_accommodations = {
    "Homestay": (10, 50),
    "Basic Lodge": (15, 50),
    "Luxury Lodge": (100, 300),
    "Basic Hotel": (15, 30),
    "Luxury Hotel": (100, 400)
}

# Everest
everest_activities = {
    "Sherpa Village Tour": (100, 150),
    "Everest Summit Path": (150, 200),
    "Helicopter Tour": (1000, 1200),
    "Camping in Base Camp": (400, 500),
    "Mountain Flight": (250, 300)
}

everest_guides = {
    "Full-time Guide": (450, 500),
    "Cultural Guide": (250, 300),
    "Trekking Guide": (350, 400)
}

everest_porters = {
    "Full-time Porter": (180, 200),
    "Halfway Porter": (90, 100),
    "Multiple Porters": (300, 350)
}

everest_accommodations = {
    "Homestay": (15, 20),
    "Basic Lodge": (40, 50),
    "Luxury Lodge": (130, 150),
    "Basic Hotel": (70, 80),
    "Luxury Hotel": (180, 200)
}

# Lumbini
lumbini_activities = {
    "Lumbini Museum": (10, 20),
    "Ashok Pillar": (5, 10),
    "Cycling": (2, 5),
    "Meditation": (5, 15)
}

lumbini_guides = {
    "Full-time Guide": (300, 450),
    "Cultural Guide": (150, 300),
}

lumbini_accommodations = {
    "Homestay": (5, 50),
    "Basic Lodge": (8, 20),
    "Luxury Lodge": (60, 140),
    "Basic Hotel": (8, 30),
    "Luxury Hotel": (75, 200)
}

# Pokhara
pokhara_activities = {
    "Boating": (5, 30),
    "Paragliding": (70, 150),
    "Rafting": (20, 100),
    "Zip Lining": (50, 120),
    "Hot Air Balloon": (90, 200),
    "Bungee Jumping": (70, 120)
}

pokhara_guides = {
    "Full-time Guide": (450, 500),
    "Cultural Guide": (250, 300),
    "Trekking Guide": (350, 400)
}

pokhara_accommodations = {
    "Homestay": (10, 60),
    "Basic Lodge": (8, 20),
    "Luxury Lodge": (100, 300),
    "Basic Hotel": (10, 40),
    "Luxury Hotel": (100, 400)
}

# Function to calculate the total cost
def calculate_total(selected_options):
    return sum(selected_options.values())

# Function to encode images to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# CSS code
css_code = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        color: #333;
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
    .doctor-card {
        width: 300px;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        background-color: #fff;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 250px;
    }
    .doctor-image {
        border-radius: 10%;
        width: 350px;
        height: 150px;
        object-fit: cover;
        margin: 0 auto 15px;
    }
    .doctor-info {
        font-size: 14px;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .doctor-name {
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
        color: #ff0000;
    }
    .doctor-position {
        color: #555;
        margin-top: 5px;
        font-size: 13px;
    }
    .doctor-nmc {
        color: #888;
        margin-top: 5px;
        font-size: 12px;
    }
    @media (max-width: 600px) {
        .reason {
            flex: 1 1 100%;
        }
    }
</style>
"""

# Main function for Streamlit
def show():
    st.markdown(css_code, unsafe_allow_html=True)  # Embed CSS
    st.image('wow.jpg')
    st.title("Nepal Trip Budget Calculator")

    doctors = [
        {"name": "Pokhare", "image": "pokhara.jpg"},
        {"name": "Everest", "image": "everest.png"},
        {"name": "Chitwan", "image": "chit.png"},
        {"name": "Lumbini", "image": "lumbini.jpg"}
    ]

    # Displaying doctors in a grid layout with two columns
    for i in range(0, len(doctors), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(doctors):
                doctor = doctors[i + j]
                with cols[j]:
                    image_base64 = get_image_base64(doctor['image'])
                    st.markdown(f"""
                        <div class="doctor-card">
                            <div>
                                <img src="data:image/jpeg;base64,{image_base64}" class="doctor-image" alt="{doctor['name']}">
                                <div class="doctor-info">
                                    <div class="doctor-name">{doctor['name']}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")

    # Select Destination
    destination = st.selectbox("Choose your destination:", ["Chitwan", "Everest", "Lumbini", "Pokhara"])

    # Get the user's budget
    budget = st.number_input("Enter your budget:", min_value=0, step=10, value=1000)

    selected_options = {}

    # Define the data based on the selected destination
    if destination == "Chitwan":
        activities = chitwan_activities
        guides = chitwan_guides
        accommodations = chitwan_accommodations
    elif destination == "Everest":
        activities = everest_activities
        guides = everest_guides
        accommodations = everest_accommodations
        porters = everest_porters
    elif destination == "Lumbini":
        activities = lumbini_activities
        guides = lumbini_guides
        accommodations = lumbini_accommodations
    elif destination == "Pokhara":
        activities = pokhara_activities
        guides = pokhara_guides
        accommodations = pokhara_accommodations

    # Select Activities
    st.subheader("Select Activities:")
    for activity, (min_cost, max_cost) in activities.items():
        if st.checkbox(f"Add {activity} (Cost: ${min_cost}-${max_cost})"):
            selected_options[activity] = max_cost

    # Select a Guide
    st.subheader("Select a Guide:")
    guide_options = {guide: f"${min_cost}-${max_cost}" for guide, (min_cost, max_cost) in guides.items()}
    selected_guide = st.selectbox("Choose a Guide:", list(guide_options.keys()), format_func=lambda x: f"{x} ({guide_options[x]})")
    if selected_guide:
        selected_options['Guide'] = guides[selected_guide][1]

    # Select a Porter (if applicable)
    if destination == "Everest":
        st.subheader("Select a Porter:")
        porter_options = {porter: f"${min_cost}-${max_cost}" for porter, (min_cost, max_cost) in porters.items()}
        selected_porter = st.selectbox("Choose a Porter:", list(porter_options.keys()), format_func=lambda x: f"{x} ({porter_options[x]})")
        if selected_porter:
            selected_options['Porter'] = porters[selected_porter][1]

    # Select Accommodation
    st.subheader("Select Accommodation:")
    accommodation_options = {accommodation: f"${min_cost}-${max_cost}" for accommodation, (min_cost, max_cost) in accommodations.items()}
    selected_accommodation = st.selectbox("Choose Accommodation:", list(accommodation_options.keys()), format_func=lambda x: f"{x} ({accommodation_options[x]})")
    if selected_accommodation:
        selected_options['Accommodation'] = accommodations[selected_accommodation][1]

    # Calculate the total cost
    total_cost = calculate_total(selected_options)

    # Display the total cost and comparison with the budget
    st.write(f"### Total Estimated Cost: ${total_cost}")

    if total_cost <= budget:
        st.write("### :green[Your selections are within the budget!]")
        if st.button("Book this Package"):
            st.success("Package successfully booked!")
    else:
        st.write("### :red[Your selections exceed the budget. Please adjust your options.]")
        # this will change
if __name__ == "__main__":
    show()
