from web3 import Web3
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import json
import traceback

class Layer2DAppTester:
    def __init__(self, n_users=100):
        # Connect to local blockchain
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        
        # Ensure connection
        if not self.w3.is_connected():
            raise Exception("Couldn't connect to local Ethereum node")
            
        print("Connected to Ethereum node")
        
        # Set default account for transactions
        self.w3.eth.default_account = self.w3.eth.accounts[0]
        
        # Get accounts
        self.accounts = self.w3.eth.accounts
        print(f"Found {len(self.accounts)} accounts")
        
        if len(self.accounts) < n_users:
            print(f"Warning: Not enough accounts. Using {len(self.accounts)} accounts instead of {n_users}")
            n_users = len(self.accounts)
        
        # Load contract
        try:
            with open('build/contracts/Layer2DApp.json', 'r') as f:
                contract_json = json.load(f)
                
            # Get network ID
            network_id = str(self.w3.net.version)
            print(f"Network ID: {network_id}")
            
            # Get deployed contract address
            self.contract_address = contract_json['networks'][network_id]['address']
            print(f"Contract address: {self.contract_address}")
            
            # Create contract instance
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=contract_json['abi']
            )
        except Exception as e:
            print(f"Error loading contract: {e}")
            raise
        
        self.n_users = n_users
        print("Contract instance created")

    def register_users(self):
        """Register users on the network"""
        print("Registering users...")
        for i in range(self.n_users):
            try:
                # Estimate gas first
                gas_estimate = self.contract.functions.registerUser(i, f"User{i}").estimate_gas()
                
                # Send transaction with estimated gas
                tx_hash = self.contract.functions.registerUser(
                    i, f"User{i}"
                ).transact({
                    'from': self.w3.eth.default_account, 
                    'gas': gas_estimate * 2  # Add some buffer
                })
                
                # Wait for transaction receipt
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                
                # Check transaction status
                if receipt['status'] != 1:
                    print(f"Failed to register user {i}")
                
                if i % 10 == 0:
                    print(f"Registered {i} users...")
            except Exception as e:
                print(f"Error registering user {i}: {e}")
                traceback.print_exc()
        print("All users registered")

    def create_network(self):
        """Create power-law network and joint accounts"""
        print("Creating network...")
        # Generate power-law network
        G = nx.barabasi_albert_graph(self.n_users, 3)
        
        # Create joint accounts for each edge
        for i, (user1, user2) in enumerate(G.edges()):
            try:
                # Generate random initial balances following exponential distribution
                balance1 = int(np.random.exponential(1000))
                balance2 = int(np.random.exponential(1000))
                
                # Estimate gas first
                gas_estimate = self.contract.functions.createAcc(
                    int(user1), int(user2), balance1, balance2
                ).estimate_gas()
                
                # Create account
                tx_hash = self.contract.functions.createAcc(
                    int(user1), int(user2), balance1, balance2
                ).transact({
                    'from': self.w3.eth.default_account, 
                    'gas': gas_estimate * 2  # Add some buffer
                })
                
                # Wait for transaction receipt
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                
                # Check transaction status
                if receipt['status'] != 1:
                    print(f"Failed to create account between {user1} and {user2}")
                
                if i % 10 == 0:
                    print(f"Created {i} joint accounts...")
            except Exception as e:
                print(f"Error creating account between {user1} and {user2}: {e}")
                traceback.print_exc()
        
        self.network = G
        print("Network created")
        return G

    def run_transactions(self, n_transactions=1000):
        """Run random transactions and track success rate"""
        print("Running transactions...")
        success_rates = []
        successes = 0

        for i in range(n_transactions):
            # Random source and destination
            source = np.random.randint(0, self.n_users)
            dest = np.random.randint(0, self.n_users)
            while dest == source:
                dest = np.random.randint(0, self.n_users)

            try:
                # Estimate gas first
                try:
                    gas_estimate = self.contract.functions.sendAmount(source, dest, 1).estimate_gas({
                        'from': self.accounts[source]
                    })
                    print(f"Estimated gas for transaction: {gas_estimate}")
                except Exception as gas_est_error:
                    print(f"Gas estimation failed: {gas_est_error}")
                    gas_estimate = 500000

                # Simulate the transaction
                try:
                    simulation = self.contract.functions.sendAmount(source, dest, 1).call({
                        'from': self.accounts[source],
                        'gas': gas_estimate
                    })
                    print(f"Simulation result: {simulation}")
                except Exception as sim_error:
                    print(f"Simulation failed with error: {sim_error}")
                    traceback.print_exc()
                    continue

                # Actually send the transaction
                tx_hash = self.contract.functions.sendAmount(
                    source, dest, 1
                ).transact({
                    'from': self.accounts[source], 
                    'gas': gas_estimate * 2  # Add buffer
                })
                
                # Wait for transaction receipt
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                
                if receipt['status'] == 1:
                    successes += 1
                    print(f"Transaction {i} succeeded!")
                else:
                    print(f"Transaction {i} failed with status: {receipt['status']}")
                    
                    # Additional transaction details
                    try:
                        tx = self.w3.eth.get_transaction(tx_hash)
                        print(f"Transaction details: {tx}")
                    except Exception as tx_error:
                        print(f"Could not retrieve transaction details: {tx_error}")

            except Exception as e:
                print(f"Transaction {i} completely failed with error: {e}")
                traceback.print_exc()

            # Record success rate every 100 transactions
            if (i + 1) % 100 == 0:
                rate = successes / (i + 1)
                success_rates.append(rate)
                print(f"Success rate after {i+1} transactions: {rate:.2%}")

        return success_rates

    def plot_results(self, success_rates):
        """Plot transaction success rates"""
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(success_rates) + 1), success_rates, 'bo-')
        plt.xlabel('Transaction Batch (100 transactions each)')
        plt.ylabel('Success Rate')
        plt.title('Transaction Success Rate Over Time')
        plt.grid(True)
        plt.show()

def main():
    try:
        # Initialize tester with fewer users if needed
        tester = Layer2DAppTester(n_users=100)  # Reduced from 100 to 50
        
        # Register users
        tester.register_users()
        
        # Create network
        network = tester.create_network()
        
        # Run transactions
        success_rates = tester.run_transactions(n_transactions=1000)
        
        # Plot results
        tester.plot_results(success_rates)
        
        # Print network statistics
        print("\nNetwork Statistics:")
        print(f"Number of nodes: {network.number_of_nodes()}")
        print(f"Number of edges: {network.number_of_edges()}")
        print(f"Average degree: {sum(dict(network.degree()).values()) / network.number_of_nodes():.2f}")
    
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()