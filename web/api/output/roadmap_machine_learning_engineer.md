# Machine Learning Engineer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### Python
**Why first:** Python is the lingua franca of ML engineering. Every tool, framework, and workflow downstream depends on Python proficiency. You cannot proceed effectively without solid fundamentals in syntax, data structures, and libraries.

### SQL & PostgreSQL
**Why alongside Python:** Data is foundational to ML work. SQL is non-negotiable for querying, transforming, and understanding data. PostgreSQL serves as your first relational database to understand ACID principles and query optimization. These skills unlock data exploration before any ML work begins.

### Pandas
**Why here:** Once you know Python and SQL, pandas bridges the gap between databases and analysis. It's your primary tool for data manipulation, cleaning, and exploration—essential before touching any ML frameworks.

---

## Phase 2: Data Infrastructure (Weeks 5-8)

### Snowflake & dbt
**Why together:** Snowflake is a cloud data warehouse; dbt transforms raw data into analytics-ready datasets. Learning them together shows you the modern data stack pattern: ingest → transform → serve. dbt enforces good practices (version control, testing, documentation) that scale beyond ad-hoc SQL scripts.

### SQL Server
**Why after Snowflake:** You now understand relational databases conceptually. SQL Server adds enterprise context—T-SQL dialects, performance tuning, and on-premises considerations. This breadth makes you adaptable across different organizational stacks.

---

## Phase 3: ML Frameworks & Compute (Weeks 9-14)

### PyTorch
**Why before Spark:** Start with PyTorch for deep learning fundamentals on single machines. It's more intuitive than TensorFlow for learning, and you'll understand neural networks before scaling to distributed training.

### Spark
**Why after PyTorch:** Now that you understand ML concepts, Spark teaches you distributed computing. You'll apply ML at scale—processing terabytes of data, running feature engineering pipelines, and training on clusters. Spark is the bridge between data engineering and ML engineering.

### AWS
**Why here:** With Spark knowledge, you're ready for cloud infrastructure. AWS provides the compute, storage, and orchestration for your ML pipelines. Focus on EC2, S3, SageMaker, and RDS initially—the core services for ML workflows.

---

## Phase 4: Orchestration & Workflow (Weeks 15-18)

### Airflow
**Why first orchestrator:** Airflow is the industry standard for scheduling and monitoring data pipelines. Learn it to automate your dbt transformations, Spark jobs, and model training. It's simpler than Dagster and teaches you DAG thinking.

### Dagster
**Why after Airflow:** Dagster is a more modern, asset-oriented orchestrator. Having learned Airflow's task-based model, you'll appreciate Dagster's improvements in testability, error handling, and data lineage. Use it for complex, production ML pipelines.

### Kubernetes
**Why last in orchestration:** Kubernetes manages containerized workloads at scale. After orchestrating pipelines with Airflow/Dagster, you're ready to deploy them in Kubernetes for reliability, auto-scaling, and multi-tenant environments. This is advanced infrastructure knowledge.

---

## Phase 5: Analytics & Visualization (Weeks 19-20)

### Power BI & Tableau
**Why together, why last:** These are complementary BI tools. Power BI integrates tightly with Azure/Microsoft ecosystems; Tableau excels at exploratory analysis and dashboarding. Learn both to communicate ML results to stakeholders. They're last because they depend on clean data pipelines (dbt, Spark) and orchestration (Airflow) being in place.

---

## Learning Dependencies Summary

```
Python
  ├─ SQL & PostgreSQL
  │   ├─ Pandas
  │   └─ Snowflake & dbt
  │       └─ SQL Server
  │
  ├─ PyTorch
  │   └─ Spark
  │       └─ AWS
  │           ├─ Airflow
  │            └─ Dagster
  │               └─ Kubernetes
  │
  └─ Power BI & Tableau (consume outputs from above)
```

---

## Key Principles

1. **Data before models:** Phases 1-2 ensure you can find, understand, and prepare data correctly. Most ML failures stem from poor data, not poor algorithms.

2. **Single-machine before distributed:** Learn PyTorch on your laptop before Spark on clusters. Understand the concepts before scaling.

3. **Orchestration enables production:** Phases 3-4 transition you from notebooks to production systems. Orchestration tools (Airflow, Dagster) are what make ML engineering different from data science.

4. **Infrastructure is a means, not an end:** AWS and Kubernetes are tools to deploy and scale your work. Master the ML and data concepts first; infrastructure follows naturally.

5. **Visualization is communication:** BI tools are last because they're only useful once you have reliable pipelines and models producing insights.