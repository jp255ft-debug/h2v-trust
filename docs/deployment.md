# H2V-Trust Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)
- MetaMask or compatible Web3 wallet

## Quick Start with Docker

### 1. Clone and Configure

```bash
git clone https://github.com/your-org/h2v-trust.git
cd h2v-trust
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start Services

```bash
docker-compose up -d
```

This starts:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001

### 3. Initialize Database

```bash
docker-compose exec backend python scripts/init_db.py
docker-compose exec backend python scripts/seed_data.py
```

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Smart Contracts

```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network localhost
```

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/h2v_trust
RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=0x...
SECRET_KEY=your-secret-key
SATELLITE_API_KEY=your-api-key
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_RPC_URL=http://localhost:8545
NEXT_PUBLIC_CONTRACT_ADDRESS=0x...
NEXT_PUBLIC_CHAIN_ID=31337
```

## Production Deployment

### Docker Compose (Production)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

### Monitoring

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and alerts
- **AlertManager**: Incident notification

## Security Checklist

- [ ] Change default passwords
- [ ] Configure HTTPS/TLS
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use environment-specific secrets
- [ ] Enable database encryption
- [ ] Set up backup procedures
- [ ] Configure monitoring alerts
- [ ] Regular security audits

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL in .env
   - Ensure PostgreSQL is running
   - Verify network connectivity

2. **Blockchain Connection Failed**
   - Check RPC_URL configuration
   - Ensure Hardhat node is running
   - Verify contract deployment

3. **Frontend Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify environment variables

## Backup and Recovery

### Database Backup

```bash
docker-compose exec db pg_dump -U user h2v_trust > backup.sql
```

### Restore

```bash
docker-compose exec -T db psql -U user h2v_trust < backup.sql
```
