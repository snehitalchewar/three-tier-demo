# AWS 3-Tier Demo

Architecture:

Browser
  -> Route 53
  -> Internet-facing ALB
     -> `/` and frontend assets -> Web EC2 (Nginx)
     -> `/api/*` -> App EC2 (Gunicorn/Flask)
  -> RDS PostgreSQL (private DB subnet)

## Components

### Frontend
`frontend/index.html` is a plain static frontend. It calls relative `/api/*` URLs, so the browser uses the same ALB hostname and no CORS configuration is required.

### Backend
`backend/app.py` exposes:
- GET `/api/health`
- GET `/api/users`
- POST `/api/users`

Database configuration is supplied through environment variables:
- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD

### Database
Run `schema.sql` against the RDS PostgreSQL database.

## ALB listener rules

Use two target groups:
1. `web-tg` -> Web EC2 instances, port 80
2. `app-tg` -> App EC2 instances, port 8000

Example HTTPS/HTTP listener rules:
- `/api/*` -> `app-tg`
- Default `/` -> `web-tg`

The frontend uses `/api/*`, so the browser does not need to know the private App EC2 address.

## Security groups

ALB SG:
- inbound 80/443 from the Internet as required
- outbound to Web SG and App SG

Web SG:
- inbound TCP 80 from ALB SG
- no public SSH required

App SG:
- inbound TCP 8000 from ALB SG
- outbound TCP 5432 to DB SG

DB SG:
- inbound TCP 5432 from App SG only

SSM:
- EC2 instances have an instance profile containing `AmazonSSMManagedInstanceCore`
- SSM Agent uses outbound HTTPS 443 via NAT or VPC endpoints
# three-tier-demo
