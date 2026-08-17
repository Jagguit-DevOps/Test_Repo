# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Welcome to Azure DevOps CI/CD Training - Thanks for Joining"

# @app.route("/health")
# def health():
#     return "Application is healthy"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)


from flask import Flask, render_template_string

app = Flask(__name__)

DEVOPS_TOOLS = {
    "CI/CD": {
        "description": "Continuous Integration & Continuous Deployment",
        "tools": [
            {"name": "Azure DevOps", "adoption": 99, "image": "https://cdn-images-1.medium.com/max/1200/1*RVlkJlhKBZ5vCx9V_KhVJQ.png"},
            {"name": "Jenkins", "adoption": 99, "image": "https://www.jenkins.io/images/logos/jenkins/jenkins.png"},
            {"name": "GitHub Actions", "adoption": 99, "image": "https://github.githubassets.com/images/modules/site/features/actions-icon-actions.svg"},
            {"name": "GitLab CI", "adoption": 99, "image": "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png"},
        ]
    },
    "Containerization": {
        "description": "Container platforms & packaging",
        "tools": [
            {"name": "Docker", "adoption": 92, "image": "https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png"},
            {"name": "Podman", "adoption": 65, "image": "https://podman.io/images/podman.svg"},
            {"name": "Containerd", "adoption": 70, "image": "https://containerd.io/img/containerd-horizontal-color.png"},
        ]
    },
    "Orchestration": {
        "description": "Container orchestration & management",
        "tools": [
            {"name": "Kubernetes", "adoption": 89, "image": "https://kubernetes.io/images/kubernetes-horizontal-color.png"},
            {"name": "Docker Swarm", "adoption": 45, "image": "https://docs.docker.com/engine/swarm/images/swarm-diagram.png"},
            {"name": "OpenShift", "adoption": 72, "image": "https://www.openshift.com/hubfs/images/logos/osh-logo.svg"},
        ]
    },
    "Infrastructure as Code": {
        "description": "Declarative infrastructure management",
        "tools": [
            {"name": "Terraform", "adoption": 85, "image": "https://www.datocms-assets.com/2885/1629941242-terraform-logo.svg"},
            {"name": "Ansible", "adoption": 80, "image": "https://www.ansible.com/hubfs/2020-10-13-Ansible-logo-black.png"},
            {"name": "ARM Templates", "adoption": 68, "image": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/media/overview/azure-resource-manager-flow.png"},
        ]
    },
    "Monitoring & Logging": {
        "description": "Observability and performance tracking",
        "tools": [
            {"name": "Prometheus", "adoption": 86, "image": "https://prometheus.io/assets/prometheus_logo.svg"},
            {"name": "Grafana", "adoption": 84, "image": "https://grafana.com/static/assets/img/branding/grafana_logo_swirl_dark.svg"},
            {"name": "ELK Stack", "adoption": 79, "image": "https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt8bc6e05e4bfa0326/Elastic_Logo.svg"},
            {"name": "Datadog", "adoption": 74, "image": "https://imgix.datadoghq.com/img/about/presskit/logo-v/dd_vertical_purple.png"},
        ]
    },
    "Security & Scanning": {
        "description": "Security scanning and vulnerability management",
        "tools": [
            {"name": "SonarQube", "adoption": 77, "image": "https://www.sonarqube.org/logos/index/sonarqube-logo.svg"},
            {"name": "Snyk", "adoption": 70, "image": "https://snyk.io/style/asset/logo/snyk-print.svg"},
            {"name": "HashiCorp Vault", "adoption": 75, "image": "https://www.hashicorp.com/_next/image?url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fpath%3D%2Fproducts%2Fvault%2Fvault-logo.svg&w=640&q=80"},
        ]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Tools Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        header { text-align: center; color: white; margin-bottom: 40px; padding: 30px 0; }
        header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        header p { font-size: 1.2em; opacity: 0.95; }
        .category-section { margin-bottom: 50px; }
        .category-title { color: white; font-size: 2em; margin-bottom: 20px; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 10px; border-left: 5px solid #fff; }
        .category-description { color: rgba(255,255,255,0.9); font-size: 1.1em; margin-bottom: 20px; }
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; }
        .tool-card { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer; }
        .tool-card:hover { transform: translateY(-10px); box-shadow: 0 15px 40px rgba(0,0,0,0.3); }
        .tool-image-container { width: 100%; height: 180px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; padding: 20px; }
        .tool-image { max-width: 100%; max-height: 100%; object-fit: contain; }
        .tool-info { padding: 20px; }
        .tool-name { font-size: 1.3em; font-weight: bold; color: #333; margin-bottom: 15px; }
        .adoption-container { margin-bottom: 15px; }
        .adoption-label { font-size: 0.9em; color: #666; margin-bottom: 8px; display: flex; justify-content: space-between; font-weight: 600; }
        .adoption-bar { width: 100%; height: 10px; background: #e0e0e0; border-radius: 5px; overflow: hidden; }
        .adoption-fill { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.3s ease; }
        .stats-section { background: white; border-radius: 15px; padding: 40px; margin: 40px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .stats-title { text-align: center; font-size: 2em; color: #333; margin-bottom: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; }
        .stat-value { font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }
        .stat-label { font-size: 1em; opacity: 0.95; text-transform: uppercase; letter-spacing: 1px; }
        footer { text-align: center; color: white; margin-top: 50px; padding: 20px; border-top: 2px solid rgba(255,255,255,0.3); }
        @media (max-width: 768px) { header h1 { font-size: 2em; } .tools-grid { grid-template-columns: 1fr; } .stats-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 DevOps Tools Dashboard</h1>
            <p>Industry-leading DevOps tools and adoption rates</p>
        </header>
        <div class="stats-section">
            <div class="stats-title">Industry Adoption Rates (%)</div>
            <div class="stats-grid">
                <div class="stat-card"><div class="stat-value">89%</div><div class="stat-label">CI/CD Automation</div></div>
                <div class="stat-card"><div class="stat-value">85%</div><div class="stat-label">Containerization</div></div>
                <div class="stat-card"><div class="stat-value">81%</div><div class="stat-label">Orchestration</div></div>
                <div class="stat-card"><div class="stat-value">88%</div><div class="stat-label">Monitoring</div></div>
            </div>
        </div>
        {% for category, data in tools_data.items() %}
        <div class="category-section">
            <div class="category-title">{{ category }}</div>
            <div class="category-description">{{ data.description }}</div>
            <div class="tools-grid">
                {% for tool in data.tools %}
                <div class="tool-card">
                    <div class="tool-image-container">
                        <img src="{{ tool.image }}" alt="{{ tool.name }}" class="tool-image" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%22 height=%22100%22%3E%3Crect fill=%22%23ddd%22 width=%22100%22 height=%22100%22/%3E%3C/svg%3E'">
                    </div>
                    <div class="tool-info">
                        <div class="tool-name">{{ tool.name }}</div>
                        <div class="adoption-container">
                            <div class="adoption-label"><span>Industry Adoption</span><span>{{ tool.adoption }}%</span></div>
                            <div class="adoption-bar"><div class="adoption-fill" style="width: {{ tool.adoption }}%"></div></div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
        <footer>
            <p>📊 DevOps Tools Dashboard | Created for Training & Educational Purposes</p>
            <p>Deployed on Azure Web App</p>
        </footer>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, tools_data=DEVOPS_TOOLS)

@app.route("/health")
def health():
    return {"status": "healthy", "service": "DevOps Dashboard"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
