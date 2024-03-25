
import ServiceImpl as services
import Models.QuizAwnser
from flask import Flask, jsonify

app = Flask(__name__)

# Define a route for your API endpoint
@app.route('/ai/recommend', methods=['GET'])
def hello():
    return jsonify({"message": str(services.recommendAndImage(1))})

if __name__ == '__main__':
    app.run(debug=True)