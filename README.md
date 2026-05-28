#  Enterprise Asset Management System (FastAPI + SQL)

##  Project Overview

This project is a backend system designed to manage company assets, employees, asset allocation, maintenance tracking, and audit history using FastAPI and SQL (PostgreSQL/MySQL).

It simulates a real-world enterprise asset management system used in companies to track IT assets, employee assignments, and maintenance activities.

---

## Tech Stack

- Python 3.x
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL / MySQL
- Pydantic
- JWT Authentication
- Uvicorn

---

##  Features Implemented

### Authentication
- User Registration
- User Login
- JWT Token Authentication
- Role-Based Access (Admin / Employee)

---

###  Asset Management
- Add Asset
- View Assets
- Update Asset
- Soft Delete Asset
- Asset Status Tracking (Available / Assigned / Maintenance / Retired)

---

###  Employee Asset Allocation
- Assign Asset to Employee
- Prevent Duplicate Asset Assignment
- Return Asset
- View Allocation History

---

###  Maintenance Management
- Raise Maintenance Request
- Update Maintenance Status
- Track Maintenance Cost
- Maintenance History Reports

---

###  Audit System
- Track Asset Assignment Logs
- Track Asset Return Logs
- User Activity History

---

##  Database Design

Tables used:

- users
- assets
- allocations
- maintenance
- audit_logs

---

##  SQL Tasks Included

- Find most assigned assets
- Employees holding multiple assets
- Monthly maintenance cost report
- Assets not used for last 6 months
- Asset utilization percentage
- Department-wise asset allocation report
- Top 5 expensive assets
- Assets under maintenance with pending requests
- Employee asset audit report using JOINs
- Window functions to rank departments by asset value

---

##  How to Run Project

###  Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pymysql
