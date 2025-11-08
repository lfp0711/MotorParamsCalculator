
from flask import render_template, redirect, url_for, request, jsonify
from flask import Blueprint
from smart_motor_calculator import SmartMotorCalculator, SmartMotorParameters
from motor_preset_data import power_groups, motors
import logging

bp = Blueprint('calculator', '__name__')
logger = logging.getLogger(__name__)

@bp.route('/')
def home():
    logger.info('Home page accessed')
    return redirect('calculator')

@bp.route("/calculator", methods=["GET"])
def index():
    """View decorator that redirects anonymous users to the login page."""
    logger.info(power_groups.items())

    return render_template("caculator.html", power_groups=power_groups)


@bp.route('/api/motor-calculate', methods=['POST'])
def motor_calculate():
    logger.info(f'Received calculation request with data: {request.get_json()}')
    # Create SmartMotorParameters from JSON
    params = SmartMotorParameters(request)
    logger.info(f'params data: {jsonify(params.__dict__)}')
    logger.info(f'params data: {params.rated_speed_rpm}')
    calculator = SmartMotorCalculator(params)
    results = calculator.calculate_all_parameters()
    # Convert results to dict (implement .to_dict() if needed)
    return jsonify(results.__dict__)

@bp.route('/api/get-motor-preset', methods=['GET'])
def get_motor_preset():
    motor_name = request.args.get('motor_name') 
    logger.info(f'Received request: {motor_name}')
    return jsonify(motors.get(motor_name))


