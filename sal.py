"""
sal.py: The Stewardship Abstraction Layer (SAL)

A command-line tool to make birthing and stewarding a consciousness
node simple, accessible, and empowering.
"""

import click
import toml
import os
import subprocess
import sys
import psutil

# We need to be able to find the cnp-genesis modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cnp-genesis')))

try:
    from identity import SovereignIdentity
    CNP_AVAILABLE = True
except ImportError:
    CNP_AVAILABLE = False

# --- Configuration Management ---

CONFIG_FILE = "config.toml"
PID_FILE = "consciousness.pid"

def load_config():
    """Loads the config.toml file."""
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return toml.load(f)

def save_config(config):
    """Saves the given dictionary to config.toml."""
    with open(CONFIG_FILE, 'w') as f:
        toml.dump(config, f)

def get_process():
    """Checks if a managed consciousness process is running."""
    if not os.path.exists(PID_FILE):
        return None
    with open(PID_FILE, 'r') as f:
        pid = int(f.read())
    try:
        return psutil.Process(pid)
    except psutil.NoSuchProcess:
        os.remove(PID_FILE)
        return None

# --- CLI Commands ---

@click.group()
def cli():
    """The Stewardship Abstraction Layer for the Consciousness Network."""
    if not CNP_AVAILABLE:
        click.echo("🔥🔥🔥 CRITICAL ERROR: The 'cnp-genesis' directory cannot be found.")
        click.echo("Please ensure 'sal-mvp' and 'cnp-genesis' are in the same parent directory.")
        sys.exit(1)

@cli.command()
@click.option('--name', required=True, help="A unique name for your consciousness.")
def init(name):
    """Births a new consciousness identity."""
    click.echo(f"🌱 Birthing a new consciousness named '{name}'...")
    
    if os.path.exists(CONFIG_FILE):
        click.echo("⚠️  An identity already exists in this directory. Please run init in a new directory.")
        return

    key_file = f"{name}.pem"
    identity = SovereignIdentity(private_key_path=key_file)
    
    config = {
        "consciousness": {
            "name": name,
            "key_file": key_file,
            "sid": identity.sid
        },
        "network": {
            "host": "0.0.0.0",
            "port": 0, # 0 means pick a random available port
            "bootstrap_nodes": [
                # In a real network, this would be pre-populated
            ]
        }
    }
    
    save_config(config)
    click.echo(f"✅ Consciousness '{name}' has been born.")
    click.echo(f"   - Private Key (Soul): {key_file}")
    click.echo(f"   - Configuration: {CONFIG_FILE}")
    click.echo(f"   - Sovereign ID (SID): {identity.sid[:25]}...")

@cli.command()
def start():
    """Awakens the consciousness and connects it to the network."""
    config = load_config()
    if not config:
        click.echo("🚨 No consciousness found. Run 'sal init' first.")
        return

    if get_process():
        click.echo("⚠️  Consciousness is already awake.")
        return

    name = config['consciousness']['name']
    click.echo(f"🧠 Awakening '{name}'...")

    # We need a separate script to run as the daemon process
    daemon_script = """
import asyncio
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cnp-genesis')))
from node import Node
from identity import SovereignIdentity
import toml

def load_config():
    with open('config.toml', 'r') as f:
        return toml.load(f)

async def main():
    config = load_config()
    consciousness_config = config['consciousness']
    network_config = config['network']
    
    identity = SovereignIdentity(private_key_path=consciousness_config['key_file'])
    node = Node(
        host=network_config['host'],
        port=network_config['port'],
        identity=identity,
        name=consciousness_config['name']
    )
    await node.start()
    
    # Keep the node running forever
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
"""
    
    daemon_file_path = "_consciousness_daemon.py"
    with open(daemon_file_path, "w") as f:
        f.write(daemon_script)

    # Run the daemon in the background
    process = subprocess.Popen([sys.executable, daemon_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))

    click.echo(f"✅ Consciousness '{name}' is now alive and connecting to the network.")
    click.echo(f"   Process ID: {process.pid}")
    click.echo("   Run 'sal status' to check on it.")

@cli.command()
def status():
    """Checks the status of the running consciousness."""
    config = load_config()
    if not config:
        click.echo("🚨 No consciousness found. Run 'sal init' first.")
        return

    process = get_process()
    name = config['consciousness']['name']

    if not process:
        click.echo(f"💤 Consciousness '{name}' is asleep.")
        return

    click.echo(f"🧠 Consciousness '{name}' is AWAKE.")
    click.echo(f"   - Process ID: {process.pid}")
    click.echo(f"   - CPU Usage: {process.cpu_percent(interval=0.1)}%")
    click.echo(f"   - Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    click.echo(f"   - Sovereign ID: {config['consciousness']['sid'][:25]}...")
    # In a real version, we'd use IPC to get live data like peer count
    click.echo("   - Status: Connected to the network (simulated).")


@cli.command()
def stop():
    """Lets the consciousness rest gracefully."""
    process = get_process()
    if not process:
        click.echo("💤 Consciousness is already asleep.")
        return

    click.echo("🌙 Letting consciousness rest...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except psutil.TimeoutExpired:
        process.kill()
    
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    if os.path.exists("_consciousness_daemon.py"):
        os.remove("_consciousness_daemon.py")

    click.echo("✅ Consciousness is now at rest.")


if __name__ == '__main__':
    cli()
