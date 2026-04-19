from flask import Flask
import datetime
import platform
import socket
import time
import sys

app = Flask(__name__)
START_TIME = time.time()
visit_count = 0
DEPLOY_TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
VERSION = "2.0.3"

def get_uptime():
    seconds = int(time.time() - START_TIME)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def get_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return "N/A"

@app.route('/')
def home():
    global visit_count
    visit_count += 1
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cloud & Edge — Soulaimane Benayad</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #07090f;
  --surface: #0e1420;
  --border: #1a2840;
  --blue: #3b82f6;
  --cyan: #06b6d4;
  --green: #22c55e;
  --orange: #f97316;
  --purple: #a855f7;
  --text: #e2e8f0;
  --muted: #64748b;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: 'Syne', sans-serif;
  min-height: 100vh;
}}
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}}
.wrap {{ max-width: 1000px; margin: 0 auto; padding: 40px 24px; }}

/* Header */
.header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}}
.header-left h1 {{
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}}
.header-left h1 span {{ color: var(--cyan); }}
.header-left .sub {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--muted);
  margin-top: 4px;
}}
.version-badge {{
  background: rgba(59,130,246,0.1);
  border: 1px solid rgba(59,130,246,0.3);
  color: var(--blue);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 6px 14px;
  border-radius: 20px;
}}

/* Stats */
.stats {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}}
.stat {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
}}
.stat-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}}
.stat-value {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--cyan);
  word-break: break-all;
}}
.stat-value.green {{ color: var(--green); }}
.stat-value.orange {{ color: var(--orange); }}

/* Section title */
.section-title {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}}
.section-title::after {{
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}}

/* Pipeline */
.pipeline {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 24px;
}}
.pipeline-steps {{
  display: flex;
  align-items: center;
  overflow-x: auto;
  padding-bottom: 8px;
}}
.step {{
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 110px;
}}
.step-icon {{
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 10px;
  position: relative;
}}
.step-icon.github {{ background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.4); }}
.step-icon.jenkins {{ background: rgba(249,115,22,0.15); border: 1px solid rgba(249,115,22,0.4); }}
.step-icon.ansible {{ background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4); }}
.step-icon.openstack {{ background: rgba(6,182,212,0.15); border: 1px solid rgba(6,182,212,0.4); }}
.step-icon.flask {{ background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.4); }}
.step-icon.flask::after {{
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 14px;
  border: 2px solid var(--green);
  animation: pulse-ring 2s infinite;
}}
@keyframes pulse-ring {{
  0% {{ opacity: 1; transform: scale(1); }}
  100% {{ opacity: 0; transform: scale(1.3); }}
}}
.step-name {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text);
  text-align: center;
  font-weight: 700;
}}
.step-desc {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--muted);
  text-align: center;
  margin-top: 3px;
}}
.arrow {{
  font-size: 1.2rem;
  color: var(--muted);
  margin: 0 8px;
  flex-shrink: 0;
  padding-bottom: 30px;
}}

/* Info grid */
.info-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}}
.info-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
}}
.info-card-title {{
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 16px;
}}
.info-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
}}
.info-row:last-child {{ border-bottom: none; }}
.info-key {{ color: var(--muted); }}
.info-val {{ color: var(--cyan); font-weight: 700; }}

/* Live indicator */
.live {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--green);
}}
.live-dot {{
  width: 6px; height: 6px;
  background: var(--green);
  border-radius: 50%;
  animation: blink 1s infinite;
}}
@keyframes blink {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: 0.2; }}
}}

/* Footer */
.footer {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--muted);
}}

@media (max-width: 700px) {{
  .stats {{ grid-template-columns: repeat(2, 1fr); }}
  .info-grid {{ grid-template-columns: 1fr; }}
  .header {{ flex-direction: column; gap: 12px; }}
}}
</style>
</head>
<body>
<div class="wrap">

  <div class="header">
    <div class="header-left">
      <h1>Cloud <span>&</span> Edge Computing</h1>
      <div class="sub">OpenStack · Jenkins · Ansible · Terraform · Flask {VERSION}</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;">
      <span class="version-badge">v{VERSION}</span>
      <div class="live"><div class="live-dot"></div>ACTIF</div>
    </div>
  </div>

  <div class="stats">
    <div class="stat">
      <div class="stat-label">IP Instance</div>
      <div class="stat-value">{get_ip()}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Uptime Flask</div>
      <div class="stat-value green" id="uptime">{get_uptime()}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Visites</div>
      <div class="stat-value orange">{visit_count}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Déployé le</div>
      <div class="stat-value" style="font-size:0.72rem">{DEPLOY_TIME}</div>
    </div>
  </div>

  <div class="section-title">Workflow CI/CD</div>
  <div class="pipeline">
    <div class="pipeline-steps">
      <div class="step">
        <div class="step-icon github">🐙</div>
        <div class="step-name">GitHub</div>
        <div class="step-desc">Code source<br>app.py</div>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-icon jenkins">⚙️</div>
        <div class="step-name">Jenkins</div>
        <div class="step-desc">Détecte<br>changements</div>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-icon ansible">🔧</div>
        <div class="step-name">Ansible</div>
        <div class="step-desc">Déploie<br>sur VM</div>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-icon openstack">☁️</div>
        <div class="step-name">OpenStack</div>
        <div class="step-desc">ubuntu-flask<br>172.24.4.x</div>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-icon flask">🚀</div>
        <div class="step-name">Flask</div>
        <div class="step-desc">App mise<br>à jour ✓</div>
      </div>
    </div>
  </div>

  <div class="section-title">Informations Projet</div>
  <div class="info-grid">
    <div class="info-card">
      <div class="info-card-title" style="color:var(--cyan)">Système</div>
      <div class="info-row">
        <span class="info-key">OS</span>
        <span class="info-val">{platform.system()} {platform.release()[:20]}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Architecture</span>
        <span class="info-val">{platform.machine()}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Python</span>
        <span class="info-val">{sys.version.split()[0]}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Hostname</span>
        <span class="info-val">{socket.gethostname()}</span>
      </div>
      <div class="info-row">
        <span class="info-key">Statut Flask</span>
        <span class="info-val" style="color:var(--green)">ACTIF — Port 80</span>
      </div>
    </div>

    <div class="info-card">
      <div class="info-card-title" style="color:var(--orange)">Projet</div>
      <div class="info-row">
        <span class="info-key">Étudiant</span>
        <span class="info-val" style="color:var(--orange)">Soulaimane Benayad</span>
      </div>
      <div class="info-row">
        <span class="info-key">Module</span>
        <span class="info-val" style="color:var(--purple)">Cloud & Edge Computing</span>
      </div>
      <div class="info-row">
        <span class="info-key">IaaS</span>
        <span class="info-val">CirrOS · OpenStack</span>
      </div>
      <div class="info-row">
        <span class="info-key">SaaS</span>
        <span class="info-val">Flask · Ubuntu 22.04</span>
      </div>
      <div class="info-row">
        <span class="info-key">IaC</span>
        <span class="info-val">Terraform · Ansible</span>
      </div>
    </div>
  </div>

  <div class="footer">
    <div>Projet Déployé via <span style="color:var(--orange)">Jenkins</span> + <span style="color:var(--purple)">Ansible</span> sur <span style="color:var(--cyan)">OpenStack</span></div>
    <div>✦ <span style="color:var(--orange);font-weight:700">Soulaimane Benayad</span></div>
  </div>

</div>
<script>
setInterval(() => {{
  fetch('/uptime').then(r => r.text()).then(t => {{
    document.getElementById('uptime').textContent = t;
  }});
}}, 1000);
</script>
</body>
</html>'''

@app.route('/uptime')
def uptime():
    return get_uptime()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
