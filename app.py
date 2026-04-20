from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

# Configuration
APP_VERSION = "1.0.0"
DEPLOY_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cloud & Edge Computing</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 12px;
                padding: 40px;
                max-width: 700px;
                width: 90%;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e2e8f0;
            }
            .header h1 {
                color: #2d3748;
                font-size: 28px;
                margin-bottom: 8px;
            }
            .header p {
                color: #718096;
                font-size: 14px;
            }
            .badge {
                display: inline-block;
                background: #48bb78;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            .info-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 25px;
            }
            .info-card {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
            }
            .info-card .label {
                color: #a0aec0;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 5px;
            }
            .info-card .value {
                color: #2d3748;
                font-size: 14px;
                font-weight: bold;
            }
            .stack-section {
                background: #ebf8ff;
                border: 1px solid #bee3f8;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
            }
            .stack-section h3 {
                color: #2b6cb0;
                font-size: 14px;
                margin-bottom: 10px;
            }
            .stack-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }
            .tag {
                background: #2b6cb0;
                color: white;
                padding: 3px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            .footer {
                text-align: center;
                color: #a0aec0;
                font-size: 12px;
                padding-top: 15px;
                border-top: 1px solid #e2e8f0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <span class="badge">ACTIVE</span>
                <h1>Application Flask</h1>
                <p>Deploye sur Infrastructure OpenStack</p>
            </div>

            <div class="info-grid">
                <div class="info-card">
                    <div class="label">Version</div>
                    <div class="value">''' + APP_VERSION + '''</div>
                </div>
                <div class="info-card">
                    <div class="label">Statut</div>
                    <div class="value" style="color: #48bb78;">En ligne</div>
                </div>
                <div class="info-card">
                    <div class="label">Deploye le</div>
                    <div class="value">''' + DEPLOY_TIME + '''</div>
                </div>
                <div class="info-card">
                    <div class="label">Environnement</div>
                    <div class="value">OpenStack IaaS</div>
                </div>
            </div>

            <div class="stack-section">
                <h3>Stack Technique</h3>
                <div class="stack-tags">
                    <span class="tag">OpenStack</span>
                    <span class="tag">Flask 2.0.3</span>
                    <span class="tag">Python 3.8</span>
                    <span class="tag">Ansible</span>
                    <span class="tag">Jenkins</span>
                    <span class="tag">Ubuntu 20.04</span>
                </div>
            </div>

            <div class="footer">
                Cloud & Edge Computing — Projet Academic 2025-2026
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/status')
def status():
    return jsonify({
        "status": "running",
        "version": APP_VERSION,
        "deployed_at": DEPLOY_TIME,
        "service": "flask-app",
        "environment": "openstack"
    })

@app.route('/health')
def health():
    return jsonify({
        "health": "ok",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
