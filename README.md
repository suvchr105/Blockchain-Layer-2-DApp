## Layer 2 Decentralized Application (DApp) Tester

![dapp](https://github.com/user-attachments/assets/9c9d5385-3d62-43da-a75f-8ffd73d9edf0)


# 📋 Table of Contents
1. Project Overview
2. Prerequisites
3. Installation
4. Project Structure
5. Configuration
6. Running the Application
7. Troubleshooting
8. Contributing

# 🌟 Project Overview
This Layer 2 DApp Tester is a comprehensive blockchain network simulation tool designed to test and analyze decentralized application performance using Ethereum-compatible blockchain technologies.
![Screenshot 2024-11-18 at 7 28 26 PM](https://github.com/user-attachments/assets/a2ec0140-cd49-4365-a320-2c8923c8009c)

# Experimental Setup

1. Network Configuration

Total Nodes: 100 users
Network Topology: Barabási-Albert Scale-Free Network
Joint Account Generation: Power-law degree distribution
Initial Balance Distribution: Exponential distribution (μ = 10)

2. Transaction Simulation Parameters
Total Transactions: 1000
Transaction Amount: 1 coin
Transaction Selection: Random user pair

3. Network Topology Analysis
3.1 Network Characteristics
Nodes: 100
Edges (Joint Accounts): 291
Average Node Degree: 5.82
Key Observations:
Scale-free network structure mimics real-world social networks
Power-law distribution ensures some nodes have higher connectivity
Network exhibits small-world network properties



4 . Transaction Performance Metrics

4.1 Transaction Success Rate
Total Transactions: 1000
Successful Transactions: 996
Success Rate: 99.60%



# Key Features

User registration simulation
Joint account creation
Power-law network generation
Transaction performance tracking
Detailed error handling and logging

# 🛠 Prerequisites

System Requirements
Python 3.8+
Node.js 14+
npm 6+
Required Software
Truffle
Ganache
Python Virtual Environment

# 💻 Installation

1. Clone the Repository

git clone https://github.com/suvchr105/layer2-dapp-tester.git
cd layer2-dapp-tester
2. Blockchain Development Tools Setup

# Install Truffle and Ganache globally
npm install -g truffle ganache-cli
3. Python Environment Setup

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install Python dependencies
pip install -r requirements.txt

# 📂 Project Structure


layer2-dapp-tester/
│
├── contracts/             # Solidity smart contracts
│   └── Layer2DApp.sol
│
├── migrations/            # Deployment scripts
│   └── 2_deploy_contracts.js
│
├── src/                   # Source code
│   └── layer2_dapp_tester.py
│
├── tests/                 # Test scripts
│   └── test_layer2_dapp.py
│
├── truffle-config.js      # Truffle configuration
├── requirements.txt       # Python dependencies
└── README.md
🔧 Configuration
Blockchain Configuration
Edit truffle-config.js:

# javascript

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*"
    }
  },
  compilers: {
    solc: {
      version: "0.8.13"
    }
  }
};
Application Parameters
Edit src/layer2_dapp_tester.py:


# Customize simulation parameters
tester = Layer2DAppTester(
    n_users=100,           # Number of simulated users
    network_type='barabasi' # Network generation algorithm
)

# Configure transaction simulation
success_rates = tester.run_transactions(
    n_transactions=1000,   # Total transactions to simulate
    transaction_size=1     # Base transaction amount
)
🚀 Running the Application
1. Start Local Blockchain

# Start Ganache
ganache-cli -a 100 -e 1000 --port 8545
2. Compile Smart Contracts

# In a new terminal
truffle compile
3. Deploy Contracts

truffle migrate --reset
4. Run DApp Tester

# Activate virtual environment
source venv/bin/activate

# Run the main script
python src/layer2_dapp_tester.py
🔍 Troubleshooting
Common Issues
Ganache Connection

Ensure Ganache is running
Check network configuration
Contract Deployment

Verify Solidity compiler version
Check gas limits
Inspect contract logic

Python Dependencies

# Reinstall dependencies
pip install -r requirements.txt --upgrade


# 🤝 Contributing
## Development Workflow
Fork the repository
Create a feature branch

git checkout -b feature/your-feature-name

Commit changes
Push to your branch
Create a Pull Request


# Coding Standards

Follow PEP 8 guidelines
Write comprehensive tests
Document new features


# 📊 Performance Monitoring

Metrics Tracked
Transaction success rates
Network topology
Gas consumption


# Visualization

Matplotlib success rate graphs
Console network statistics output


# 🔒 Security Considerations

Best Practices
Use latest web3.py version
Implement proper access controls
Add comprehensive error handling
Use environment variables
