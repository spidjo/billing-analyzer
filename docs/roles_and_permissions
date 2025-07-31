# Roles and Permissions

This document outlines the different roles and associated permissions within the Generic SaaS Billing Platform.

## Overview

A flexible and extensible Role-Based Access Control (RBAC) model is used to manage access to platform features. Each user is assigned a role that determines what they can see and do within the system.

---

## System Roles

### 1. Super Admin

**Description**: Full control of the system. Manages platform-wide settings, tenants, and users.

**Permissions**:
- Manage all tenants (create, update, delete)
- Access and configure platform-level settings
- View global billing analytics
- Manage system-wide users and roles
- Monitor usage and system health
- Impersonate any tenant admin for support

---

### 2. Tenant Admin

**Description**: Administers the account for their organization or tenant.

**Permissions**:
- Manage their organization's billing settings and integrations
- Add/update/delete users under their tenant
- Assign roles within their tenant (e.g., billing manager, analyst)
- Create and manage customer profiles
- Set up pricing, plans, and usage rules
- View and export reports, invoices, and revenue dashboards
- Approve payments and handle disputes

---

### 3. Billing Manager

**Description**: Handles billing configurations and ensures invoices are accurate.

**Permissions**:
- Define billing rules (e.g., usage metrics, proration)
- Configure plans, discounts, and custom pricing
- Monitor usage data and perform reconciliations
- Generate and review invoices
- Trigger billing cycles manually (if required)

---

### 4. Analyst / Viewer

**Description**: Can view data and reports but cannot make changes.

**Permissions**:
- View dashboards (usage, revenue, customers)
- Export reports
- Monitor real-time analytics
- View billing history per customer

---

### 5. Customer (End-User)

**Description**: A paying customer of the tenant, usually accessing a billing portal.

**Permissions**:
- View own invoices and payment history
- Update billing information (e.g., card details)
- View usage data (if exposed by tenant)
- Download receipts
- Open support tickets or billing inquiries

---

## Permission Matrix

| Permission Area             | Super Admin | Tenant Admin | Billing Manager | Analyst | Customer |
|----------------------------|-------------|--------------|-----------------|---------|----------|
| Tenant Management          | ✅           | ❌            | ❌               | ❌       | ❌        |
| User Management            | ✅           | ✅            | ❌               | ❌       | ❌        |
| Billing Rule Configuration | ✅           | ✅            | ✅               | ❌       | ❌        |
| Invoice Generation         | ✅           | ✅            | ✅               | ❌       | ❌        |
| View Dashboards            | ✅           | ✅            | ✅               | ✅       | ❌        |
| View Own Billing Data      | ❌           | ❌            | ❌               | ❌       | ✅        |
| Email / Notification Setup | ✅           | ✅            | ✅               | ❌       | ❌        |

---

## Notes

- Permissions can be extended by implementing a fine-grained ACL later.
- Additional roles may be defined per industry use case (e.g., Finance Manager, Compliance Officer).
- Multi-tenancy is enforced; tenant users cannot access data across tenants unless elevated.

---

