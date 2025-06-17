# Multi-Tenant E-commerce Platform with Django

A demonstration project showing how to build a multi-tenant SaaS application using Django and PostgreSQL schemas. Each tenant (store) gets their own isolated schema within a shared database, ensuring complete data separation while maintaining a single codebase.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Understanding Multi-Tenancy](#understanding-multi-tenancy)
- [Testing the Application](#testing-the-application)
- [API Endpoints](#api-endpoints)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Overview

This project demonstrates **schema-based multi-tenancy** where:
- Each tenant (store) has their own PostgreSQL schema
- Complete data isolation between tenants
- Shared application code
- Automatic schema switching based on subdomain

### Example Tenants
- **TechStore** (techstore.localhost:8000) - Sells electronics
- **Fashion Boutique** (fashion.localhost:8000) - Sells clothing

## Architecture

```
PostgreSQL Database (marketplace_db)
├── public schema (shared data)
│   ├── tenants table
│   ├── domains table
│   └── shared configurations
├── techstore schema (TechStore's isolated data)
│   ├── products table
│   ├── orders table
│   └── users table
└── fashion schema (Fashion Boutique's isolated data)
    ├── products table
    ├── orders table
    └── users table
```

## Features

- ✅ Complete data isolation between tenants
- ✅ Automatic schema switching based on domain
- ✅ Shared public schema for system-wide data
- ✅ Per-tenant admin interface
- ✅ Tenant-specific products and orders
- ✅ PostgreSQL schema-based separation
- ✅ Easy tenant creation and management

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher (15 recommended)
- Windows 11 / Linux / macOS
- Basic knowledge of Django

## Installation Guide

### 1. Clone the Repository
```bash
git clone <repository-url>
cd multi_tenant_marketplace
```

### 2. Set Up PostgreSQL

#### For Windows:
1. Download PostgreSQL from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Install with default settings, remember the password

#### Create Database:
```sql
# Access PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE marketplace_db;
CREATE USER marketplace_user WITH PASSWORD 'marketplace123';
GRANT ALL PRIVILEGES ON DATABASE marketplace_db TO marketplace_user;

# Important: Grant schema creation permission
\c marketplace_db
GRANT CREATE ON DATABASE marketplace_db TO marketplace_user;
\q
```

### 3. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
DB_NAME=marketplace_db
DB_USER=marketplace_user
DB_PASSWORD=marketplace123
DB_HOST=localhost
DB_PORT=5432
```

### 5. Configure Hosts File

Add these entries to your hosts file:

**Windows:** `C:\Windows\System32\drivers\etc\hosts`
**Linux/Mac:** `/etc/hosts`

```
127.0.0.1 localhost
127.0.0.1 techstore.localhost
127.0.0.1 fashion.localhost
```

### 6. Run Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations to all schemas
python manage.py migrate_schemas
```

### 7. Create Test Data

```bash
# Create tenants with test data
python manage.py create_tenant --name="TechStore" --email="admin@techstore.local" --schema="techstore" --domain="techstore.localhost"

python manage.py create_tenant --name="Fashion Boutique" --email="admin@fashion.local" --schema="fashion" --domain="fashion.localhost"

# Add sample products
python manage.py create_test_data
```

### 8. Run the Server

```bash
python manage.py runserver
```

## Understanding Multi-Tenancy

### What is Schema-Based Multi-Tenancy?

- Each tenant gets their own PostgreSQL schema (namespace)
- Schemas provide complete data isolation
- Tables are duplicated in each schema
- Tenant identification happens via subdomain

### How Request Processing Works

1. **Request arrives**: `techstore.localhost:8000/products/`
2. **Middleware identifies tenant**: Extracts "techstore" from domain
3. **Schema switch**: `SET search_path TO techstore, public;`
4. **Query execution**: All queries now use techstore schema
5. **Response**: Only TechStore's data is returned

## Testing the Application

### 1. Public Schema (No Tenant)

**URL:** http://localhost:8000/

**Expected Response:**
```json
{
  "message": "This is the public schema",
  "info": "Access tenant sites using subdomain.localhost:8000",
  "available_tenants": [
    "http://techstore.localhost:8000",
    "http://fashion.localhost:8000"
  ]
}
```

### 2. Schema Information

**URL:** http://localhost:8000/schema-info/

**Expected Response:**
```json
{
  "current_schema": "public",
  "tenant": "No tenant",
  "domain": "localhost:8000",
  "all_tenants": [
    {"name": "TechStore", "schema_name": "techstore"},
    {"name": "Fashion Boutique", "schema_name": "fashion"}
  ]
}
```

### 3. TechStore Data

**URL:** http://techstore.localhost:8000/data/

**Expected Response:**
```json
{
  "tenant_info": {
    "name": "TechStore",
    "schema": "techstore",
    "domain": "techstore.localhost:8000"
  },
  "products": [
    {"name": "Laptop", "price": "999.99"},
    {"name": "Mouse", "price": "29.99"}
  ],
  "orders": [
    {"order_number": "TECH001", "total": "1029.98"}
  ],
  "counts": {
    "products": 2,
    "orders": 1
  }
}
```

### 4. Fashion Boutique Data

**URL:** http://fashion.localhost:8000/data/

**Expected Response:**
```json
{
  "tenant_info": {
    "name": "Fashion Boutique",
    "schema": "fashion",
    "domain": "fashion.localhost:8000"
  },
  "products": [
    {"name": "T-Shirt", "price": "19.99"},
    {"name": "Jeans", "price": "49.99"}
  ],
  "orders": [
    {"order_number": "FASH001", "total": "69.98"}
  ],
  "counts": {
    "products": 2,
    "orders": 1
  }
}
```

### 5. Request Flow Visualization

**URL:** http://techstore.localhost:8000/request-flow/

**Expected Response:**
```json
{
  "current_state": {
    "domain": "techstore.localhost:8000",
    "tenant": "TechStore",
    "schema": "techstore",
    "is_public": false
  },
  "request_flow": [
    {
      "step": 1,
      "action": "Request Received",
      "details": "Domain: techstore.localhost:8000, Path: /request-flow/"
    },
    {
      "step": 2,
      "action": "TenantMainMiddleware Processing",
      "details": "Middleware extracts domain from request"
    },
    {
      "step": 3,
      "action": "Domain Lookup",
      "details": "Query: SELECT tenant_id FROM domains WHERE domain='techstore.localhost:8000'"
    },
    {
      "step": 4,
      "action": "Tenant Found",
      "details": "Tenant: TechStore, Schema: techstore"
    },
    {
      "step": 5,
      "action": "Schema Switch",
      "details": "PostgreSQL: SET search_path TO techstore, public;"
    }
  ]
}
```

### 6. Database Routing Explanation

**URL:** http://techstore.localhost:8000/db-routing/

**Expected Response:**
```json
{
  "routing_explanation": {
    "current_schema": "techstore",
    "how_routing_works": {
      "step1": "Query: Product.objects.all()",
      "step2": "Router adds schema prefix: techstore.products",
      "step3": "Actual SQL: SELECT * FROM techstore.products"
    }
  },
  "current_tenant_data": {
    "products_count": 2,
    "users_count": 1,
    "all_tenants_count": 2
  }
}
```

## API Endpoints

| Endpoint | Description | Schema Used |
|----------|-------------|-------------|
| `http://localhost:8000/` | Public landing page | public |
| `http://localhost:8000/schema-info/` | Current schema information | public |
| `http://{tenant}.localhost:8000/data/` | Tenant's products and orders | tenant-specific |
| `http://{tenant}.localhost:8000/request-flow/` | Request processing details | tenant-specific |
| `http://{tenant}.localhost:8000/db-routing/` | Database routing explanation | tenant-specific |
| `http://{tenant}.localhost:8000/admin/` | Tenant's admin interface | tenant-specific |

## How It Works

### 1. Request Processing
```
User visits: techstore.localhost:8000
     ↓
TenantMainMiddleware extracts domain
     ↓
Queries public.domains table
     ↓
Finds tenant: TechStore (schema: techstore)
     ↓
Sets PostgreSQL: SET search_path TO techstore, public;
     ↓
All queries now use techstore schema
```

### 2. Data Isolation
- Each tenant has separate tables in their schema
- No `tenant_id` filtering needed in queries
- Complete database-level isolation
- Impossible to accidentally access other tenant's data

### 3. Code Example
```python
# This same code returns different data based on the domain:
products = Product.objects.all()

# On techstore.localhost → Returns electronics
# On fashion.localhost → Returns clothing
```

## Project Structure


```
multi_tenant_marketplace/
├── apps/
│   ├── customers/        # Shared app (public schema)
│   │   ├── models.py     # Tenant, Domain models
│   │   ├── admin.py      # Tenant management
│   │   ├── views.py      # Debug/info views
│   │   └── management/
│   │       └── commands/
│   │           ├── create_tenant.py
│   │           └── create_test_data.py
│   ├── products/         # Tenant app (isolated per schema)
│   │   ├── models.py     # Product model
│   │   ├── admin.py
│   │   └── views.py
│   ├── orders/          # Tenant app (isolated per schema)
│   │   ├── models.py    # Order model
│   │   └── admin.py
│   └── cart/            # Tenant app (not implemented)
├── marketplace/
│   ├── settings.py      # Django settings with multi-tenant config
│   ├── urls.py          # URLs for tenant schemas
│   └── urls_public.py   # URLs for public schema
├── .env                 # Environment variables (don't commit!)
├── manage.py
└── requirements.txt
```

## Key Configuration Files

### settings.py
```python
# Apps are divided into shared and tenant-specific
SHARED_APPS = [
    'django_tenants',
    'apps.customers',
    # ... Django apps for public schema
]

TENANT_APPS = [
    'django.contrib.admin',
    'apps.products',
    'apps.orders',
    # ... Apps that need isolation
]

# Database uses special backend
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        # ... connection details
    }
}

# Middleware for tenant detection
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # Must be first!
    # ... other middleware
]
```

## Common Commands

### Create a New Tenant
```bash
python manage.py create_tenant --name="Electronics Plus" --email="admin@electronics.local" --schema="electronics" --domain="electronics.localhost"
```

### List All Tenants
```bash
python manage.py shell
>>> from apps.customers.models import Tenant
>>> for t in Tenant.objects.all():
...     print(f"{t.name}: {t.schema_name}")
```

### Access PostgreSQL to View Schemas
```bash
python manage.py dbshell

\dn                    # List all schemas
\dt techstore.*        # List tables in techstore schema
\dt fashion.*          # List tables in fashion schema
```

### Create Superuser for a Tenant
```bash
# First, create a management command or use schema_context
python manage.py shell
>>> from django_tenants.utils import schema_context
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> 
>>> with schema_context('techstore'):
...     User.objects.create_superuser('admin', 'admin@techstore.local', 'password')
```

## Troubleshooting

### Issue: "Subdomain not working"
**Solution:** 
1. Check hosts file has entries for subdomains
2. Ensure domain exists in database:
```python
python manage.py shell
>>> from apps.customers.models import Domain
>>> Domain.objects.all().values('domain', 'tenant__name')
```

### Issue: "Schema not found"
**Solution:**
1. Check if tenant was created properly
2. Verify in PostgreSQL:
```sql
\dn  -- Should show your schema
```

### Issue: "No data showing for tenant"
**Solution:**
1. Run `python manage.py create_test_data`
2. Check you're accessing correct domain
3. Verify schema in response headers (X-Tenant-Schema)

### Issue: "Migrations not applying"
**Solution:**
Use `migrate_schemas` instead of regular `migrate`:
```bash
python manage.py migrate_schemas
```

## Security Considerations

1. **Data Isolation**: Each tenant's data is completely isolated at the database level
2. **Schema Permissions**: Only the database user can access all schemas
3. **Session Handling**: Sessions are shared but user data is per-schema
4. **Admin Access**: Each tenant has separate admin users

## Performance Notes

- Schema switching has minimal overhead
- Each schema has its own indexes
- Connection pooling is shared across schemas
- Can scale to thousands of tenants

## Next Steps

1. **Add more features**: Implement cart functionality, user registration
2. **Custom domains**: Allow tenants to use their own domains
3. **Tenant themes**: Let each tenant customize their store appearance
4. **Billing**: Implement subscription management
5. **API**: Add Django REST Framework for API access

## Resources

- [Django-Tenants Documentation](https://django-tenants.readthedocs.io/)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [Django Documentation](https://docs.djangoproject.com/)

## License

This is a demonstration project for educational purposes.

---

## Quick Test Checklist

After setup, verify everything works:

- [ ] PostgreSQL running and accessible
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Hosts file updated
- [ ] Migrations applied
- [ ] Test data created
- [ ] Can access http://localhost:8000/
- [ ] Can access http://techstore.localhost:8000/data/
- [ ] Can access http://fashion.localhost:8000/data/
- [ ] Data is different between tenants
- [ ] Admin interface works for each tenant

If all checks pass, your multi-tenant application is working correctly! 🎉