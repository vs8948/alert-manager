from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        alert = request.json
        print("Received alert data:", alert)  # Log the incoming alert data

        # Enrich and process the alert
        enriched_alert = enrich_alert(alert)
        send_to_slack(enriched_alert)

        return jsonify({"status": "received"}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

def enrich_alert(alert):
    alert['enriched_data'] = {'example_key': 'example_value'}
    return alert

def send_to_slack(alert):
    slack_webhook_url = 'https://hooks.slack.com/services/**************************'
    annotations = alert.get('annotations', {})
    summary = annotations.get('summary', 'No summary provided')
    description = annotations.get('description', 'No description provided')

    message = {
        'text': f"Alert: {summary}\nDetails: {description}"
    }

    response = requests.post(slack_webhook_url, json=message)
    if response.status_code != 200:
        print(f"Failed to send message to Slack: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

