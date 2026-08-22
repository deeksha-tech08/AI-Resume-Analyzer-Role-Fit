"""
Hardcoded role skill profiles for the 4 supported tech roles.
Each role has core skills (weighted 2x) and optional skills (weighted 1x).

This is intentionally simple — Python dictionaries are the right tool here.
In an interview: "I kept profiles hardcoded because they change infrequently,
and this makes the scoring logic transparent and easy to explain."
"""

ROLE_PROFILES: dict[str, dict] = {
    "Software Engineer": {
        "core": ["Python", "JavaScript", "Data Structures", "Algorithms", "REST APIs", "Git"],
        "optional": ["React", "Node.js", "System Design", "Docker", "AWS"],
        "description": "Full-stack development with strong CS fundamentals",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "SDE": {
        "core": ["Data Structures", "Algorithms", "System Design", "Java", "C++", "Python"],
        "optional": ["Object-Oriented Design", "Distributed Systems", "AWS", "Git", "Databases"],
        "description": "Software Development Engineer focusing on scalable systems and algorithms",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Backend Developer": {
        "core": ["Python", "FastAPI", "REST APIs", "MongoDB", "JWT", "Git"],
        "optional": ["Docker", "AWS", "Redis", "PostgreSQL", "Microservices"],
        "description": "Server-side development, APIs, and database management",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Data Analyst": {
        "core": ["Python", "SQL", "Pandas", "NumPy", "Data Analysis"],
        "optional": ["Power BI", "Tableau", "Scikit-learn", "Excel", "Statistics"],
        "description": "Data analysis, visualization, and statistical insights",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "AI/ML Engineer": {
        "core": ["Python", "Machine Learning", "Scikit-learn", "NumPy", "Pandas"],
        "optional": ["TensorFlow", "PyTorch", "OpenAI API", "spaCy", "Deep Learning"],
        "description": "Machine learning model development and deployment",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "DevOps Engineer": {
        "core": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Git"],
        "optional": ["Terraform", "Ansible", "Jenkins", "Python", "Bash"],
        "description": "Infrastructure automation, CI/CD pipelines, and cloud deployment",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "QA Engineer": {
        "core": ["Testing", "Selenium", "Automation", "Python", "Git"],
        "optional": ["pytest", "Jest", "CI/CD", "API Testing", "Load Testing"],
        "description": "Quality assurance, test automation, and software testing",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Full Stack Developer": {
        "core": ["React", "Node.js", "JavaScript", "REST APIs", "MongoDB"],
        "optional": ["TypeScript", "Express", "Redux", "Docker", "AWS"],
        "description": "End-to-end web application development",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Cloud Architect": {
        "core": ["AWS", "Azure", "Infrastructure", "System Design", "Security"],
        "optional": ["Kubernetes", "GCP", "Terraform", "Docker", "Microservices"],
        "description": "Cloud infrastructure design and scalable architecture",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Mobile Developer": {
        "core": ["React Native", "Flutter", "Swift", "Mobile UI", "APIs"],
        "optional": ["Kotlin", "iOS", "Android", "Redux", "Firebase"],
        "description": "Cross-platform and native mobile application development",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Security Engineer": {
        "core": ["Cybersecurity", "Penetration Testing", "Network Security", "Linux"],
        "optional": ["Cryptography", "OWASP", "AWS Security", "Python", "SIEM"],
        "description": "System security, penetration testing, and vulnerability management",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Frontend Developer": {
        "core": ["JavaScript", "React", "HTML/CSS", "REST APIs", "Git"],
        "optional": ["Vue.js", "Angular", "TypeScript", "Redux", "Webpack"],
        "description": "User interface design and implementation",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Data Scientist": {
        "core": ["Python", "Machine Learning", "Statistics", "Data Analysis", "SQL"],
        "optional": ["TensorFlow", "PyTorch", "Deep Learning", "R", "Spark"],
        "description": "Predictive modeling and advanced analytics",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "React Developer": {
        "core": ["JavaScript", "React", "HTML/CSS", "State Management", "Git"],
        "optional": ["TypeScript", "Next.js", "Redux", "Testing", "Performance"],
        "description": "Frontend development using React ecosystem",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Python Developer": {
        "core": ["Python", "Object-Oriented Programming", "Problem Solving", "Git"],
        "optional": ["Django", "FastAPI", "Async Programming", "Testing", "AWS"],
        "description": "Python-based application development",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Java Developer": {
        "core": ["Java", "Object-Oriented Programming", "Spring Framework", "SQL", "Git"],
        "optional": ["Microservices", "Docker", "Kubernetes", "REST APIs", "Maven"],
        "description": "Enterprise software development using Java",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Database Administrator": {
        "core": ["SQL", "Database Design", "Performance Tuning", "Backup/Recovery", "Monitoring"],
        "optional": ["PostgreSQL", "MongoDB", "MySQL", "Data Warehousing", "Query Optimization"],
        "description": "Database management and optimization",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Infrastructure Engineer": {
        "core": ["Linux", "Networking", "Cloud Platforms", "Infrastructure as Code", "Monitoring"],
        "optional": ["Docker", "Kubernetes", "Terraform", "Ansible", "AWS/Azure"],
        "description": "Systems and infrastructure management",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Platform Engineer": {
        "core": ["Cloud Platforms", "Infrastructure as Code", "CI/CD", "Kubernetes", "Python/Go"],
        "optional": ["Service Mesh", "Monitoring", "Observability", "Security", "Scalability"],
        "description": "Internal developer platform building",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Site Reliability Engineer (SRE)": {
        "core": ["System Administration", "Linux", "Scripting", "Monitoring", "Incident Response"],
        "optional": ["Kubernetes", "Go", "Python", "SLIs/SLOs", "Automation"],
        "description": "System reliability and performance",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Cloud Engineer": {
        "core": ["AWS", "Azure", "GCP", "Linux", "Networking", "Security", "Infrastructure as Code"],
        "optional": ["Python", "Bash", "Terraform", "Docker", "Kubernetes"],
        "description": "Cloud deployment and maintenance",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Solutions Architect": {
        "core": ["System Design", "Cloud Architecture", "Enterprise Integration", "Security", "Databases"],
        "optional": ["Microservices", "Serverless", "Agile", "DevOps", "API Design"],
        "description": "Designing technical solutions to business problems",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "MLOps Engineer": {
        "core": ["Machine Learning", "Python", "CI/CD", "Docker", "Kubernetes"],
        "optional": ["MLflow", "AWS SageMaker", "Model Serving", "Data Pipelines", "Monitoring"],
        "description": "Deploying and maintaining ML models",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Technical Lead / Engineering Manager": {
        "core": ["Leadership", "System Architecture", "Agile", "Mentorship", "Code Review"],
        "optional": ["Project Management", "Stakeholder Management", "Scaling", "Hiring", "DevOps"],
        "description": "Team leadership and technical direction",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Embedded Systems Engineer": {
        "core": ["C", "C++", "Microcontrollers", "RTOS", "Hardware Debugging"],
        "optional": ["Python", "IoT", "Linux Kernel", "Schematics", "Assembly"],
        "description": "Hardware and low-level software development",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Game Developer": {
        "core": ["C++", "C#", "Game Engines", "3D Math", "Performance Optimization"],
        "optional": ["Unity", "Unreal Engine", "Graphics Programming", "AI", "Physics"],
        "description": "Video game and interactive media development",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Blockchain Developer": {
        "core": ["Cryptography", "Smart Contracts", "Solidity", "Web3", "Distributed Systems"],
        "optional": ["Rust", "Go", "Ethereum", "DeFi", "Cryptography"],
        "description": "Decentralized application development",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Product Manager (Tech)": {
        "core": ["Product Strategy", "Agile", "Data Analysis", "User Stories", "Roadmapping"],
        "optional": ["UX Design", "A/B Testing", "SQL", "Technical Architecture", "Go-to-Market"],
        "description": "Technical product strategy and execution",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Growth Engineer": {
        "core": ["Data Analysis", "A/B Testing", "Full Stack Development", "Analytics", "Marketing Tech"],
        "optional": ["SQL", "React", "Python", "SEO", "Growth Hacking"],
        "description": "Engineering for user acquisition and retention",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },
    "Staff Engineer / Principal Engineer": {
        "core": ["System Architecture", "Cross-team Collaboration", "Mentorship", "Strategic Planning", "Complex Problem Solving"],
        "optional": ["Distributed Systems", "Cloud Scale", "Performance Engineering", "Tech Debt Management", "Open Source"],
        "description": "High-level technical leadership and architecture",
        "core_weight": 2.0,
        "optional_weight": 1.0,
    },

}

# Valid role names for validation
VALID_ROLES: list[str] = list(ROLE_PROFILES.keys())


def get_role_profile(role_name: str) -> dict | None:
    """Get skill profile for a specific role. Returns None if not found."""
    return ROLE_PROFILES.get(role_name)


def get_all_roles() -> list[str]:
    """Return list of all valid role names."""
    return VALID_ROLES
