from flask import Blueprint, request, jsonify
from app.models import User

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask MongoDB API!'}), 200

@main_blueprint.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
  
    publicKey = data.get('publicKey')
    addingToken = data.get('addingToken', 0)  # Default to 0 if not provided
    deactivateState = data.get('deactivateState', False)  # Default to False if not provided

    if not publicKey:
        return jsonify({'error': 'Missing publicKey'}), 400

    try:
        # Pass all parameters to create_user method
        user_id = User.create_user(publicKey, addingToken, deactivateState)
        return jsonify({'message': 'User created', 'id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_blueprint.route('/update_deactivate_state', methods=['POST'])
def update_deactivate_state():
    data = request.get_json()
  
    userId = data.get('userId')
    deactivateState = data.get('deactivateState')  # Fix here to get the correct key

    if userId is None or deactivateState is None:  # Check for missing parameters
        return jsonify({'error': 'Missing userId or deactivateState'}), 400

    try:
        # Pass all parameters to update_deactivate_state method
        updated_user = User.update_deactivate_state(userId, deactivateState)
        if updated_user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User deactivation state updated', 'user': updated_user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main_blueprint.route('/check_deactivate_state/<user_id>', methods=['GET'])
def check_deactivate_state(user_id):
    user = User.check_deactivate_state(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user), 200

@main_blueprint.route('/update_adding_token/<user_id>', methods=['GET'])
def update_adding_token(user_id):
    updated_token = User.update_adding_token(user_id)

    if updated_token is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'Adding token updated', 'addingToken': updated_token}), 200


@main_blueprint.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user), 200

@main_blueprint.route('/add_user/<int:addingToken>', methods=['GET'])
def get_public_key_by_adding_token(addingToken):
    result = User.get_user_by_adding_token(addingToken)

    if 'error' in result:
        return jsonify({'error': result['error']}), 400

    return jsonify({'publicKey': result['publicKey']}), 200