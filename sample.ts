// Sample TypeScript file for testing PyCodeLens

// Interface
interface Product {
    id: number;
    name: string;
    price: number;
    inStock: boolean;
  }
  
  // Class with typed properties
  class ShoppingCart {
    private items: Product[] = [];
    
    constructor(private readonly userId: string) {}
    
    addItem(product: Product): void {
      if (product.inStock) {
        this.items.push(product);
        console.log(`Added ${product.name} to cart`);
      }
    }
    
    getTotal(): number {
      return this.items.reduce((total, item) => total + item.price, 0);
    }
  }
  
  // Function with type annotations
  function processOrder(cart: ShoppingCart, userRole: string): boolean {
    if (userRole === 'guest') {
      console.log('Guests cannot place orders');
      return false;
    }
    
    const total = cart.getTotal();
    console.log(`Processing order with total: $${total}`);
    return true;
  }