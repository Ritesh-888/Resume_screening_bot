from flask import Flask, render_template, request
import boto3
import json

app = Flask(__name__)

# Replace with your deployed SageMaker endpoint name
ENDPOINT_NAME = "your-sagemaker-endpoint-name"
# runtime = boto3.client('sagemaker-runtime')
runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')  # or your actual region

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        resume_text = request.form['resume_text']
        if resume_text.strip() != '':
            response = runtime.invoke_endpoint(
                EndpointName=ENDPOINT_NAME,
                ContentType='application/json',
                Body=json.dumps({'text': resume_text})
            )
            result = json.loads(response['Body'].read().decode())
            prediction = result.get('prediction')

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
