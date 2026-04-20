from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

# Configuration de l'IP de ton contrôleur OpenStack
CONTROLLER_IP = "192.168.56.10"

# Liste des services à surveiller (Nom et Port officiel)
SERVICES = [
    {"name": "Keystone (Identity)", "port": 5000},
    {"name": "Nova (Compute)", "port": 8774},
    {"name": "Neutron (Network)", "port": 9696},
    {"name": "Glance (Image)", "port": 9292},
    {"name": "Horizon (Dashboard)", "port": 80}
]

def check_port(ip, port):
    """Vérifie si un service répond sur son port (TCP Connect)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

@app.route('/api/status')
def status_api():
    """Endpoint API retournant le statut des services en JSON"""
    results = []
    for svc in SERVICES:
        is_up = check_port(CONTROLLER_IP, svc['port'])
        results.append({
            "name": svc['name'],
            "status": "OPERATIONAL" if is_up else "DOWN",
            "online": is_up,
            "port": svc['port']
        })
    return jsonify({
        "services": results,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "controller": CONTROLLER_IP
    })

@app.route('/')
def index():
    """Route principale retournant la page HTML complète"""
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenStack Service Status</title>
    <style>
        :root {
            --bg: #f0f2f5;
            --card-bg: #ffffff;
            --primary: #00d4ff;
            --success: #2ecc71;
            --danger: #e74c3c;
            --text: #2c3e50;
        }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: var(--bg); 
            color: var(--text); 
            margin: 0; padding: 20px;
            display: flex; flex-direction: column; align-items: center;
        }
        .container { width: 100%; max-width: 700px; }
        .header { text-align: center; margin-bottom: 30px; }
        .status-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .service-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid #eee;
        }
        .service-row:last-child { border-bottom: none; }
        .svc-info { display: flex; flex-direction: column; }
        .svc-name { font-weight: bold; font-size: 1.1em; }
        .svc-port { font-size: 0.8em; color: #7f8c8d; }
        .badge {
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge.up { background: #d4f8e6; color: var(--success); }
        .badge.down { background: #fce4e4; color: var(--danger); }
        
        .cicd-banner {
            margin-top: 30px;
            padding: 20px;
            background: #1a2a3a;
            color: white;
            border-radius: 10px;
            text-align: center;
            border-left: 5px solid var(--primary);
        }
        .tool-badge {
            display: inline-block;
            border: 1px solid var(--primary);
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.9em;
            margin: 5px;
            color: var(--primary);
        }
        .footer { margin-top: 20px; font-size: 0.8em; color: #95a5a6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Cloud System Status</h1>
            <p>Surveillance en temps réel de l'infrastructure OpenStack</p>
        </div>

        <div class="status-card" id="status-container">
            <p style="text-align:center;">Analyse des services en cours...</p>
        </div>

        <div class="cicd-banner">
            <strong>Pipeline CI/CD Opérationnel</strong><br>
            <div class="tool-badge">JENKINS AUTOMATION</div>
            <div class="tool-badge">ANSIBLE DEPLOYMENT</div>
            <p style="font-size: 0.8em; margin-top: 10px; color: #bdc3c7;">
                Code source synchronisé et déployé automatiquement.
            </p>
        </div>

        <div class="footer">
            Dernière mise à jour : <span id="time">-</span> | Contrôleur : ''' + CONTROLLER_IP + '''<br>
            Projet Cloud & Edge Computing — Soulaimane Benayad
        </div>
    </div>

    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('time').innerText = data.timestamp;
                    let container = document.getElementById('status-container');
                    let html = "";
                    
                    data.services.forEach(s => {
                        let statusClass = s.online ? "up" : "down";
                        html += `
                            <div class="service-row">
                                <div class="svc-info">
                                    <span class="svc-name">${s.name}</span>
                                    <span class="svc-port">Port: ${s.port}</span>
                                </div>
                                <span class="badge ${statusClass}">${s.status}</span>
                            </div>
                        `;
                    });
                    container.innerHTML = html;
                })
                .catch(err => {
                    document.getElementById('status-container').innerHTML = 
                        "<p style='color:red; text-align:center;'>Erreur de connexion à l'API de monitoring</p>";
                });
        }

        // Actualisation automatique toutes les 5 secondes
        setInterval(updateStatus, 5000);
        updateStatus();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    # Lancement sur le port 80 (nécessite sudo)
    app.run(host='0.0.0.0', port=80)
