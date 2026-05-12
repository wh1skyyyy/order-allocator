from flask import Flask, request, jsonify
from itertools import product

app = Flask(__name__)

def allocate_orders(orders):
    total_mileage = sum(o['mileage'] for o in orders)
    target_A = total_mileage * 0.5
    target_B = total_mileage * 0.25
    target_C = total_mileage * 0.25
    
    mileages = [o['mileage'] for o in orders]
    best_assign = None
    best_diff = float('inf')
    
    for assignment in product(['A', 'B', 'C'], repeat=len(orders)):
        sum_A = sum(mileages[i] for i, a in enumerate(assignment) if a == 'A')
        sum_B = sum(mileages[i] for i, a in enumerate(assignment) if a == 'B')
        sum_C = sum(mileages[i] for i, a in enumerate(assignment) if a == 'C')
        diff = abs(sum_A - target_A) + abs(sum_B - target_B) + abs(sum_C - target_C)
        if diff < best_diff:
            best_diff = diff
            best_assign = assignment
    
    result = []
    for i, order in enumerate(orders):
        result.append({
            'serial_no': order['serial_no'],
            'mileage': order['mileage'],
            'assigned_team': best_assign[i]
        })
    return result

@app.route('/allocate', methods=['POST'])
def allocate():
    try:
        data = request.json
        orders = data.get('orders', [])
        if not orders:
            return jsonify({'error': '没有订单数据'}), 400
        result = allocate_orders(orders)
        return jsonify({'success': True, 'allocations': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)