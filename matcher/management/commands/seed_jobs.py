"""
Management command: seed_jobs
Usage: python3 manage.py seed_jobs

Populates the Django database AND ChromaDB with 57 diverse job listings.
Jobs are created as Job model instances — each model.save() automatically
embeds the job text and upserts it into ChromaDB.

Run this once to seed the database. After that, manage jobs via /admin/.
"""

from django.core.management.base import BaseCommand


JOBS = [
    # ── Software & Tech ──────────────────────────────────────────────
    {
        "title": "Software Engineer",
        "company": "TechCorp Solutions",
        "field": "Software Engineering",
        "description": (
            "Develop, test, and maintain software applications. "
            "Collaborate with cross-functional teams to design scalable systems. "
            "Write clean, efficient, and well-documented code."
        ),
        "skills": "Python, Java, SQL, Git, REST APIs, Agile",
    },
    {
        "title": "Frontend Developer",
        "company": "WebStudio Inc",
        "field": "Software Engineering",
        "description": (
            "Build responsive and visually appealing web interfaces using modern frameworks. "
            "Work closely with designers to translate mockups into functional UI components."
        ),
        "skills": "HTML, CSS, JavaScript, React, Vue.js, Figma",
    },
    {
        "title": "Backend Developer",
        "company": "CloudBase Ltd",
        "field": "Software Engineering",
        "description": (
            "Design and build server-side logic, databases, and APIs. "
            "Ensure high performance, security, and reliability of backend services."
        ),
        "skills": "Node.js, Python, Django, PostgreSQL, Docker, REST",
    },
    {
        "title": "Mobile App Developer",
        "company": "AppFactory",
        "field": "Software Engineering",
        "description": (
            "Design and develop Android and iOS mobile applications. "
            "Optimize app performance and ensure a smooth user experience."
        ),
        "skills": "Flutter, React Native, Kotlin, Swift, Firebase",
    },
    {
        "title": "DevOps Engineer",
        "company": "InfraCloud",
        "field": "DevOps & Cloud",
        "description": (
            "Manage CI/CD pipelines, automate infrastructure, and ensure system reliability. "
            "Implement monitoring and alerting solutions."
        ),
        "skills": "Docker, Kubernetes, Jenkins, AWS, Terraform, Linux",
    },
    {
        "title": "Cloud Architect",
        "company": "SkyNet Systems",
        "field": "DevOps & Cloud",
        "description": (
            "Design and oversee cloud infrastructure strategies. "
            "Lead migration of on-premise systems to cloud environments."
        ),
        "skills": "AWS, Azure, GCP, Kubernetes, Microservices, Security",
    },
    {
        "title": "Cybersecurity Analyst",
        "company": "SecureShield",
        "field": "Cybersecurity",
        "description": (
            "Monitor networks for security breaches, conduct vulnerability assessments, "
            "and respond to incidents. Develop security policies and procedures."
        ),
        "skills": "Network Security, SIEM, Penetration Testing, Firewalls, Python",
    },
    # ── Data & AI ────────────────────────────────────────────────────
    {
        "title": "Data Scientist",
        "company": "Insight Analytics",
        "field": "Data Science",
        "description": (
            "Analyze large datasets to extract meaningful insights. "
            "Build machine learning models to solve business problems. "
            "Communicate findings through clear visualizations and reports."
        ),
        "skills": "Python, R, Machine Learning, SQL, Pandas, TensorFlow, Statistics",
    },
    {
        "title": "Data Analyst",
        "company": "DataFirst Corp",
        "field": "Data Science",
        "description": (
            "Collect, process, and analyze data to support business decisions. "
            "Create dashboards and visual reports for stakeholders."
        ),
        "skills": "Excel, SQL, Python, Power BI, Tableau, Statistics",
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Dynamics",
        "field": "Artificial Intelligence",
        "description": (
            "Design, build, and deploy machine learning models at scale. "
            "Optimize algorithms for performance and accuracy in production environments."
        ),
        "skills": "Python, TensorFlow, PyTorch, MLOps, Scikit-learn, Docker",
    },
    {
        "title": "AI Research Scientist",
        "company": "NeuralLabs",
        "field": "Artificial Intelligence",
        "description": (
            "Conduct cutting-edge research in AI and publish findings. "
            "Develop novel deep learning architectures and NLP techniques."
        ),
        "skills": "Deep Learning, NLP, Research, Python, PyTorch, Mathematics",
    },
    {
        "title": "Business Intelligence Developer",
        "company": "BIHub",
        "field": "Data Science",
        "description": (
            "Design and develop BI solutions, data warehouses, and ETL pipelines. "
            "Translate business requirements into technical data models."
        ),
        "skills": "SQL, Power BI, Tableau, ETL, Data Warehousing, Python",
    },
    # ── Healthcare ───────────────────────────────────────────────────
    {
        "title": "Registered Nurse",
        "company": "City General Hospital",
        "field": "Healthcare",
        "description": (
            "Provide direct patient care including assessments, medication administration, "
            "and treatment monitoring. Coordinate with physicians and healthcare teams."
        ),
        "skills": "Patient Care, IV Therapy, EMR, Critical Thinking, Compassion, BLS",
    },
    {
        "title": "ICU Nurse",
        "company": "Metropolitan Medical Center",
        "field": "Healthcare",
        "description": (
            "Care for critically ill patients in the intensive care unit. "
            "Monitor vital signs, manage ventilators, and respond to medical emergencies."
        ),
        "skills": "Critical Care, Ventilator Management, ACLS, Patient Monitoring, EMR",
    },
    {
        "title": "Pharmacist",
        "company": "MedPlus Pharmacy",
        "field": "Healthcare",
        "description": (
            "Dispense medications, counsel patients on drug use, and ensure medication safety. "
            "Review prescriptions and collaborate with physicians."
        ),
        "skills": "Pharmacology, Drug Interactions, Patient Counseling, Dispensing, EMR",
    },
    {
        "title": "Physical Therapist",
        "company": "RehabCare Clinic",
        "field": "Healthcare",
        "description": (
            "Evaluate and treat patients with physical impairments through exercises and therapy. "
            "Develop personalized rehabilitation plans."
        ),
        "skills": "Manual Therapy, Exercise Prescription, Patient Education, Anatomy",
    },
    {
        "title": "Medical Laboratory Technician",
        "company": "Diagnostics Plus",
        "field": "Healthcare",
        "description": (
            "Perform laboratory tests on blood, tissue, and other samples. "
            "Operate and maintain lab equipment and ensure accurate test results."
        ),
        "skills": "Lab Techniques, Microbiology, Hematology, Equipment Calibration, Attention to Detail",
    },
    {
        "title": "Dental Hygienist",
        "company": "Bright Smile Dental",
        "field": "Healthcare",
        "description": (
            "Clean teeth, examine patients for signs of oral disease, and provide preventive care. "
            "Educate patients on proper oral hygiene practices."
        ),
        "skills": "Dental Cleaning, X-Ray, Patient Education, Periodontal Care",
    },
    # ── Education ────────────────────────────────────────────────────
    {
        "title": "High School Teacher",
        "company": "Greenfield Academy",
        "field": "Education",
        "description": (
            "Teach curriculum subjects to high school students. Plan lessons, assess progress, "
            "and maintain a positive learning environment."
        ),
        "skills": "Curriculum Development, Classroom Management, Communication, Assessment",
    },
    {
        "title": "University Lecturer",
        "company": "State University",
        "field": "Education",
        "description": (
            "Deliver undergraduate and graduate lectures in your area of specialization. "
            "Conduct research and publish academic papers."
        ),
        "skills": "Research, Academic Writing, Lecturing, Subject Expertise, Mentoring",
    },
    {
        "title": "Special Education Teacher",
        "company": "Sunrise Learning Center",
        "field": "Education",
        "description": (
            "Design and implement individualized education programs for students with disabilities. "
            "Use specialized teaching methods and adaptive technologies."
        ),
        "skills": "IEP Development, Adaptive Teaching, Patience, Child Psychology, Communication",
    },
    {
        "title": "Online Course Instructor",
        "company": "EduStream Platform",
        "field": "Education",
        "description": (
            "Create and deliver online courses in your area of expertise. "
            "Develop video content, quizzes, and course materials."
        ),
        "skills": "Content Creation, Video Editing, Subject Expertise, Communication, LMS",
    },
    # ── Finance & Accounting ─────────────────────────────────────────
    {
        "title": "Accountant",
        "company": "FinancePro Group",
        "field": "Finance & Accounting",
        "description": (
            "Prepare financial statements, manage ledgers, and ensure compliance with tax regulations. "
            "Analyze financial data and provide insights to management."
        ),
        "skills": "Accounting, Excel, QuickBooks, Tax, Financial Reporting, Auditing",
    },
    {
        "title": "Financial Analyst",
        "company": "WealthEdge Capital",
        "field": "Finance & Accounting",
        "description": (
            "Analyze financial data and market trends to guide investment decisions. "
            "Prepare forecasting models and financial reports."
        ),
        "skills": "Financial Modeling, Excel, Bloomberg, CFA, Valuation, Statistics",
    },
    {
        "title": "Investment Banker",
        "company": "Pinnacle Bank",
        "field": "Finance & Accounting",
        "description": (
            "Advise companies on mergers, acquisitions, and capital raising. "
            "Conduct due diligence and prepare financial models."
        ),
        "skills": "M&A, Valuation, Financial Modeling, Capital Markets, Negotiation",
    },
    {
        "title": "Tax Consultant",
        "company": "TaxWise Advisory",
        "field": "Finance & Accounting",
        "description": (
            "Provide tax planning advice to individuals and businesses. "
            "Prepare and file tax returns ensuring maximum compliance and efficiency."
        ),
        "skills": "Tax Law, Compliance, Accounting, Research, Client Communication",
    },
    # ── Marketing & Sales ────────────────────────────────────────────
    {
        "title": "Digital Marketing Specialist",
        "company": "GrowthHive Agency",
        "field": "Marketing",
        "description": (
            "Plan and execute digital marketing campaigns across SEO, SEM, social media, and email. "
            "Track performance metrics and optimize campaigns for ROI."
        ),
        "skills": "SEO, Google Ads, Social Media, Analytics, Email Marketing, Content",
    },
    {
        "title": "Content Marketing Manager",
        "company": "StoryBrand Media",
        "field": "Marketing",
        "description": (
            "Develop and manage content strategy across blogs, social media, and video. "
            "Lead a team of writers and coordinate publishing schedules."
        ),
        "skills": "Content Strategy, SEO, Copywriting, Social Media, Analytics, Leadership",
    },
    {
        "title": "Sales Representative",
        "company": "SalesForce Pro",
        "field": "Sales",
        "description": (
            "Identify and pursue new business opportunities. Manage client relationships, "
            "negotiate contracts, and achieve sales targets."
        ),
        "skills": "Sales, CRM, Negotiation, Communication, Lead Generation, Closing",
    },
    {
        "title": "Brand Manager",
        "company": "Luxe Brands Co",
        "field": "Marketing",
        "description": (
            "Develop and execute brand strategies to build brand equity and market presence. "
            "Oversee advertising, packaging, and brand communications."
        ),
        "skills": "Brand Strategy, Market Research, Campaign Management, Analytics",
    },
    # ── Design & Creative ────────────────────────────────────────────
    {
        "title": "Graphic Designer",
        "company": "PixelCraft Studios",
        "field": "Design",
        "description": (
            "Create visual concepts for print and digital media including logos, brochures, "
            "and social media graphics. Work with clients to translate briefs into designs."
        ),
        "skills": "Adobe Photoshop, Illustrator, InDesign, Typography, Color Theory",
    },
    {
        "title": "UI/UX Designer",
        "company": "UserFirst Design",
        "field": "Design",
        "description": (
            "Design intuitive and visually appealing user interfaces and experiences. "
            "Conduct user research, create wireframes, and prototype interactive designs."
        ),
        "skills": "Figma, Sketch, Wireframing, Prototyping, User Research, CSS",
    },
    {
        "title": "Video Editor",
        "company": "CineEdge Productions",
        "field": "Creative Arts",
        "description": (
            "Edit raw footage into polished video content for YouTube, social media, and broadcast. "
            "Add motion graphics, sound design, and color correction."
        ),
        "skills": "Premiere Pro, After Effects, DaVinci Resolve, Storytelling, Color Grading",
    },
    {
        "title": "Interior Designer",
        "company": "HomeVision Design",
        "field": "Design",
        "description": (
            "Create functional and aesthetically pleasing interior spaces for homes and offices. "
            "Select furnishings, materials, and color palettes. Coordinate with contractors."
        ),
        "skills": "AutoCAD, 3D Rendering, Space Planning, Color Theory, Client Relations",
    },
    # ── Engineering (non-software) ───────────────────────────────────
    {
        "title": "Mechanical Engineer",
        "company": "PrecisionTech Manufacturing",
        "field": "Mechanical Engineering",
        "description": (
            "Design and develop mechanical systems, components, and machinery. "
            "Perform engineering calculations, create technical drawings, and oversee production."
        ),
        "skills": "AutoCAD, SolidWorks, Thermodynamics, FEA, Manufacturing, MATLAB",
    },
    {
        "title": "Civil Engineer",
        "company": "BuildRight Infrastructure",
        "field": "Civil Engineering",
        "description": (
            "Plan, design, and supervise construction of infrastructure projects including roads, "
            "bridges, and buildings. Ensure compliance with safety and environmental standards."
        ),
        "skills": "AutoCAD, Structural Analysis, Project Management, Surveying, Revit",
    },
    {
        "title": "Electrical Engineer",
        "company": "PowerGrid Solutions",
        "field": "Electrical Engineering",
        "description": (
            "Design electrical systems, circuits, and equipment for commercial and industrial use. "
            "Troubleshoot electrical issues and ensure compliance with codes."
        ),
        "skills": "Circuit Design, AutoCAD, PLC, Power Systems, MATLAB, Safety Standards",
    },
    {
        "title": "Chemical Engineer",
        "company": "ChemProcess Industries",
        "field": "Chemical Engineering",
        "description": (
            "Design and optimize chemical processes for manufacturing. "
            "Ensure safety compliance, scale up lab processes, and minimize waste."
        ),
        "skills": "Process Design, ASPEN, Safety Management, Chemical Analysis, Thermodynamics",
    },
    {
        "title": "Environmental Engineer",
        "company": "GreenEarth Consulting",
        "field": "Environmental Engineering",
        "description": (
            "Develop solutions to environmental problems including water treatment, pollution control, "
            "and waste management. Conduct environmental impact assessments."
        ),
        "skills": "EIA, Water Treatment, GIS, Environmental Regulations, Sampling",
    },
    # ── Legal & HR ───────────────────────────────────────────────────
    {
        "title": "Corporate Lawyer",
        "company": "LexGroup Law Firm",
        "field": "Legal",
        "description": (
            "Advise companies on legal matters including contracts, compliance, and M&A. "
            "Represent clients in negotiations and regulatory proceedings."
        ),
        "skills": "Contract Law, Corporate Law, Negotiation, Legal Research, Compliance",
    },
    {
        "title": "Legal Assistant",
        "company": "Justice & Partners",
        "field": "Legal",
        "description": (
            "Support attorneys with legal research, document preparation, and case management. "
            "Draft correspondence and maintain legal files."
        ),
        "skills": "Legal Research, Document Drafting, Case Management, MS Office, Organization",
    },
    {
        "title": "Human Resources Manager",
        "company": "PeopleFirst Corp",
        "field": "Human Resources",
        "description": (
            "Oversee recruitment, employee relations, performance management, and HR policies. "
            "Ensure compliance with employment laws and foster a positive work culture."
        ),
        "skills": "Recruitment, Employee Relations, HRIS, Labor Law, Performance Management",
    },
    {
        "title": "Recruitment Specialist",
        "company": "TalentBridge Agency",
        "field": "Human Resources",
        "description": (
            "Source, screen, and interview candidates for various roles. "
            "Build relationships with hiring managers and manage the full recruitment lifecycle."
        ),
        "skills": "Sourcing, LinkedIn, Interviewing, ATS, Communication, Negotiation",
    },
    # ── Hospitality & Food ───────────────────────────────────────────
    {
        "title": "Executive Chef",
        "company": "Grand Luxe Hotel",
        "field": "Culinary Arts",
        "description": (
            "Lead the kitchen team to deliver exceptional dining experiences. "
            "Create menus, manage food costs, and maintain hygiene standards."
        ),
        "skills": "Menu Design, Food Safety, Team Leadership, Cost Control, Culinary Arts",
    },
    {
        "title": "Pastry Chef",
        "company": "Sweet Creations Bakery",
        "field": "Culinary Arts",
        "description": (
            "Create artisan breads, cakes, and pastries for restaurant and retail. "
            "Develop new recipes and ensure consistent quality."
        ),
        "skills": "Baking, Recipe Development, Chocolate Work, Decoration, Inventory Management",
    },
    {
        "title": "Hotel Manager",
        "company": "Prestige Hotels Group",
        "field": "Hospitality",
        "description": (
            "Oversee daily hotel operations including front desk, housekeeping, and F&B. "
            "Ensure guest satisfaction and manage staff performance."
        ),
        "skills": "Operations Management, Guest Relations, Leadership, Revenue Management",
    },
    # ── Architecture & Construction ──────────────────────────────────
    {
        "title": "Architect",
        "company": "BluePrint Architects",
        "field": "Architecture",
        "description": (
            "Design buildings and spaces that are functional, safe, and aesthetically pleasing. "
            "Prepare technical drawings and oversee construction."
        ),
        "skills": "AutoCAD, Revit, SketchUp, Building Codes, Project Management, 3D Modeling",
    },
    {
        "title": "Construction Project Manager",
        "company": "BuildMaster Co",
        "field": "Construction",
        "description": (
            "Plan, coordinate, and oversee construction projects from inception to completion. "
            "Manage budgets, timelines, subcontractors, and safety compliance."
        ),
        "skills": "Project Management, MS Project, Budgeting, Safety, Contract Management",
    },
    # ── Journalism & Communication ───────────────────────────────────
    {
        "title": "Journalist",
        "company": "Daily Herald Newspaper",
        "field": "Journalism",
        "description": (
            "Research, write, and report on news stories across various topics. "
            "Conduct interviews, verify facts, and meet strict publication deadlines."
        ),
        "skills": "Writing, Research, Interviewing, Fact-Checking, Storytelling, AP Style",
    },
    {
        "title": "Public Relations Specialist",
        "company": "ReputationEdge PR",
        "field": "Communications",
        "description": (
            "Manage a company's public image through press releases, media relations, "
            "and crisis communications. Develop PR strategies and campaigns."
        ),
        "skills": "Press Releases, Media Relations, Crisis Management, Writing, Social Media",
    },
    {
        "title": "Social Media Manager",
        "company": "ViralReach Agency",
        "field": "Marketing",
        "description": (
            "Manage and grow social media channels. Create engaging content, "
            "respond to followers, and analyze performance metrics."
        ),
        "skills": "Instagram, TikTok, Content Creation, Analytics, Copywriting, Strategy",
    },
    # ── Supply Chain & Logistics ─────────────────────────────────────
    {
        "title": "Supply Chain Manager",
        "company": "GlobalFlow Logistics",
        "field": "Supply Chain",
        "description": (
            "Oversee end-to-end supply chain operations from procurement to delivery. "
            "Optimize logistics, reduce costs, and manage supplier relationships."
        ),
        "skills": "Procurement, ERP, Inventory Management, Supplier Relations, Analytics",
    },
    {
        "title": "Logistics Coordinator",
        "company": "SwiftShip Ltd",
        "field": "Supply Chain",
        "description": (
            "Coordinate the movement of goods from suppliers to customers. "
            "Track shipments, manage documentation, and resolve logistics issues."
        ),
        "skills": "Shipping, Freight, Documentation, Communication, Problem Solving, SAP",
    },
    # ── Psychology & Social Work ─────────────────────────────────────
    {
        "title": "Clinical Psychologist",
        "company": "MindWell Clinic",
        "field": "Psychology",
        "description": (
            "Assess and treat mental health disorders through therapy and counseling. "
            "Develop treatment plans and maintain detailed case records."
        ),
        "skills": "CBT, Assessment, Counseling, Mental Health, Empathy, Report Writing",
    },
    {
        "title": "Social Worker",
        "company": "Community Care Services",
        "field": "Social Work",
        "description": (
            "Support individuals and families facing challenges such as poverty, abuse, or addiction. "
            "Connect clients to resources and advocate for their well-being."
        ),
        "skills": "Case Management, Counseling, Community Resources, Empathy, Documentation",
    },
    # ── Agriculture & Environment ────────────────────────────────────
    {
        "title": "Agricultural Engineer",
        "company": "FarmTech Solutions",
        "field": "Agriculture",
        "description": (
            "Design and implement systems to improve agricultural productivity. "
            "Work on irrigation, crop management, and farm machinery optimization."
        ),
        "skills": "Irrigation Design, Crop Science, GIS, Equipment Operation, Data Analysis",
    },
    {
        "title": "Environmental Scientist",
        "company": "EcoResearch Institute",
        "field": "Environmental Science",
        "description": (
            "Study environmental conditions and the impact of human activity. "
            "Collect field samples, analyze data, and recommend remediation strategies."
        ),
        "skills": "Field Sampling, GIS, Environmental Regulations, Data Analysis, Report Writing",
    },
]


class Command(BaseCommand):
    help = "Seed the Django DB and ChromaDB with 57 diverse job listings."

    def handle(self, *args, **kwargs):
        from matcher.models import Job

        existing = Job.objects.count()
        if existing > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing} jobs already in the database. "
                    "Delete them from /admin/ or the DB first if you want to re-seed."
                )
            )
            return

        self.stdout.write(f"Creating {len(JOBS)} job listings...")

        for i, job_data in enumerate(JOBS, 1):
            # Job.save() automatically embeds the text and upserts to ChromaDB
            Job.objects.create(
                title=job_data["title"],
                company=job_data["company"],
                field=job_data["field"],
                description=job_data["description"],
                skills=job_data["skills"],
            )
            self.stdout.write(f"  [{i}/{len(JOBS)}] Created: {job_data['title']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Successfully seeded {len(JOBS)} jobs into Django DB + ChromaDB!"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Manage jobs at: http://127.0.0.1:8080/admin/matcher/job/"
            )
        )
