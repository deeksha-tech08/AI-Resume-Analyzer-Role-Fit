import os
import json

backend_path = 'backend/app/ai/role_profiles.py'
frontend_path = 'frontend/src/pages/RoleSelectPage.jsx'

roles = {
    "Frontend Developer": {
        "core": ["JavaScript", "React", "HTML/CSS", "REST APIs", "Git"],
        "optional": ["Vue.js", "Angular", "TypeScript", "Redux", "Webpack"],
        "description": "User interface design and implementation",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Data Scientist": {
        "core": ["Python", "Machine Learning", "Statistics", "Data Analysis", "SQL"],
        "optional": ["TensorFlow", "PyTorch", "Deep Learning", "R", "Spark"],
        "description": "Predictive modeling and advanced analytics",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "React Developer": {
        "core": ["JavaScript", "React", "HTML/CSS", "State Management", "Git"],
        "optional": ["TypeScript", "Next.js", "Redux", "Testing", "Performance"],
        "description": "Frontend development using React ecosystem",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Python Developer": {
        "core": ["Python", "Object-Oriented Programming", "Problem Solving", "Git"],
        "optional": ["Django", "FastAPI", "Async Programming", "Testing", "AWS"],
        "description": "Python-based application development",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Java Developer": {
        "core": ["Java", "Object-Oriented Programming", "Spring Framework", "SQL", "Git"],
        "optional": ["Microservices", "Docker", "Kubernetes", "REST APIs", "Maven"],
        "description": "Enterprise software development using Java",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Database Administrator": {
        "core": ["SQL", "Database Design", "Performance Tuning", "Backup/Recovery", "Monitoring"],
        "optional": ["PostgreSQL", "MongoDB", "MySQL", "Data Warehousing", "Query Optimization"],
        "description": "Database management and optimization",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Infrastructure Engineer": {
        "core": ["Linux", "Networking", "Cloud Platforms", "Infrastructure as Code", "Monitoring"],
        "optional": ["Docker", "Kubernetes", "Terraform", "Ansible", "AWS/Azure"],
        "description": "Systems and infrastructure management",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Platform Engineer": {
        "core": ["Cloud Platforms", "Infrastructure as Code", "CI/CD", "Kubernetes", "Python/Go"],
        "optional": ["Service Mesh", "Monitoring", "Observability", "Security", "Scalability"],
        "description": "Internal developer platform building",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Site Reliability Engineer (SRE)": {
        "core": ["System Administration", "Linux", "Scripting", "Monitoring", "Incident Response"],
        "optional": ["Kubernetes", "Go", "Python", "SLIs/SLOs", "Automation"],
        "description": "System reliability and performance",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Cloud Engineer": {
        "core": ["AWS", "Azure", "GCP", "Linux", "Networking", "Security", "Infrastructure as Code"],
        "optional": ["Python", "Bash", "Terraform", "Docker", "Kubernetes"],
        "description": "Cloud deployment and maintenance",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Solutions Architect": {
        "core": ["System Design", "Cloud Architecture", "Enterprise Integration", "Security", "Databases"],
        "optional": ["Microservices", "Serverless", "Agile", "DevOps", "API Design"],
        "description": "Designing technical solutions to business problems",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "MLOps Engineer": {
        "core": ["Machine Learning", "Python", "CI/CD", "Docker", "Kubernetes"],
        "optional": ["MLflow", "AWS SageMaker", "Model Serving", "Data Pipelines", "Monitoring"],
        "description": "Deploying and maintaining ML models",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Technical Lead / Engineering Manager": {
        "core": ["Leadership", "System Architecture", "Agile", "Mentorship", "Code Review"],
        "optional": ["Project Management", "Stakeholder Management", "Scaling", "Hiring", "DevOps"],
        "description": "Team leadership and technical direction",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Embedded Systems Engineer": {
        "core": ["C", "C++", "Microcontrollers", "RTOS", "Hardware Debugging"],
        "optional": ["Python", "IoT", "Linux Kernel", "Schematics", "Assembly"],
        "description": "Hardware and low-level software development",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Game Developer": {
        "core": ["C++", "C#", "Game Engines", "3D Math", "Performance Optimization"],
        "optional": ["Unity", "Unreal Engine", "Graphics Programming", "AI", "Physics"],
        "description": "Video game and interactive media development",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Blockchain Developer": {
        "core": ["Cryptography", "Smart Contracts", "Solidity", "Web3", "Distributed Systems"],
        "optional": ["Rust", "Go", "Ethereum", "DeFi", "Cryptography"],
        "description": "Decentralized application development",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Product Manager (Tech)": {
        "core": ["Product Strategy", "Agile", "Data Analysis", "User Stories", "Roadmapping"],
        "optional": ["UX Design", "A/B Testing", "SQL", "Technical Architecture", "Go-to-Market"],
        "description": "Technical product strategy and execution",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Growth Engineer": {
        "core": ["Data Analysis", "A/B Testing", "Full Stack Development", "Analytics", "Marketing Tech"],
        "optional": ["SQL", "React", "Python", "SEO", "Growth Hacking"],
        "description": "Engineering for user acquisition and retention",
        "core_weight": 2.0, "optional_weight": 1.0
    },
    "Staff Engineer / Principal Engineer": {
        "core": ["System Architecture", "Cross-team Collaboration", "Mentorship", "Strategic Planning", "Complex Problem Solving"],
        "optional": ["Distributed Systems", "Cloud Scale", "Performance Engineering", "Tech Debt Management", "Open Source"],
        "description": "High-level technical leadership and architecture",
        "core_weight": 2.0, "optional_weight": 1.0
    }
}

frontend_roles = [
    "{ name: 'Frontend Developer', icon: '🎨', desc: 'User interface design and implementation' }",
    "{ name: 'Data Scientist', icon: '🔬', desc: 'Predictive modeling and advanced analytics' }",
    "{ name: 'React Developer', icon: '⚛️', desc: 'Frontend development using React' }",
    "{ name: 'Python Developer', icon: '🐍', desc: 'Python-based application development' }",
    "{ name: 'Java Developer', icon: '☕', desc: 'Enterprise software development' }",
    "{ name: 'Database Administrator', icon: '🗄️', desc: 'Database management and optimization' }",
    "{ name: 'Infrastructure Engineer', icon: '🏗️', desc: 'Systems and infrastructure management' }",
    "{ name: 'Platform Engineer', icon: '🛠️', desc: 'Internal developer platform building' }",
    "{ name: 'Site Reliability Engineer (SRE)', icon: '🚨', desc: 'System reliability and performance' }",
    "{ name: 'Cloud Engineer', icon: '🌩️', desc: 'Cloud deployment and maintenance' }",
    "{ name: 'Solutions Architect', icon: '📐', desc: 'Designing technical solutions' }",
    "{ name: 'MLOps Engineer', icon: '🔄', desc: 'Deploying and maintaining ML models' }",
    "{ name: 'Technical Lead / Engineering Manager', icon: '👥', desc: 'Team leadership and technical direction' }",
    "{ name: 'Embedded Systems Engineer', icon: '🔌', desc: 'Hardware and low-level software' }",
    "{ name: 'Game Developer', icon: '🎮', desc: 'Video game development' }",
    "{ name: 'Blockchain Developer', icon: '⛓️', desc: 'Decentralized application development' }",
    "{ name: 'Product Manager (Tech)', icon: '📈', desc: 'Technical product strategy' }",
    "{ name: 'Growth Engineer', icon: '🚀', desc: 'Engineering for user acquisition' }",
    "{ name: 'Staff Engineer / Principal Engineer', icon: '🏛️', desc: 'High-level technical leadership' }"
]

# Update backend roles
with open(backend_path, 'r', encoding='utf-8') as f:
    backend_content = f.read()

# Generate python code string for new roles
new_roles_py = ""
for name, profile in roles.items():
    new_roles_py += f'    "{name}": {{\n'
    new_roles_py += f'        "core": {json.dumps(profile["core"])},\n'
    new_roles_py += f'        "optional": {json.dumps(profile["optional"])},\n'
    new_roles_py += f'        "description": "{profile["description"]}",\n'
    new_roles_py += f'        "core_weight": 2.0,\n'
    new_roles_py += f'        "optional_weight": 1.0,\n'
    new_roles_py += f'    }},\n'

backend_content = backend_content.replace('\n}\n\n# Valid role names', f',\n{new_roles_py}\n}}\n\n# Valid role names')
with open(backend_path, 'w', encoding='utf-8') as f:
    f.write(backend_content)

# Update frontend roles
with open(frontend_path, 'r', encoding='utf-8') as f:
    frontend_content = f.read()

new_roles_js = ",\n  ".join(frontend_roles)
frontend_content = frontend_content.replace('\n];', f',\n  {new_roles_js}\n];')
with open(frontend_path, 'w', encoding='utf-8') as f:
    f.write(frontend_content)

print("Roles updated successfully!")
