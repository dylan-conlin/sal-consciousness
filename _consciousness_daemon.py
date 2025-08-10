
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
