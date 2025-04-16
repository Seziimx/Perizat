from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, Response, session
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
import qrcode
import pandas as pd
from datetime import datetime
import io
from database.models import db, Equipment, EquipmentHistory, Well
from routes.auth_routes import role_required
from utils.qr_generator import generate_qr_code  # Assume this is a utility function for QR generation

equipment_bp = Blueprint('equipment_bp', __name__)

UPLOAD_FOLDER = 'uploads/files'
QR_FOLDER = 'uploads/qr_codes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

EQUIPMENT_TYPES = [
    "Бұрғылау жабдығы", "Өндіру жабдығы", "Ұңғыма сағасының жабдығы",
    "Циркуляция және айдау", "Электр жабдығы", "Сыйымдылық жабдығы",
    "Технологиялық блоктар", "Көмекші жабдық"
]
STATUSES = ["Пайдалануда", "Жөндеуде", "Тізімнен шығарылған"]

@equipment_bp.route('/equipment_list', methods=['GET'])
def equipment_list():
    # Fetch all equipment from the database
    equipment_list = Equipment.query.all()  # Ensure this fetches all equipment
    return render_template('equipment_list.html', equipment_list=equipment_list)

@equipment_bp.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        type_ = request.form.get('type')
        location = request.form.get('location')
        status = request.form.get('status')
        activation_date = request.form.get('activation_date')
        inventory_number = request.form.get('inventory_number')

        # Convert activation_date to a Python date object
        try:
            activation_date = datetime.strptime(activation_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Іске қосу күні дұрыс форматта емес!', 'danger')
            return redirect(url_for('equipment_bp.add_equipment'))

        # Check for duplicate inventory_number
        existing_equipment = Equipment.query.filter_by(inventory_number=inventory_number).first()
        if existing_equipment:
            flash(f'Қате: түгендеу нөмірі "{inventory_number}" тіркелген!', 'danger')
            return redirect(url_for('equipment_bp.add_equipment'))

        # Validate required fields
        if not all([name, type_, location, status, activation_date, inventory_number]):
            flash('Барлық өрістерді толтырыңыз!', 'danger')
            return redirect(url_for('equipment_bp.add_equipment'))

        # Add new equipment to the database
        new_equipment = Equipment(
            name=name,
            type=type_,
            location=location,
            status=status,
            activation_date=activation_date,
            inventory_number=inventory_number
        )
        db.session.add(new_equipment)
        db.session.commit()

        flash('Жабдық сәтті қосылды!', 'success')
        return redirect(url_for('equipment_bp.equipment_list'))

    # Render the "Жабдық қосу" form for GET requests
    return render_template('add_equipment.html')

@equipment_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def edit_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    if request.method == 'POST':
        # Update logic
        equipment.name = request.form['name']
        equipment.type = request.form['type']
        equipment.status = request.form['status']
        activation_date = request.form['activation_date']
        equipment.activation_date = datetime.strptime(activation_date, '%Y-%m-%d') if activation_date else None
        db.session.commit()
        flash('Жабдық сәтті жаңартылды!', 'success')
        return redirect(url_for('equipment_bp.equipment_list'))
    # Render edit form
    return render_template('edit_equipment.html', equipment=equipment, types=EQUIPMENT_TYPES, statuses=STATUSES)

@equipment_bp.route('/upload/<int:id>', methods=['POST'])
@login_required
@role_required(['admin', 'mechanic'])
def upload_file(id):
    equipment = Equipment.query.get_or_404(id)
    file = request.files['file']
    if file:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        flash('Файл сәтті жүктелді!', 'success')
    else:
        flash('Файл таңдалмаған!', 'danger')
    return redirect(url_for('equipment_bp.edit_equipment', id=id))

@equipment_bp.route('/generate_qr/<int:id>', methods=['GET'])
def generate_qr(id):
    equipment = Equipment.query.get_or_404(id)
    # Logic for generating QR code
    return "QR Code Generated"

@equipment_bp.route('/export_excel', methods=['GET'])
@login_required
@role_required(['admin', 'operator'])
def export_excel():
    equipment_list = Equipment.query.all()
    data = [
        {
            'Атауы': e.name,
            'Түрі': e.type,
            'Мәртебесі': e.status,
            'Іске қосу күні': e.activation_date.strftime('%Y-%m-%d') if e.activation_date else ''
        }
        for e in equipment_list
    ]
    df = pd.DataFrame(data)
    file_path = os.path.join('uploads', 'equipment_report.xlsx')
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@equipment_bp.route('/log_event/<int:equipment_id>', methods=['POST'])
@login_required
@role_required(['admin', 'mechanic'])
def log_event(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    event = request.form.get('event', '').strip()

    if not event:
        flash('Оқиға бос болуы мүмкін емес!', 'danger')
        return redirect(url_for('equipment_bp.equipment_list'))

    # Add the event to the equipment's logs
    new_log = EquipmentHistory(event=event, equipment_id=equipment.id, user_id=session.get('user_id'))
    db.session.add(new_log)
    db.session.commit()

    flash('Оқиға сәтті қосылды!', 'success')
    return redirect(url_for('equipment_bp.equipment_list'))

@equipment_bp.route('/equipment_history', methods=['GET'])
def equipment_history():
    equipment_list = Equipment.query.all()  # Fetch all equipment and their logs
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date
    return render_template('history.html', equipment_list=equipment_list, current_date=current_date)

@equipment_bp.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    equipment = Equipment.query.get_or_404(id)
    new_status = request.form['status']
    equipment.status = new_status
    db.session.commit()
    flash('Мәртебесі сәтті жаңартылды!', 'success')
    return redirect(url_for('equipment_bp.equipment_list'))
