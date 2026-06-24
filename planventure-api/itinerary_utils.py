from datetime import datetime, timedelta


def generate_default_itinerary(destination: str, start_date, end_date) -> str:
    """Generate a default itinerary template based on trip duration.

    Args:
        destination: The trip destination name
        start_date: Trip start date (datetime.date)
        end_date: Trip end date (datetime.date)

    Returns:
        A formatted itinerary template string
    """
    if not start_date or not end_date:
        return ""

    # Convert to date objects if needed
    if hasattr(start_date, "date"):
        start_date = start_date.date()
    if hasattr(end_date, "date"):
        end_date = end_date.date()

    num_days = (end_date - start_date).days + 1
    itinerary_lines = [f"Trip to {destination} - {num_days} days\n"]
    itinerary_lines.append("=" * 50)

    current_date = start_date
    day_number = 1

    while current_date <= end_date:
        date_str = current_date.strftime("%A, %B %d, %Y")
        itinerary_lines.append(f"\nDay {day_number}: {date_str}")
        itinerary_lines.append("-" * 40)

        # Add activity placeholders based on day
        if day_number == 1:
            itinerary_lines.append("• Arrival and check-in")
            itinerary_lines.append("• Explore local area")
            itinerary_lines.append("• Dinner at a local restaurant")
        elif day_number == num_days:
            itinerary_lines.append("• Final activities")
            itinerary_lines.append("• Packing and checkout")
            itinerary_lines.append("• Departure")
        else:
            itinerary_lines.append("• Morning activity")
            itinerary_lines.append("• Lunch break")
            itinerary_lines.append("• Afternoon exploration")
            itinerary_lines.append("• Evening activity")

        current_date += timedelta(days=1)
        day_number += 1

    itinerary_lines.append("\n" + "=" * 50)
    itinerary_lines.append("Notes:")
    itinerary_lines.append("• Remember to book accommodations in advance")
    itinerary_lines.append("• Check local events and attractions")
    itinerary_lines.append("• Plan transportation between locations")

    return "\n".join(itinerary_lines)
