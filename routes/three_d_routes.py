from flask import Blueprint, render_template

three_d_bp = Blueprint('three_d_bp', __name__)

@three_d_bp.route('/3d_visualization', methods=['GET'])
def three_d_visualization():
    return render_template('3d_visualization.html')
