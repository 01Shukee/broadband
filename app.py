import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="NIGCOMSAT Broadband Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .region-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">📡 NIGCOMSAT Regional Broadband Coverage</h1>', unsafe_allow_html=True)
st.markdown("### Real-time Monitoring of Satellite Broadband Connectivity Across Nigeria")

# Generate sample data
@st.cache_data
def generate_sample_data():
    # Nigerian regions and states
    regions = {
        'North Central': ['Benue', 'Kogi', 'Kwara', 'Nasarawa', 'Niger', 'Plateau', 'FCT'],
        'North East': ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe'],
        'North West': ['Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Sokoto', 'Zamfara'],
        'South East': ['Abia', 'Anambra', 'Ebonyi', 'Enugu', 'Imo'],
        'South South': ['Akwa Ibom', 'Bayelsa', 'Cross River', 'Delta', 'Edo', 'Rivers'],
        'South West': ['Ekiti', 'Lagos', 'Ogun', 'Ondo', 'Osun', 'Oyo']
    }
    
    data = []
    for region, states in regions.items():
        for state in states:
            # Generate realistic coverage data
            population = np.random.randint(500000, 8000000)
            coverage_percentage = np.random.uniform(20, 95)
            connected_users = int(population * (coverage_percentage / 100))
            avg_speed = np.random.uniform(5, 50)
            latency = np.random.uniform(20, 150)
            
            data.append({
                'Region': region,
                'State': state,
                'Population': population,
                'Coverage_Percentage': coverage_percentage,
                'Connected_Users': connected_users,
                'Avg_Speed_Mbps': avg_speed,
                'Latency_ms': latency,
                'Last_Update': datetime.now() - timedelta(days=np.random.randint(0, 30))
            })
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()

# Sidebar filters
st.sidebar.title("📊 Dashboard Filters")
st.sidebar.markdown("---")

# Region filter
selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All Regions"] + list(df['Region'].unique())
)

# Coverage threshold
coverage_threshold = st.sidebar.slider(
    "Minimum Coverage Percentage",
    min_value=0,
    max_value=100,
    value=0
)

# Date filter
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Last Updated")
latest_update = df['Last_Update'].max()
st.sidebar.info(f"🕒 {latest_update.strftime('%Y-%m-%d %H:%M')}")

# Filter data based on selections
filtered_df = df.copy()
if selected_region != "All Regions":
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

filtered_df = filtered_df[filtered_df['Coverage_Percentage'] >= coverage_threshold]

# Main dashboard layout
col1, col2, col3, col4 = st.columns(4)

# Key metrics
with col1:
    total_coverage = filtered_df['Coverage_Percentage'].mean()
    st.metric(
        label="Average Coverage",
        value=f"{total_coverage:.1f}%",
        delta=f"{(total_coverage - df['Coverage_Percentage'].mean()):.1f}%"
    )

with col2:
    total_users = filtered_df['Connected_Users'].sum()
    st.metric(
        label="Total Connected Users",
        value=f"{total_users:,}",
        delta=f"{(total_users/1000000):.1f}M"
    )

with col3:
    avg_speed = filtered_df['Avg_Speed_Mbps'].mean()
    st.metric(
        label="Average Speed",
        value=f"{avg_speed:.1f} Mbps",
        delta=f"{(avg_speed - df['Avg_Speed_Mbps'].mean()):.1f} Mbps"
    )

with col4:
    avg_latency = filtered_df['Latency_ms'].mean()
    st.metric(
        label="Average Latency",
        value=f"{avg_latency:.1f} ms",
        delta=f"{(avg_latency - df['Latency_ms'].mean()):.1f} ms",
        delta_color="inverse"
    )

st.markdown("---")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📈 Coverage Map", "📊 Regional Analysis", "🚀 Performance Metrics", "📋 Raw Data"])

with tab1:
    st.subheader("Broadband Coverage Heatmap")
    
    # Create Nigeria coordinates (approximate)
    nigeria_coords = {
        'North Central': {'lat': 8.5, 'lon': 8.0},
        'North East': {'lat': 10.5, 'lon': 12.5},
        'North West': {'lat': 12.0, 'lon': 8.0},
        'South East': {'lat': 5.5, 'lon': 7.5},
        'South South': {'lat': 5.0, 'lon': 6.0},
        'South West': {'lat': 7.0, 'lon': 4.0}
    }
    
    # Add coordinates to dataframe
    map_df = filtered_df.copy()
    map_df['lat'] = map_df['Region'].map(lambda x: nigeria_coords[x]['lat'] + np.random.uniform(-1, 1))
    map_df['lon'] = map_df['Region'].map(lambda x: nigeria_coords[x]['lon'] + np.random.uniform(-1, 1))
    
    fig_map = px.scatter_mapbox(
        map_df,
        lat='lat',
        lon='lon',
        size="Coverage_Percentage",
        color="Coverage_Percentage",
        hover_name="State",
        hover_data={
            "Region": True,
            "Coverage_Percentage": ":.1f%",
            "Connected_Users": ":,",
            "Avg_Speed_Mbps": ":.1f",
            "lat": False,
            "lon": False
        },
        color_continuous_scale="Viridis",
        size_max=30,
        zoom=5,
        height=500,
        title="Broadband Coverage Across Nigerian Regions"
    )
    
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Coverage by Region")
        
        # Regional coverage bar chart
        regional_avg = filtered_df.groupby('Region').agg({
            'Coverage_Percentage': 'mean',
            'Connected_Users': 'sum',
            'State': 'count'
        }).reset_index()
        
        fig_regional = px.bar(
            regional_avg,
            x='Region',
            y='Coverage_Percentage',
            color='Coverage_Percentage',
            color_continuous_scale='Blues',
            title="Average Coverage Percentage by Region",
            labels={'Coverage_Percentage': 'Coverage %', 'Region': 'Region'}
        )
        st.plotly_chart(fig_regional, use_container_width=True)
    
    with col2:
        st.subheader("User Distribution")
        
        # Pie chart of connected users by region
        regional_users = filtered_df.groupby('Region')['Connected_Users'].sum().reset_index()
        fig_pie = px.pie(
            regional_users,
            values='Connected_Users',
            names='Region',
            title="Connected Users Distribution by Region",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Internet Speed Analysis")
        
        fig_speed = px.box(
            filtered_df,
            x='Region',
            y='Avg_Speed_Mbps',
            color='Region',
            title="Internet Speed Distribution by Region (Mbps)",
            points="all"
        )
        st.plotly_chart(fig_speed, use_container_width=True)
    
    with col2:
        st.subheader("Network Latency Analysis")
        
        fig_latency = px.scatter(
            filtered_df,
            x='Avg_Speed_Mbps',
            y='Latency_ms',
            color='Region',
            size='Coverage_Percentage',
            hover_name='State',
            title="Speed vs Latency Correlation",
            labels={'Avg_Speed_Mbps': 'Speed (Mbps)', 'Latency_ms': 'Latency (ms)'}
        )
        st.plotly_chart(fig_latency, use_container_width=True)

with tab4:
    st.subheader("Raw Coverage Data")
    
    # Display data table - FIXED LINE: Changed {} to []
    st.dataframe(
        filtered_df[[
            'Region', 'State', 'Coverage_Percentage', 
            'Connected_Users', 'Avg_Speed_Mbps', 'Latency_ms', 'Last_Update'
        ]].sort_values('Coverage_Percentage', ascending=False),
        use_container_width=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"nigcomsat_coverage_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "📡 NIGCOMSAT Broadband Monitoring System | "
    "Last Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M") +
    "</div>", 
    unsafe_allow_html=True
)