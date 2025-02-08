# myapp/services.py

def calculate_revenue_share(total_revenue):
    if total_revenue <= 29000:
        percentage = 30
    elif total_revenue <= 30000:
        percentage = 40
    elif total_revenue <= 50000:
        percentage = 45
    else:
        percentage = 50  # Optionally, add a default for revenues above $50,000

    return percentage
