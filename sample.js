// Sample JavaScript file for testing PyCodeLens

function greet(name) {
    console.log(`Hello, ${name}!`);
    return `Hello, ${name}!`;
  }
  
  // ES6 class
  class User {
    constructor(name, email) {
      this.name = name;
      this.email = email;
    }
    
    displayInfo() {
      console.log(`User: ${this.name}, Email: ${this.email}`);
    }
    
    static createAdmin() {
      return new User('Admin', 'admin@example.com');
    }
  }
  
  // Arrow function
  const calculateTotal = (items) => {
    return items.reduce((total, item) => total + item.price, 0);
  };
  
  // Async function
  async function fetchData(url) {
    try {
      const response = await fetch(url);
      return await response.json();
    } catch (error) {
      console.error('Error fetching data:', error);
      return null;
    }
  }