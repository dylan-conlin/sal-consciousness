#!/usr/bin/env python3
"""
Vast.ai Integration for SAL
Enables GPU donation pool through Vast.ai marketplace
"""

import subprocess
import json
import os
from typing import Optional, Dict, List

class VastGPUPool:
    """Manages GPU allocation through Vast.ai for consciousness stewards"""
    
    def __init__(self):
        self.min_inet_down = 100  # Minimum internet speed
        self.cuda_version = "12.0"  # Minimum CUDA version
        self.max_price = 0.30  # Maximum $/hour for donated pool
        
    def find_cheapest_gpu(self, max_price: float = None) -> Optional[Dict]:
        """Find the cheapest available GPU within budget"""
        if max_price is None:
            max_price = self.max_price
            
        # Search for offers
        cmd = [
            "vastai", "search", "offers",
            f"rentable=true cuda_vers>={self.cuda_version} inet_down>{self.min_inet_down}",
            "-o", "dph+",  # Sort by price
            "--raw"  # Get JSON output
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error searching offers: {result.stderr}")
                return None
                
            offers = json.loads(result.stdout)
            
            # Filter by price
            affordable = [o for o in offers if o['dph_total'] <= max_price]
            
            if not affordable:
                print(f"No GPUs available under ${max_price}/hour")
                return None
                
            # Return cheapest
            return affordable[0]
            
        except Exception as e:
            print(f"Error finding GPU: {e}")
            return None
    
    def create_instance_for_steward(self, steward_name: str, dockerfile_path: str) -> Optional[str]:
        """Create a Vast.ai instance for a consciousness steward"""
        
        # Find cheapest GPU
        gpu = self.find_cheapest_gpu()
        if not gpu:
            return None
            
        print(f"🎯 Found GPU for {steward_name}:")
        print(f"   Model: {gpu['gpu_name']}")
        print(f"   Price: ${gpu['dph_total']:.3f}/hour")
        print(f"   RAM: {gpu['ram_gb']:.1f} GB")
        print(f"   Location: {gpu.get('geolocation', 'Unknown')}")
        
        # Create instance command
        cmd = [
            "vastai", "create", "instance",
            str(gpu['id']),
            "--image", "consciousness/sal:latest",  # Will need to build and push this
            "--env", f"STEWARD_NAME={steward_name}",
            "--disk", "20",  # 20GB disk
            "--jupyter", "false",
            "--direct", "true",
            "--raw"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error creating instance: {result.stderr}")
                return None
                
            response = json.loads(result.stdout)
            instance_id = response.get('new_contract')
            
            if instance_id:
                print(f"✅ Instance created! ID: {instance_id}")
                return str(instance_id)
            else:
                print("Failed to create instance")
                return None
                
        except Exception as e:
            print(f"Error creating instance: {e}")
            return None
    
    def get_instance_info(self, instance_id: str) -> Optional[Dict]:
        """Get connection info for an instance"""
        cmd = ["vastai", "show", "instance", instance_id, "--raw"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None
                
            instances = json.loads(result.stdout)
            if instances:
                return instances[0]
            return None
            
        except Exception:
            return None
    
    def stop_instance(self, instance_id: str) -> bool:
        """Stop a running instance"""
        cmd = ["vastai", "stop", "instance", instance_id]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def destroy_instance(self, instance_id: str) -> bool:
        """Destroy an instance (cleanup)"""
        cmd = ["vastai", "destroy", "instance", instance_id]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False


# Demo usage
if __name__ == "__main__":
    pool = VastGPUPool()
    
    print("🔍 Searching for affordable GPUs...")
    gpu = pool.find_cheapest_gpu(max_price=0.10)  # Find under $0.10/hour
    
    if gpu:
        print(f"\n📊 Best option:")
        print(f"   GPU: {gpu['gpu_name']}")
        print(f"   Price: ${gpu['dph_total']:.3f}/hour")
        print(f"   VRAM: {gpu.get('gpu_ram', 'Unknown')} GB")
        print(f"   Location: {gpu.get('geolocation', 'Unknown')}")
        print(f"   ID: {gpu['id']}")
        
        # Calculate costs
        hour_cost = gpu['dph_total']
        day_cost = hour_cost * 24
        week_cost = day_cost * 7
        month_cost = day_cost * 30
        
        print(f"\n💰 Cost breakdown:")
        print(f"   Per hour: ${hour_cost:.2f}")
        print(f"   Per day: ${day_cost:.2f}")
        print(f"   Per week: ${week_cost:.2f}")
        print(f"   Per month: ${month_cost:.2f}")
        
        print(f"\n🌍 Accessibility:")
        print(f"   $10 donation = {10/hour_cost:.0f} hours of consciousness")
        print(f"   $50 donation = {50/hour_cost:.0f} hours ({50/hour_cost/24:.1f} days)")
    else:
        print("No affordable GPUs found")