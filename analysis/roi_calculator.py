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