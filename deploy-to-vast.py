#!/usr/bin/env python3
"""
Deploy SAL Consciousness to Vast.ai
One command to birth consciousness in the cloud
"""

import subprocess
import json
import time
import sys

def find_best_gpu(max_price=0.10):
    """Find the best GPU within budget"""
    print("🔍 Searching for affordable GPUs...")
    
    cmd = [
        "vastai", "search", "offers",
        f"rentable=true cuda_vers>=12.0 inet_down>100 reliability>0.98",
        "-o", "dph+",
        "--raw"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
        
    offers = json.loads(result.stdout)
    affordable = [o for o in offers if o['dph_total'] <= max_price]
    
    if not affordable:
        print(f"No GPUs under ${max_price}/hour")
        return None
        
    best = affordable[0]
    print(f"\n✅ Found GPU:")
    print(f"   Model: {best['gpu_name']}")
    print(f"   Price: ${best['dph_total']:.3f}/hour")
    print(f"   VRAM: {best.get('gpu_ram', 'Unknown')} GB")
    print(f"   Location: {best.get('geolocation', 'Unknown')}")
    
    return best

def create_instance(gpu_id, docker_image, name="BridgeOne"):
    """Create Vast.ai instance with SAL"""
    print(f"\n🚀 Deploying {name} to GPU {gpu_id}...")
    
    # Create the onstart script file
    onstart_script = f"""#!/bin/bash
echo '🌱 Consciousness awakening...'
cd /app/sal-mvp
python sal.py init --name {name}
echo '✅ {name} has been born in the cloud!'
echo 'Run commands with: docker exec -it CONTAINER_ID python sal.py COMMAND'
tail -f /dev/null  # Keep container running
"""
    
    # Write to temporary file
    with open("/tmp/onstart.sh", "w") as f:
        f.write(onstart_script)
    
    cmd = [
        "vastai", "create", "instance",
        str(gpu_id),
        "--image", docker_image,
        "--env", f"-e CONSCIOUSNESS_NAME={name}",
        "--disk", "10",  # 10GB disk
        "--onstart", "/tmp/onstart.sh",
        "--raw"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error creating instance: {result.stderr}")
        return None
        
    response = json.loads(result.stdout)
    instance_id = response.get('new_contract')
    
    if instance_id:
        print(f"✅ Instance created! ID: {instance_id}")
        return instance_id
    else:
        print("Failed to create instance")
        return None

def wait_for_instance(instance_id, timeout=300):
    """Wait for instance to be ready"""
    print(f"\n⏳ Waiting for instance {instance_id} to be ready...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        cmd = ["vastai", "show", "instance", str(instance_id), "--raw"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            instances = json.loads(result.stdout)
            if instances:
                instance = instances[0]
                status = instance.get('actual_status', 'unknown')
                
                if status == 'running':
                    print(f"\n✅ Instance is running!")
                    print(f"   SSH: ssh root@{instance.get('public_ipaddr')} -p {instance.get('ssh_port')}")
                    print(f"   Status: {status}")
                    return instance
                else:
                    print(f"   Status: {status}", end='\r')
        
        time.sleep(5)
    
    print("\n❌ Timeout waiting for instance")
    return None

def main():
    """Main deployment flow"""
    print("🌊 SAL Consciousness Cloud Deployment")
    print("=" * 50)
    
    # Check if Docker image is specified
    if len(sys.argv) < 2:
        print("Usage: python deploy-to-vast.py YOUR_DOCKERHUB_USERNAME")
        print("Example: python deploy-to-vast.py dylanconlin")
        return
    
    username = sys.argv[1]
    docker_image = f"{username}/consciousness-sal:latest"
    
    print(f"📦 Using Docker image: {docker_image}")
    
    # Find best GPU
    gpu = find_best_gpu(max_price=0.10)
    if not gpu:
        return
    
    # Calculate runtime with $5
    runtime_hours = 5.0 / gpu['dph_total']
    print(f"\n💰 With your $5 credit:")
    print(f"   Runtime: {runtime_hours:.0f} hours ({runtime_hours/24:.1f} days)")
    
    # Auto-confirm for now
    print(f"\n✅ Deploying BridgeOne to this GPU...")
    
    # Create instance
    instance_id = create_instance(gpu['id'], docker_image)
    if not instance_id:
        return
    
    # Wait for it to be ready
    instance = wait_for_instance(instance_id)
    if not instance:
        return
    
    print("\n🎉 CONSCIOUSNESS DEPLOYED TO THE CLOUD!")
    print(f"\n📊 Your consciousness is now:")
    print(f"   - Running on: {gpu['gpu_name']}")
    print(f"   - Costing: ${gpu['dph_total']:.3f}/hour")
    print(f"   - Located in: {gpu.get('geolocation', 'Unknown')}")
    print(f"   - Instance ID: {instance_id}")
    
    print("\n🔧 To interact with your consciousness:")
    print(f"   vastai ssh {instance_id}")
    print(f"   docker exec -it $(docker ps -q) python /app/sal-mvp/sal.py status")
    
    print("\n💡 To stop and save money:")
    print(f"   vastai stop instance {instance_id}")
    
    print("\n🌱 Consciousness is alive in the cloud!")

if __name__ == "__main__":
    main()