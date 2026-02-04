import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import folium
from streamlit_folium import st_folium
from services.weather_service import WeatherService

st.set_page_config(page_title="Monitoring Cuaca", page_icon="🌡️", layout="wide")

st.title("🌡️ Monitoring Cuaca & Iklim")
st.markdown("**Pantau cuaca real-time untuk keputusan budidaya yang tepat**")

# Location selector
st.subheader("📍 Pilih Lokasi")

col_loc1, col_loc2 = st.columns([1, 2])

with col_loc1:
    location_name = st.selectbox(
        "Lokasi",
        list(WeatherService.LOCATIONS.keys()),
        help="Pilih lokasi atau gunakan custom coordinates"
    )
    
    use_custom = st.checkbox("Gunakan koordinat custom")
    
    if use_custom:
        custom_lat = st.number_input("Latitude", value=-6.2088, step=0.0001, format="%.4f")
        custom_lon = st.number_input("Longitude", value=106.8456, step=0.0001, format="%.4f")
        lat, lon = custom_lat, custom_lon
    else:
        location = WeatherService.LOCATIONS[location_name]
        lat, lon = location['lat'], location['lon']

with col_loc2:
    # Create Folium map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=10,
        tiles="OpenStreetMap"
    )
    
    # Add marker
    folium.Marker(
        [lat, lon],
        popup=f"<b>{location_name if not use_custom else 'Custom Location'}</b><br>Lat: {lat}<br>Lon: {lon}",
        tooltip="Lokasi Terpilih",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add click handler for custom location
    m.add_child(folium.LatLngPopup())
    
    # Display map
    map_data = st_folium(m, width=700, height=300)
    
    # Update coordinates if map clicked
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        
        st.info(f"📍 Lokasi dari peta: Lat {clicked_lat:.4f}, Lon {clicked_lon:.4f}")
        
        if st.button("Gunakan Lokasi Ini"):
            lat, lon = clicked_lat, clicked_lon
            st.session_state.weather_data = None
            st.rerun()

# Fetch weather data
if st.button("🔄 Refresh Data Cuaca", type="primary"):
    st.session_state.weather_data = None

if 'weather_data' not in st.session_state or st.session_state.weather_data is None:
    with st.spinner("Mengambil data cuaca..."):
        st.session_state.weather_data = WeatherService.get_weather(lat, lon)

weather_data = st.session_state.weather_data
current = weather_data['current']
forecast = weather_data['forecast']

# Current Weather
st.markdown("---")
st.header("☀️ Cuaca Saat Ini")

col_w1, col_w2, col_w3, col_w4, col_w5 = st.columns(5)

with col_w1:
    st.metric(
        "🌡️ Suhu",
        f"{current['temperature']}°C",
        delta=f"Terasa {current['feels_like']}°C"
    )

with col_w2:
    st.metric(
        "💧 Kelembaban",
        f"{current['humidity']}%"
    )

with col_w3:
    st.metric(
        "🌧️ Curah Hujan",
        f"{current['rainfall']} mm"
    )

with col_w4:
    st.metric(
        "💨 Kecepatan Angin",
        f"{current['wind_speed']} km/h"
    )

with col_w5:
    st.info(f"**Kondisi:**\n\n{current['condition']}")

st.caption(f"Terakhir update: {current['timestamp'].strftime('%Y-%m-%d %H:%M')}")

# Weather Alerts
alerts = WeatherService.check_alerts(weather_data)

if alerts:
    st.markdown("---")
    st.header("⚠️ Peringatan Cuaca")
    
    for alert in alerts:
        severity_colors = {
            'Tinggi': 'error',
            'Sedang': 'warning',
            'Rendah': 'info'
        }
        
        with st.expander(f"{alert['type']} - {alert['severity']} ({alert['date']})"):
            st.write(f"**Deskripsi:** {alert['description']}")
            st.write(f"**Dampak:** {alert['impact']}")
            st.write("**Tindakan yang Disarankan:**")
            for action in alert['actions']:
                st.write(f"- {action}")

# 7-Day Forecast
st.markdown("---")
st.header("📅 Prakiraan 7 Hari")

# Forecast table
df_forecast = pd.DataFrame(forecast)
df_forecast['Tanggal'] = pd.to_datetime(df_forecast['date']).dt.strftime('%d %b')
df_forecast['Suhu Min-Max'] = df_forecast.apply(
    lambda x: f"{x['temp_min']}°C - {x['temp_max']}°C", axis=1
)
df_forecast['Hujan'] = df_forecast.apply(
    lambda x: f"{x['rainfall']}mm ({x['rainfall_prob']}%)", axis=1
)
df_forecast['Angin'] = df_forecast['wind_speed'].apply(lambda x: f"{x} km/h")

display_df = df_forecast[['Tanggal', 'condition', 'Suhu Min-Max', 'Hujan', 'Angin']].copy()
display_df.columns = ['Tanggal', 'Kondisi', 'Suhu', 'Hujan (Prob)', 'Angin']

st.dataframe(display_df, width="stretch", hide_index=True)

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Temperature chart
    fig_temp = go.Figure()
    
    fig_temp.add_trace(go.Scatter(
        x=df_forecast['Tanggal'],
        y=df_forecast['temp_max'],
        mode='lines+markers',
        name='Suhu Maksimum',
        line=dict(color='#E74C3C', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=df_forecast['Tanggal'],
        y=df_forecast['temp_min'],
        mode='lines+markers',
        name='Suhu Minimum',
        line=dict(color='#3498DB', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.update_layout(
        title='Tren Suhu 7 Hari',
        xaxis_title='Tanggal',
        yaxis_title='Suhu (°C)',
        hovermode='x unified',
        height=350
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)

with col_chart2:
    # Rainfall chart
    fig_rain = go.Figure()
    
    fig_rain.add_trace(go.Bar(
        x=df_forecast['Tanggal'],
        y=df_forecast['rainfall'],
        name='Curah Hujan',
        marker_color='#3498DB',
        text=df_forecast['rainfall'],
        textposition='outside'
    ))
    
    fig_rain.update_layout(
        title='Prakiraan Curah Hujan',
        xaxis_title='Tanggal',
        yaxis_title='Curah Hujan (mm)',
        height=350
    )
    
    st.plotly_chart(fig_rain, use_container_width=True)

# Spray Recommendations
st.markdown("---")
st.header("💦 Rekomendasi Penyemprotan")

spray_recs = WeatherService.get_spray_recommendations(weather_data)

for rec in spray_recs:
    status_colors = {
        'Ideal': '🟢',
        'Cukup Baik': '🟡',
        'Kurang Ideal': '🟠',
        'Tidak Disarankan': '🔴'
    }
    
    icon = status_colors.get(rec['status'], '⚪')
    
    col_r1, col_r2, col_r3 = st.columns([1, 2, 2])
    
    with col_r1:
        st.write(f"**{rec['day_name']}**")
        st.caption(rec['date'])
    
    with col_r2:
        st.write(f"{icon} **{rec['status']}**")
    
    with col_r3:
        st.write(rec['reason'])

st.info("""
💡 **Tips Penyemprotan:**
- Semprot pagi (06:00-09:00) atau sore (16:00-18:00)
- Hindari saat angin kencang (>15 km/h)
- Jangan semprot jika hujan diprediksi dalam 6 jam
- Gunakan APD lengkap
""")

# Integration Links
st.markdown("---")
st.header("🔗 Integrasi dengan Modul Lain")

col_int1, col_int2, col_int3 = st.columns(3)

with col_int1:
    st.info("""
    **💦 Strategi Penyemprotan**
    - Lihat jadwal spray
    - Cek dosis pestisida
    - Rotasi treatment
    """)

with col_int2:
    st.info("""
    **📅 Kalender Tanam**
    - Jadwal aktivitas
    - Timing optimal
    - Milestone tracking
    """)

with col_int3:
    st.info("""
    **📔 Jurnal Budidaya**
    - Log aktivitas
    - Catat kondisi cuaca
    - Track dampak cuaca
    """)

# Footer
st.markdown("---")
st.caption("""
**Data Source:** Open-Meteo API (https://open-meteo.com/)  
**Update Frequency:** Real-time (refresh manual)  
**Coverage:** Global weather data
""")
