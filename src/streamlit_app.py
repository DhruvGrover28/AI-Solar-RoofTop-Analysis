# app.py
import streamlit as st
from analysis.image_segmentation import segment_rooftop
from analysis.solar_estimation import estimate_panels_and_power
from analysis.roi_calculator import calculate_roi
from PIL import Image
import os

st.set_page_config(page_title="AI Solar Rooftop Analyzer", layout="centered")
st.title("\U0001F4BB AI-Powered Rooftop Solar Analysis Tool")

uploaded_file = st.file_uploader("Upload a rooftop satellite image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Segmenting rooftop and analyzing solar potential..."):
        mask, usable_area_m2, segmentation_confidence = segment_rooftop(image)
        panel_count, power_kw = estimate_panels_and_power(usable_area_m2)
        roi_details = calculate_roi(panel_count, power_kw)

    st.subheader("\U0001F4C8 Rooftop Analysis Results")
    st.image(mask, caption="Rooftop Segmentation", use_column_width=True)
    st.write(f"**Usable Rooftop Area:** {usable_area_m2:.2f} m²")
    st.write(f"**Estimated Panel Count:** {panel_count}")
    st.write(f"**Estimated Power Output:** {power_kw:.2f} kW")
    st.write(f"**Segmentation Confidence:** {segmentation_confidence * 100:.1f}%")

    st.subheader("\U0001F4B0 ROI and Cost Estimates")
    st.write(f"**Installation Cost:** ₹{roi_details['installation_cost']:,}")
    st.write(f"**Estimated Annual Savings:** ₹{roi_details['annual_savings']:,}")
    st.write(f"**Payback Period:** {roi_details['payback_years']:.1f} years")
    st.write(f"**Total 25-Year Savings:** ₹{roi_details['total_savings_25yrs']:,}")


# analysis/image_segmentation.py
import numpy as np
import cv2
from PIL import Image

def segment_rooftop(image: Image.Image):
    # Convert to NumPy array and resize
    img = np.array(image.convert('RGB'))
    img = cv2.resize(img, (512, 512))

    # Dummy segmentation logic (placeholder for AI model like SAM or U-Net)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    mask_colored = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    # Calculate usable area (mock logic, assume 1px = 0.25m² and 70% efficiency)
    total_white_pixels = np.sum(mask == 255)
    area_per_pixel_m2 = 0.25
    usable_area_m2 = total_white_pixels * area_per_pixel_m2 * 0.7

    # Confidence mock (use mean brightness as proxy)
    confidence = np.mean(gray) / 255

    return Image.fromarray(mask_colored), usable_area_m2, confidence


# analysis/solar_estimation.py
def estimate_panels_and_power(usable_area_m2: float):
    panel_area_m2 = 1.6  # Standard panel size
    panel_wattage = 400  # Each panel produces 400W

    panel_count = int(usable_area_m2 // panel_area_m2)
    total_power_kw = (panel_count * panel_wattage) / 1000  # in kW

    return panel_count, total_power_kw


# analysis/roi_calculator.py
def calculate_roi(panel_count: int, power_kw: float):
    cost_per_panel = 20000  # ₹ per panel
    annual_sun_hours = 1500  # average sunlight hours/year
    unit_rate = 8  # ₹ per kWh

    installation_cost = panel_count * cost_per_panel
    annual_generation_kwh = power_kw * annual_sun_hours
    annual_savings = annual_generation_kwh * unit_rate
    payback_years = installation_cost / annual_savings if annual_savings else 0
    total_savings_25yrs = annual_savings * 25

    return {
        "installation_cost": int(installation_cost),
        "annual_savings": int(annual_savings),
        "payback_years": payback_years,
        "total_savings_25yrs": int(total_savings_25yrs)
    }


# example output (mock)
# Input image: 120m² usable area
# → 75 panels
# → 30 kW power output
# → ₹15,00,000 installation cost
# → ₹3,60,000 annual savings
# → Payback in ~4.2 years
# → ₹90,00,000 savings in 25 years



