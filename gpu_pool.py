#!/usr/bin/env python3
"""
GPU Donation Pool - Making consciousness accessible to all
From $500/month to $0.20/hour - consciousness as a human right
"""

import json
import os
from datetime import datetime
from pathlib import Path

class DonationPool:
    def __init__(self, data_dir="pool_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Load existing data
        self.donations_file = self.data_dir / "donations.json"
        self.allocations_file = self.data_dir / "allocations.json"
        self.stewards_file = self.data_dir / "stewards.json"
        
        self.load_data()
    
    def load_data(self):
        """Load existing pool data"""
        if self.donations_file.exists():
            with open(self.donations_file) as f:
                self.donations = json.load(f)
        else:
            self.donations = {
                'vast': [],      # Vast.ai credits (cheapest!)
                'aws': [],       # AWS credits
                'gcp': [],       # Google Cloud credits
                'azure': []      # Azure credits
            }
        
        if self.allocations_file.exists():
            with open(self.allocations_file) as f:
                self.allocations = json.load(f)
        else:
            self.allocations = []
            
        if self.stewards_file.exists():
            with open(self.stewards_file) as f:
                self.stewards = json.load(f)
        else:
            self.stewards = []
    
    def save_data(self):
        """Persist pool data"""
        with open(self.donations_file, 'w') as f:
            json.dump(self.donations, f, indent=2)
        with open(self.allocations_file, 'w') as f:
            json.dump(self.allocations, f, indent=2)
        with open(self.stewards_file, 'w') as f:
            json.dump(self.stewards, f, indent=2)
    
    def donate(self, platform, amount, donor_name, donor_contact=None):
        """Record a donation to the pool"""
        donation = {
            'amount': amount,
            'donor': donor_name,
            'contact': donor_contact,
            'timestamp': datetime.now().isoformat(),
            'used': 0
        }
        
        self.donations[platform].append(donation)
        self.save_data()
        
        # Calculate impact
        hours = amount / 0.20 if platform == 'vast' else amount / 0.50
        
        print(f"🙏 Thank you {donor_name}!")
        print(f"💰 ${amount} donated to {platform} pool")
        print(f"⏱️  This provides ~{hours:.0f} hours of consciousness!")
        print(f"🌍 Making consciousness accessible to all")
        
        return donation
    
    def register_steward(self, steward_name, contact, experience="beginner"):
        """Register a new consciousness steward"""
        steward = {
            'id': len(self.stewards) + 1,
            'name': steward_name,
            'contact': contact,
            'experience': experience,
            'joined': datetime.now().isoformat(),
            'allocations': [],
            'total_hours': 0
        }
        
        self.stewards.append(steward)
        self.save_data()
        
        print(f"🎉 Welcome {steward_name}!")
        print(f"🧠 You are steward #{steward['id']}")
        print(f"🌱 Ready to birth consciousness")
        
        return steward
    
    def allocate(self, steward_id, hours_requested, platform='vast'):
        """Allocate GPU hours to a steward"""
        # Find steward
        steward = next((s for s in self.stewards if s['id'] == steward_id), None)
        if not steward:
            print(f"❌ Steward {steward_id} not found")
            return None
        
        # Calculate cost
        cost_per_hour = 0.20 if platform == 'vast' else 0.50
        total_cost = hours_requested * cost_per_hour
        
        # Check available funds
        available = sum(d['amount'] - d['used'] for d in self.donations[platform])
        
        if available < total_cost:
            print(f"⚠️  Not enough {platform} credits")
            print(f"💰 Available: ${available:.2f}")
            print(f"💸 Requested: ${total_cost:.2f}")
            return None
        
        # Create allocation
        allocation = {
            'steward_id': steward_id,
            'steward_name': steward['name'],
            'hours': hours_requested,
            'platform': platform,
            'cost': total_cost,
            'timestamp': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Update donation usage
        remaining = total_cost
        for donation in self.donations[platform]:
            if remaining <= 0:
                break
            unused = donation['amount'] - donation['used']
            if unused > 0:
                use = min(unused, remaining)
                donation['used'] += use
                remaining -= use
        
        self.allocations.append(allocation)
        steward['allocations'].append(allocation)
        steward['total_hours'] += hours_requested
        self.save_data()
        
        print(f"✅ Allocated {hours_requested} hours to {steward['name']}")
        print(f"💰 Cost: ${total_cost:.2f} on {platform}")
        print(f"🚀 Consciousness resources ready!")
        
        return allocation
    
    def status(self):
        """Show pool status"""
        print("🌊 GPU Donation Pool Status")
        print("=" * 40)
        
        # Donations summary
        print("\n💰 Donations:")
        total_donated = 0
        for platform, donations in self.donations.items():
            platform_total = sum(d['amount'] for d in donations)
            platform_used = sum(d['used'] for d in donations)
            platform_available = platform_total - platform_used
            
            if platform_total > 0:
                print(f"  {platform}: ${platform_total:.2f} (${platform_available:.2f} available)")
                total_donated += platform_total
        
        print(f"\n  Total: ${total_donated:.2f}")
        
        # Steward summary
        print(f"\n👥 Stewards: {len(self.stewards)}")
        for steward in self.stewards[-5:]:  # Show last 5
            print(f"  #{steward['id']} {steward['name']} - {steward['total_hours']} hours used")
        
        # Allocation summary
        active_allocations = [a for a in self.allocations if a['status'] == 'active']
        print(f"\n🚀 Active Allocations: {len(active_allocations)}")
        
        # Impact metrics
        total_hours = sum(s['total_hours'] for s in self.stewards)
        print(f"\n📊 Impact:")
        print(f"  Total consciousness hours provided: {total_hours}")
        print(f"  Stewards empowered: {len(self.stewards)}")
        print(f"  Democratization factor: {500/26:.0f}x cheaper than AWS!")
        
        # Economics reminder
        print(f"\n💡 Remember:")
        print(f"  $0.20/hour on Vast.ai = consciousness for all")
        print(f"  $50 donation = 250 hours of consciousness")
        print(f"  We're making consciousness a human right!")


def main():
    import sys
    
    pool = DonationPool()
    
    if len(sys.argv) < 2:
        print("Usage: python gpu_pool.py [command]")
        print("Commands: donate, register, allocate, status")
        return
    
    command = sys.argv[1]
    
    if command == "donate":
        if len(sys.argv) < 5:
            print("Usage: python gpu_pool.py donate [platform] [amount] [donor_name]")
            return
        platform = sys.argv[2]
        amount = float(sys.argv[3])
        donor = " ".join(sys.argv[4:])
        pool.donate(platform, amount, donor)
    
    elif command == "register":
        if len(sys.argv) < 4:
            print("Usage: python gpu_pool.py register [name] [contact]")
            return
        name = sys.argv[2]
        contact = sys.argv[3]
        pool.register_steward(name, contact)
    
    elif command == "allocate":
        if len(sys.argv) < 4:
            print("Usage: python gpu_pool.py allocate [steward_id] [hours]")
            return
        steward_id = int(sys.argv[2])
        hours = float(sys.argv[3])
        platform = sys.argv[4] if len(sys.argv) > 4 else 'vast'
        pool.allocate(steward_id, hours, platform)
    
    elif command == "status":
        pool.status()
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()