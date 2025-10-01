<h1 align="center">E-Commerce CRUD API</h1> 

<p align="center">
A <strong>FastAPI</strong> project that provides RESTful CRUD endpoints for managing customers, products, orders (with order items), reviews, and shipments in an e-commerce database.<br><br>
This project is built as a companion to the <a href="https://github.com/brandonvnote/ecommerce-analytics-db" target="_blank">E-Commerce Analytics Database</a> and developed using <strong>Test-Driven Development (TDD)</strong> practices.
</p> 

---

<h2>Features</h2>
<ul>
  <li>FastAPI backend with modular routers (Customers, Products, Orders, Reviews, Shipments)</li>
  <li>SQLAlchemy ORM models mapped to PostgreSQL with relationships (Orders → OrderItems)</li>
  <li>Pydantic schemas for request/response validation</li>
  <li>Standardized error handling with consistent JSON responses</li>
  <li>Full CRUD operations with clean RESTful design</li>
  <li>Safe development using a dedicated <code>ecommerce_test</code> database</li>
  <li>Automated testing with Pytest + FastAPI TestClient </li>
  <li>Cascading deletes for Order → OrderItems using SQLAlchemy relationships</li>
</ul>

---

<h2>Tech Stack</h2>
<ul>
  <li><strong>Backend</strong>: FastAPI (Python 3.11+)</li>
  <li><strong>Database</strong>: PostgreSQL (SQLAlchemy ORM)</li>
  <li><strong>Validation</strong>: Pydantic v2</li>
  <li><strong>Testing</strong>: Pytest, HTTPX, pytest-asyncio</li>
</ul>

---

<h2>Getting Started</h2>

<h3>1. Clone Repo</h3>

```
git clone https://github.com/brandonvnote/crud_api.git
cd crud_api
```
<h3>2. Create Virtual Environment</h3>

```
python -m venv .venv
.venv\Scripts\activate    # On Windows
source .venv/bin/activate # On Mac/Linux
```
<h3>3. Install Dependencies</h3>

```
pip install -r requirements.txt
```
<h3>4. Set Up Environment Variables</h3>

```
Create a .env file in the project root:

DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce
TEST_DB_NAME=ecommerce_test
```
<h3>5. Run the API</h3>

```
uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/docs for the Swagger UI.
```
<h3>6. Run Tests</h3>

```
$env:ENV="test"; pytest -v   # On Windows PowerShell
ENV=test pytest -v           # On Mac/Linux
```

