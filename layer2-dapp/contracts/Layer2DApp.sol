// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Layer2DApp {
    struct User {
        string name;
        bool exists;
        uint[] connectedUsers;
    }
    
    struct JointAccount {
        bool exists;
        uint balance1;  // balance of user1
        uint balance2;  // balance of user2
    }
    
    // Store parent mapping at contract level
    mapping(uint => uint) private pathParent;
    mapping(uint => User) public users;
    // Maps hash of user IDs to their joint account
    mapping(bytes32 => JointAccount) public jointAccounts;
    
    // Helper function to create consistent hash for joint accounts
    function createAccountHash(uint user1, uint user2) private pure returns (bytes32) {
        require(user1 != user2, "Cannot create account with self");
        if (user1 < user2) {
            return keccak256(abi.encodePacked(user1, user2));
        }
        return keccak256(abi.encodePacked(user2, user1));
    }
    
    function registerUser(uint userId, string memory userName) public {
        require(!users[userId].exists, "User already exists");
        users[userId].name = userName;
        users[userId].exists = true;
    }
    
    function createAcc(uint user1, uint user2, uint initialBalance1, uint initialBalance2) public {
        require(users[user1].exists && users[user2].exists, "Users must exist");
        bytes32 accountHash = createAccountHash(user1, user2);
        require(!jointAccounts[accountHash].exists, "Joint account already exists");
        
        // Initialize joint account with provided balances
        jointAccounts[accountHash].exists = true;
        jointAccounts[accountHash].balance1 = initialBalance1;
        jointAccounts[accountHash].balance2 = initialBalance2;
        
        // Add users to each other's connected users list
        users[user1].connectedUsers.push(user2);
        users[user2].connectedUsers.push(user1);
    }
    
    // Helper function to find path between users using BFS
    function findPath(uint start, uint end) private returns (uint[] memory) {
        if (start == end) return new uint[](0);
        
        uint[] memory queue = new uint[](10000);
        bool[] memory visited = new bool[](10000);
        
        uint front = 0;
        uint back = 0;
        
        queue[back++] = start;
        visited[start] = true;
        
        bool found = false;
        while (front < back && !found) {
            uint currentNode = queue[front++];
            
            for (uint i = 0; i < users[currentNode].connectedUsers.length; i++) {
                uint neighbor = users[currentNode].connectedUsers[i];
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    pathParent[neighbor] = currentNode;
                    queue[back++] = neighbor;
                    
                    if (neighbor == end) {
                        found = true;
                        break;
                    }
                }
            }
        }
        
        if (!found) return new uint[](0);
        
        // Reconstruct path
        uint pathLength = 0;
        uint curr = end;
        while (curr != start) {
            pathLength++;
            curr = pathParent[curr];
        }
        
        uint[] memory path = new uint[](pathLength + 1);
        curr = end;
        for (uint i = pathLength; i > 0; i--) {
            path[i] = curr;
            curr = pathParent[curr];
        }
        path[0] = start;
        
        return path;
    }
    
    function sendAmount(uint from, uint to, uint amount) public returns (bool) {
        require(users[from].exists && users[to].exists, "Users must exist");
        require(from != to, "Cannot send to self");
        
        uint[] memory path = findPath(from, to);
        if (path.length == 0) return false;
        
        // Check if entire path has sufficient balance
        for (uint i = 0; i < path.length - 1; i++) {
            bytes32 accountHash = createAccountHash(path[i], path[i + 1]);
            JointAccount storage account = jointAccounts[accountHash];
            
            if (path[i] < path[i + 1]) {
                if (account.balance1 < amount) return false;
            } else {
                if (account.balance2 < amount) return false;
            }
        }
        
        // Transfer amount along the path
        for (uint i = 0; i < path.length - 1; i++) {
            bytes32 accountHash = createAccountHash(path[i], path[i + 1]);
            JointAccount storage account = jointAccounts[accountHash];
            
            if (path[i] < path[i + 1]) {
                account.balance1 -= amount;
                account.balance2 += amount;
            } else {
                account.balance2 -= amount;
                account.balance1 += amount;
            }
        }
        
        return true;
    }
    
    function closeAccount(uint user1, uint user2) public {
        require(users[user1].exists && users[user2].exists, "Users must exist");
        bytes32 accountHash = createAccountHash(user1, user2);
        require(jointAccounts[accountHash].exists, "Joint account does not exist");
        
        // Remove the account
        delete jointAccounts[accountHash];
        
        // Remove users from each other's connected users list
        for (uint i = 0; i < users[user1].connectedUsers.length; i++) {
            if (users[user1].connectedUsers[i] == user2) {
                users[user1].connectedUsers[i] = users[user1].connectedUsers[users[user1].connectedUsers.length - 1];
                users[user1].connectedUsers.pop();
                break;
            }
        }
        
        for (uint i = 0; i < users[user2].connectedUsers.length; i++) {
            if (users[user2].connectedUsers[i] == user1) {
                users[user2].connectedUsers[i] = users[user2].connectedUsers[users[user2].connectedUsers.length - 1];
                users[user2].connectedUsers.pop();
                break;
            }
        }
    }
    
    // Helper function to get account balance
    function getAccountBalance(uint user1, uint user2) public view returns (uint, uint) {
        bytes32 accountHash = createAccountHash(user1, user2);
        require(jointAccounts[accountHash].exists, "Joint account does not exist");
        return (jointAccounts[accountHash].balance1, jointAccounts[accountHash].balance2);
    }
}