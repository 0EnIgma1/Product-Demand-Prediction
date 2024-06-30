from flask import Flask, jsonify, request
import warnings
import pickle

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

app = Flask(__name__)


@app.route('/predict_demand', methods=['GET'])
def predict_product_demand():
  week_day = request.args.get('week_day')
  product = request.args.get('product')

  if not week_day or not product:
    return jsonify({'error': 'Please provide both week_day and product parameters'})

  model_filename = f"{product}.pkl"
  model = pickle.load(open(model_filename, 'rb'))
  
  week_map = {"monday":0, "tuesday":1, "wednesday":2, "thursday":3, "friday":4, "saturday":5, "sunday":6}
  current_index = week_map.get(week_day)
  next_index = (current_index + 1) % 7 

  current_day = int(model.predict([[current_index]]))
  next_day = int(model.predict([[next_index]]))
  print("Total product demand: ", current_day + next_day)
  prediced_demand = current_day + next_day

  return jsonify({'predictions': prediced_demand})

if __name__ == '__main__':
  app.run(host="0.0.0.0",port = 8082, debug=True)
