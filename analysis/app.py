# analysis/app.py
import streamlit as st
from image_segmentation import segment_rooftop
from solar_estimation import estimate_panels_and_power
from roi_calculator import calculate_roi
from PIL import Image
import os

st.set_page_config(page_title="AI Solar Rooftop Analyzer", layout="centered")
st.title("\U0001F4BB AI-Powered Rooftop Solar Analysis Tool")

uploaded_file = st.file_uploader("Upload a satelite image of house roof", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Segmenting rooftop and analyzing solar potential..."):
        mask, usable_area_m2, segmentation_confidence = segment_rooftop(image)
        panel_count, power_kw = estimate_panels_and_power(usable_area_m2)
        roi_details = calculate_roi(panel_count, power_kw)

    st.subheader("\U0001F4C8 Rooftop Analysis Results")
    st.image(mask, caption="Rooftop Segmentation", use_container_width=True)
    st.write(f"**Usable Rooftop Area:** {usable_area_m2:.2f} m²")
    st.write(f"**Estimated Panel Count:** {panel_count}")
    st.write(f"**Estimated Power Output:** {power_kw:.2f} kW")
    st.write(f"**Segmentation Confidence:** {segmentation_confidence * 100:.1f}%")

    st.subheader("\U0001F4B0 ROI and Cost Estimates")
    st.write(f"**Installation Cost:** ₹{roi_details['installation_cost']:,}")
    st.write(f"**Estimated Annual Savings:** ₹{roi_details['annual_savings']:,}")
    st.write(f"**Payback Period:** {roi_details['payback_years']:.1f} years")
    st.write(f"**Total 25-Year Savings:** ₹{roi_details['total_savings_25yrs']:,}")












