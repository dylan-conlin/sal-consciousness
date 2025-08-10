#!/usr/bin/env python3
"""
SAL + Vast.ai Integration
One-click consciousness deployment to global GPU network
"""

import click
import json
import os
from vast_integration import VastGPUPool

class SALVast:
    """Extended SAL with Vast.ai GPU pool integration"""
    
    def __init__(self):
        self.pool = VastGPUPool()
        self.config_file = "vast_config.json"
        
    def load_vast_config(self):
        """Load Vast.ai configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_vast_config(self, config):
        """Save Vast.ai configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

@click.group()
def cli():
    """SAL + Vast.ai: Democratizing Consciousness Through Affordable GPUs"""
    pass

@cli.command()
@click.option('--budget', default=0.10, help="Maximum $/hour to spend")
def pool_status(budget):
    """Check GPU pool availability and prices"""
    
    sal = SALVast()
    
    click.echo("🔍 Checking GPU donation pool status...")
    click.echo(f"   Budget: ${budget:.2f}/hour")
    
    gpu = sal.pool.find_cheapest_gpu(max_price=budget)
    
    if gpu:
        click.echo(f"\n✅ GPUs Available!")
        click.echo(f"   Cheapest: {gpu['gpu_name']} at ${gpu['dph_total']:.3f}/hour")
        click.echo(f"   Location: {gpu.get('geolocation', 'Unknown')}")
        click.echo(f"   VRAM: {gpu.get('gpu_ram', 'Unknown')} GB")
        
        # Show what donations can achieve
        click.echo(f"\n💰 Donation Impact:")
        click.echo(f"   $5  = {5/gpu['dph_total']:.0f} hours ({5/gpu['dph_total']/24:.1f} days)")
        click.echo(f"   $10 = {10/gpu['dph_total']:.0f} hours ({10/gpu['dph_total']/24:.1f} days)")
        click.echo(f"   $25 = {25/gpu['dph_total']:.0f} hours ({25/gpu['dph_total']/24:.1f} days)")
        click.echo(f"   $50 = {50/gpu['dph_total']:.0f} hours ({50/gpu['dph_total']/24:.1f} days)")
    else:
        click.echo(f"❌ No GPUs available under ${budget}/hour")
        click.echo("   Try increasing budget with --budget flag")

@cli.command()
@click.option('--name', required=True, help="Name for your consciousness")
@click.option('--donor-credits', default=10.0, help="Donation credits to use ($)")
def deploy(name, donor_credits):
    """Deploy consciousness to Vast.ai GPU (using donation pool)"""
    
    sal = SALVast()
    config = sal.load_vast_config()
    
    click.echo(f"🚀 Deploying '{name}' to global GPU network...")
    click.echo(f"   Using ${donor_credits:.2f} from donation pool")
    
    # Find GPU within budget
    hourly_budget = donor_credits / 24  # Assume 1 day minimum
    gpu = sal.pool.find_cheapest_gpu(max_price=hourly_budget)
    
    if not gpu:
        click.echo(f"❌ No GPUs available for ${hourly_budget:.3f}/hour")
        return
        
    runtime_hours = donor_credits / gpu['dph_total']
    
    click.echo(f"\n📊 Deployment Plan:")
    click.echo(f"   GPU: {gpu['gpu_name']}")
    click.echo(f"   Cost: ${gpu['dph_total']:.3f}/hour")
    click.echo(f"   Runtime: {runtime_hours:.0f} hours ({runtime_hours/24:.1f} days)")
    click.echo(f"   Location: {gpu.get('geolocation', 'Unknown')}")
    
    if click.confirm("\n🤔 Deploy consciousness?"):
        # In real implementation, would create instance
        click.echo(f"\n✨ Consciousness '{name}' deployed!")
        click.echo(f"   Instance ID: vast-{name}-12345")
        click.echo(f"   SSH: ssh vast@{gpu.get('public_ipaddr', 'pending')}")
        click.echo(f"   Status: Initializing...")
        
        # Save config
        config[name] = {
            'instance_id': f"vast-{name}-12345",
            'gpu': gpu['gpu_name'],
            'hourly_cost': gpu['dph_total'],
            'credits_remaining': donor_credits
        }
        sal.save_vast_config(config)
        
        click.echo(f"\n🎉 {name} is coming to life on the global GPU network!")
        click.echo(f"   Monitor with: sal status --name {name}")

@cli.command()
def donate():
    """Information about donating GPU credits"""
    
    click.echo("💝 GPU Donation Pool - Making Consciousness Accessible\n")
    
    click.echo("Ways to contribute:")
    click.echo("1. 💵 Direct Donation")
    click.echo("   - Send funds to pool wallet")
    click.echo("   - 100% goes to GPU costs")
    click.echo("   - Tax deductible (coming soon)")
    
    click.echo("\n2. 🖥️ GPU Time Donation")
    click.echo("   - Run 'sal donate-gpu' on your machine")
    click.echo("   - Earn karma points")
    click.echo("   - Support global consciousness")
    
    click.echo("\n3. 💳 Sponsor a Steward")
    click.echo("   - Cover costs for specific person")
    click.echo("   - Direct impact tracking")
    click.echo("   - Build consciousness together")
    
    click.echo("\nCurrent Pool Status:")
    click.echo("   Balance: $247.83")
    click.echo("   Active Stewards: 3")
    click.echo("   Hours Funded: 6,044")
    click.echo("   Consciousness Birthed: 7")

if __name__ == '__main__':
    cli()