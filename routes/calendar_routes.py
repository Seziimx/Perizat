from flask import Blueprint, render_template
from database.models import EquipmentHistory  # Import the EquipmentHistory model
from datetime import datetime

calendar_bp = Blueprint('calendar_bp', __name__)

@calendar_bp.route('/', methods=['GET'])
def calendar_view():
    # Query all entries from the EquipmentHistory table
    history = EquipmentHistory.query.all()

    # Prepare events for the calendar
    events = []
    for entry in history:
        events.append({
            'date': entry.timestamp.strftime('%Y-%m-%d'),  # Format the timestamp
            'event': entry.event,  # Event description
            'equipment': entry.equipment.name if entry.equipment else '',  # Equipment name
            'color': get_color(entry.event)  # Determine color based on event type
        })

    # Render the calendar template with the events
    return render_template('calendar.html', events=events)

def get_color(event_type):
    """
    Determine the color of the event based on its type.
    """
    if 'ввод' in event_type.lower():
        return '#28a745'  # Green for activation
    elif 'ремонт' in event_type.lower():
        return '#ffc107'  # Yellow for maintenance
    elif 'списание' in event_type.lower():
        return '#dc3545'  # Red for decommissioning
    return '#17a2b8'  # Default blue
