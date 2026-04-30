import React, { useEffect, useState } from 'react';
import '../styles/modern.css';
import { API_BASE_URL } from '../apiBase';

interface Product {
  product_id: string;
  name: string;
  category: string;
  price: number;
  stock: number;
}

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/products/`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch products');
        return res.json();
      })
      .then(data => {
        // Defensive: handle both array and wrapped response
        if (Array.isArray(data)) {
          setProducts(data);
        } else if (data && data.result && data.result.structuredContent && typeof data.result.structuredContent.result === 'string') {
          // Parse the product string (MCP format)
          const text = data.result.structuredContent.result;
          const regex = /\[(.*?)\] (.*?)\n  Category: (.*?) \| Price: \\$(.*?) \| Stock: (.*?) units/g;
          const parsed: Product[] = [];
          let match;
          while ((match = regex.exec(text)) !== null) {
            parsed.push({
              product_id: match[1],
              name: match[2],
              category: match[3],
              price: parseFloat(match[4]),
              stock: parseInt(match[5], 10)
            });
          }
          setProducts(parsed);
        } else {
          setProducts([]);
        }
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="container">Loading products...</div>;
  if (error) return <div className="container error">Error: {error}</div>;

  return (
    <div className="container">
      <h2>Product Catalog</h2>
      {products.length === 0 ? (
        <div style={{textAlign: 'center', margin: '2rem 0', color: '#888'}}>
          <p>No products found. Please check back later or contact support.</p>
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Product ID</th>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {products.map(p => (
              <tr key={p.product_id}>
                <td>{p.product_id}</td>
                <td>{p.name}</td>
                <td>{p.category}</td>
                <td>${p.price.toFixed(2)}</td>
                <td>{p.stock}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Products;
