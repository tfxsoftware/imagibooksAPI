from flask import Flask, jsonify
import ServiceImpl as services
import Models.QuizAwnser

app = Flask(__name__)

# Define a route for your API endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": str(services.recommendAndImage(1))})

if __name__ == '__main__':
    app.run(debug=True)