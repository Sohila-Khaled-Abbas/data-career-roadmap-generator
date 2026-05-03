# Real-Time Analyst Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### 1. **Python**
**Why first:** Python is the lingua franca of data work. Every tool in your stack either uses Python or integrates with it. You need fluency here before touching specialized frameworks.

### 2. **SQL & PostgreSQL**
**Why second:** Real-time analysis lives in databases. SQL is non-negotiable—you'll query data constantly. PostgreSQL is a solid, production-grade relational database that teaches you proper database concepts without vendor lock-in.

### 3. **Pandas**
**Why third:** Once you can query data, you need to manipulate it. Pandas is Python's data manipulation library and the bridge between raw SQL results and analysis. It's your daily workhorse.

---

## Phase 2: Data Warehousing & Transformation (Weeks 5-10)

### 4. **SQL Server**
**Why here:** Expand your SQL knowledge to enterprise environments. SQL Server teaches you T-SQL dialects and enterprise-specific patterns you'll encounter in real jobs.

### 5. **Snowflake**
**Why here:** Modern cloud data warehouse. After mastering relational SQL, Snowflake shows you how enterprises structure real-time data at scale. It's cloud-native and built for analytics.

### 6. **dbt (Data Build Tool)**
**Why here:** Now that you understand SQL and have a warehouse, learn dbt to orchestrate transformations. dbt turns SQL into version-controlled, tested, documented data pipelines—essential for real-time work.

---

## Phase 3: Orchestration & Workflow (Weeks 11-16)

### 7. **Airflow**
**Why here:** dbt handles transformations, but Airflow orchestrates *everything*. Learn to schedule, monitor, and manage data pipelines. This is where "real-time" becomes operational.

### 8. **Dagster**
**Why here:** After Airflow, Dagster represents the next generation of orchestration with better asset tracking and data lineage. Understanding both gives you flexibility and deeper orchestration patterns.

---

## Phase 4: Distributed Computing & Advanced Processing (Weeks 17-22)

### 9. **Spark**
**Why here:** When data exceeds single-machine capacity, Spark handles distributed processing. You've built pipelines with Airflow/dbt; now learn to process massive datasets efficiently.

### 10. **Kubernetes**
**Why here:** Spark and Airflow run *somewhere*. Kubernetes is how you deploy and scale these systems in production. Learn container orchestration after understanding what you're orchestrating.

---

## Phase 5: Cloud & Infrastructure (Weeks 23-26)

### 11. **AWS**
**Why here:** By now you know *what* to build. AWS teaches you *where* and *how* to build it at scale. Focus on S3, EC2, RDS, Lambda, and SageMaker for analytics workflows.

---

## Phase 6: Machine Learning & Advanced Analytics (Weeks 27-32)

### 12. **PyTorch**
**Why here:** Real-time analysis increasingly involves ML. PyTorch is the deep learning framework for production systems. You have Python mastery, distributed computing knowledge (Spark), and cloud infrastructure (AWS)—now apply them to ML.

---

## Phase 7: Visualization & Reporting (Weeks 33-36)

### 13. **Power BI**
**Why here:** After building pipelines and models, stakeholders need to *see* results. Power BI integrates with SQL Server and Azure ecosystems.

### 14. **Tableau**
**Why here:** Learn the other major visualization platform. Tableau excels at exploratory analysis and complex dashboards. Having both tools makes you adaptable across organizations.

---

## Learning Strategy

**Parallel tracks allowed:**
- Phases 1-2 must be sequential (foundations first)
- Within Phase 3+, you can overlap (e.g., learn Spark while practicing Airflow)
- Visualization (Phase 7) can start earlier if you have data ready

**Practice approach:**
- Build a real-time data pipeline end-to-end: ingest → transform (dbt) → orchestrate (Airflow) → visualize (Power BI/Tableau)
- Use Snowflake as your warehouse, Spark for heavy lifting, AWS for infrastructure
- Deploy on Kubernetes once comfortable

**Time estimate:** 8-10 months of consistent practice (15-20 hours/week)