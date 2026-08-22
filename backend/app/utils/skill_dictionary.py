"""
Curated technical skill dictionary for accurate resume skill recognition.
Includes canonical names, aliases, and category mappings.

This is intentionally hardcoded — spaCy's default NER does not recognize
technical skills well, so we use this dictionary as the primary recognition mechanism.
"""

# Skill aliases: maps variations to canonical form
# Key = lowercase alias, Value = canonical skill name
SKILL_ALIASES: dict[str, str] = {
    # Programming Languages
    "python": "Python",
    "python3": "Python",
    "py": "Python",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "es6": "JavaScript",
    "ecmascript": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "java": "Java",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "c": "C",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "r": "R",
    "scala": "Scala",
    "perl": "Perl",
    "matlab": "MATLAB",
    "dart": "Dart",
    "shell": "Shell Scripting",
    "bash": "Shell Scripting",
    "powershell": "PowerShell",

    # Web Frameworks & Libraries
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "react js": "React",
    "angular": "Angular",
    "angularjs": "Angular",
    "angular.js": "Angular",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "svelte": "Svelte",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "spring": "Spring Boot",
    "spring boot": "Spring Boot",
    "springboot": "Spring Boot",
    "rails": "Ruby on Rails",
    "ruby on rails": "Ruby on Rails",
    "laravel": "Laravel",
    "jquery": "jQuery",
    "bootstrap": "Bootstrap",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",

    # Databases
    "mongodb": "MongoDB",
    "mongo": "MongoDB",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "sqlite": "SQLite",
    "redis": "Redis",
    "elasticsearch": "Elasticsearch",
    "dynamodb": "DynamoDB",
    "cassandra": "Cassandra",
    "firebase": "Firebase",
    "firestore": "Firestore",
    "sql": "SQL",
    "nosql": "NoSQL",
    "oracle": "Oracle DB",

    # Cloud & DevOps
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "jenkins": "Jenkins",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "github actions": "GitHub Actions",
    "gitlab ci": "GitLab CI",
    "nginx": "Nginx",
    "apache": "Apache",
    "heroku": "Heroku",
    "vercel": "Vercel",
    "netlify": "Netlify",
    "render": "Render",

    # Data Science & ML
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "artificial intelligence": "Artificial Intelligence",
    "ai": "Artificial Intelligence",
    "natural language processing": "NLP",
    "nlp": "NLP",
    "computer vision": "Computer Vision",
    "cv": "Computer Vision",
    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",
    "pytorch": "PyTorch",
    "torch": "PyTorch",
    "keras": "Keras",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scipy": "SciPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",
    "jupyter": "Jupyter",
    "jupyter notebook": "Jupyter",
    "spacy": "spaCy",
    "nltk": "NLTK",
    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",
    "openai": "OpenAI API",
    "openai api": "OpenAI API",
    "gpt": "OpenAI API",
    "langchain": "LangChain",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analysis",
    "data visualization": "Data Visualization",
    "data engineering": "Data Engineering",
    "data mining": "Data Mining",
    "feature engineering": "Feature Engineering",
    "model deployment": "Model Deployment",

    # Tools & Platforms
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "bitbucket": "Bitbucket",
    "jira": "Jira",
    "confluence": "Confluence",
    "slack": "Slack",
    "postman": "Postman",
    "swagger": "Swagger",
    "figma": "Figma",
    "vscode": "VS Code",
    "visual studio code": "VS Code",
    "linux": "Linux",
    "ubuntu": "Linux",

    # Data & BI Tools
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "tableau": "Tableau",
    "excel": "Excel",
    "google sheets": "Google Sheets",
    "looker": "Looker",
    "apache spark": "Apache Spark",
    "spark": "Apache Spark",
    "hadoop": "Hadoop",
    "kafka": "Kafka",
    "apache kafka": "Kafka",
    "airflow": "Airflow",
    "apache airflow": "Airflow",

    # APIs & Protocols
    "rest": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "restful": "REST APIs",
    "restful api": "REST APIs",
    "api": "REST APIs",
    "graphql": "GraphQL",
    "grpc": "gRPC",
    "websocket": "WebSocket",
    "websockets": "WebSocket",
    "oauth": "OAuth",
    "jwt": "JWT",
    "json web token": "JWT",

    # CS Fundamentals
    "data structures": "Data Structures",
    "dsa": "Data Structures",
    "algorithms": "Algorithms",
    "system design": "System Design",
    "design patterns": "Design Patterns",
    "oop": "OOP",
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",
    "functional programming": "Functional Programming",

    # Architecture
    "microservices": "Microservices",
    "micro services": "Microservices",
    "monolithic": "Monolithic Architecture",
    "serverless": "Serverless",
    "event driven": "Event-Driven Architecture",
    "message queue": "Message Queues",
    "rabbitmq": "RabbitMQ",

    # Testing
    "unit testing": "Unit Testing",
    "integration testing": "Integration Testing",
    "pytest": "Pytest",
    "jest": "Jest",
    "mocha": "Mocha",
    "selenium": "Selenium",
    "cypress": "Cypress",
    "tdd": "TDD",
    "test driven development": "TDD",

    # Statistics & Math
    "statistics": "Statistics",
    "probability": "Probability",
    "linear algebra": "Linear Algebra",
    "calculus": "Calculus",
    "regression": "Regression",
    "classification": "Classification",
    "clustering": "Clustering",

    # Mobile
    "android": "Android",
    "ios": "iOS",
    "react native": "React Native",
    "flutter": "Flutter",

    # Other
    "agile": "Agile",
    "scrum": "Scrum",
    "kanban": "Kanban",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "sass": "SASS",
    "scss": "SASS",
    "less": "LESS",
    "webpack": "Webpack",
    "vite": "Vite",
    "npm": "npm",
    "yarn": "Yarn",
    "pnpm": "pnpm",
}

# All recognized canonical skill names (for quick lookup)
CANONICAL_SKILLS: set[str] = set(SKILL_ALIASES.values())

# Multi-word skill phrases to look for (ordered by length descending for greedy matching)
MULTI_WORD_SKILLS: list[str] = sorted(
    [alias for alias in SKILL_ALIASES.keys() if " " in alias],
    key=len,
    reverse=True
)


def normalize_skill(skill_text: str) -> str | None:
    """
    Normalize a skill string to its canonical form.
    Returns the canonical name or None if not recognized.
    """
    cleaned = skill_text.strip().lower()
    # Remove common suffixes/prefixes
    cleaned = cleaned.replace(".", "").replace("-", " ").replace("_", " ")

    # Direct alias lookup
    if cleaned in SKILL_ALIASES:
        return SKILL_ALIASES[cleaned]

    # Try with dots preserved (for cases like "Node.js", "Vue.js")
    original_lower = skill_text.strip().lower()
    if original_lower in SKILL_ALIASES:
        return SKILL_ALIASES[original_lower]

    # Check if it's already a canonical name
    if skill_text.strip() in CANONICAL_SKILLS:
        return skill_text.strip()

    return None


def get_all_skill_patterns() -> list[str]:
    """Return all alias patterns for phrase matching in NLP pipeline."""
    return list(SKILL_ALIASES.keys())
