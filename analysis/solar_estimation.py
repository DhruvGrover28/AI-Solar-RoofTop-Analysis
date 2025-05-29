# analysis/solar_estimation.py
def estimate_panels_and_power(usable_area_m2: float):
    panel_area_m2 = 1.6  # Standard panel size
    panel_wattage = 400  # Each panel produces 400W

    panel_count = int(usable_area_m2 // panel_area_m2)
    total_power_kw = (panel_count * panel_wattage) / 1000  # in kW

    return panel_count, total_power_kw
