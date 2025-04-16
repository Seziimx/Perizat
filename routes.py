from flask import Blueprint, render_template, request, redirect, url_for, flash

# Бағдарламаның маршруттарын анықтайтын Blueprint
main_bp = Blueprint('main_bp', __name__)

# Басты бет маршруты
@main_bp.route('/')
def басты_bet():
    return render_template('index.html')

# Жабдықтар тізімі маршруты
@main_bp.route('/equipment_list')
def жабдықтар_tizimi():
    жабдықтар = [
        {"атауы": "Бұрғылау қондырғысы", "түрі": "Бұрғылау жабдығы", "мәртебесі": "Пайдалануда"},
        {"атауы": "Штангалық насос", "түрі": "Өндіру жабдығы", "мәртебесі": "Жөндеуде"},
    ]
    return render_template('equipment_list.html', жабдықтар=жабдықтар)

# Жабдық қосу маршруты
@main_bp.route('/add_equipment', methods=['GET', 'POST'])
def жабдық_qosu():
    if request.method == 'POST':
        атауы = request.form['name']
        түрі = request.form['type']
        мәртебесі = request.form['status']
        flash(f"Жабдық қосылды: {атауы} ({түрі}, {мәртебесі})", "success")
        return redirect(url_for('main_bp.жабдықтар_tizimi'))
    return render_template('add_equipment.html')

# Қате беті маршруты
@main_bp.errorhandler(404)
def қате_beti(error):
    return render_template('404.html'), 404
