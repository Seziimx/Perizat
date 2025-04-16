from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
import os
import qrcode
from io import BytesIO
from werkzeug.utils import secure_filename
from routes.auth_routes import login_required
from database.models import Equipment

dashboard_bp = Blueprint('dashboard_bp', __name__)
UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'uploads/qr_codes'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # Retrieve filter parameters
    selected_type = request.args.get('type', '')
    selected_status = request.args.get('status', '')
    selected_location = request.args.get('location', '')

    # Build the query dynamically based on filters
    query = Equipment.query
    if selected_type:
        query = query.filter(Equipment.type == selected_type)
    if selected_status:
        query = query.filter(Equipment.status == selected_status)
    if selected_location:
        query = query.filter(Equipment.location == selected_location)

    # Fetch filtered equipment
    equipment_list = query.all()
    return render_template('dashboard.html', equipment_list=equipment_list, selected_type=selected_type, selected_status=selected_status, selected_location=selected_location)

@dashboard_bp.route('/dashboard', methods=['POST'])
@login_required
def dashboard_post():
    # Handle filtering
    equipment_type = request.args.get('type')
    equipment_status = request.args.get('status')
    filtered_list = Equipment.query
    if equipment_type:
        filtered_list = filtered_list.filter_by(type=equipment_type)
    if equipment_status:
        filtered_list = filtered_list.filter_by(status=equipment_status)

    # Handle file upload
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash('Файл сәтті жүктелді!', 'success')
    else:
        flash('Файл түрі жарамсыз!', 'danger')

    return render_template('dashboard.html', equipment_list=filtered_list.all())

@dashboard_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'Файл' not in request.files:
        flash('Файл бөлігі жоқ', 'danger')
        return redirect(url_for('dashboard_bp.dashboard'))

    file = request.files['Файл']
    if file.filename == '':
        flash('Таңдалған файл жоқ', 'danger')
        return redirect(url_for('dashboard_bp.dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash('Файл сәтті жүктелді!', 'success')
    else:
        flash('Файл түрі жарамсыз!', 'danger')

    return redirect(url_for('dashboard_bp.dashboard'))

@dashboard_bp.route('/generate_qr/<int:equipment_id>')
@login_required
def generate_qr(equipment_id):
    # Find the equipment by ID
    equipment = Equipment.query.get(equipment_id)
    if not equipment:
        flash('Жабдық табылмады!', 'danger')
        return redirect(url_for('dashboard_bp.dashboard'))

    # Generate QR code
    qr_data = f"ID: {equipment.id}\nАтауы: {equipment.name}\nОрналасуы: {equipment.location}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Save QR code as PNG
    img = qr.make_image(fill='black', back_color='white')
    qr_path = os.path.join(QR_FOLDER, f"{equipment.id}_qr.png")
    img.save(qr_path)

    flash('QR коды сәтті жасалды!', 'success')
    return send_file(qr_path, mimetype='image/png', as_attachment=True)

@dashboard_bp.route('/archive/<int:equipment_id>', methods=['POST'])
@login_required
def archive_equipment(equipment_id):
    # Find the equipment by ID and update its status
    equipment = Equipment.query.get(equipment_id)
    if equipment:
        equipment.status = 'Мұрағатталған'
        flash('Жабдық сәтті мұрағатталды!', 'success')
    else:
        flash('Жабдық табылмады!', 'danger')
    return redirect(url_for('dashboard_bp.dashboard'))
