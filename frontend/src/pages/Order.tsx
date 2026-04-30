import React, { useState } from 'react';
import '../styles/modern.css';
import { API_BASE_URL } from '../apiBase';

interface OrderProps {
  customerId: string;
  products: { product_id: string; name: string }[];
}

const Order: React.FC<OrderProps> = ({ customerId, products }) => {
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const res = await fetch(`${API_BASE_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_id: customerId, product_id: productId, quantity })
      });
      if (!res.ok) throw new Error('Order failed');
      setMessage('Order placed successfully!');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleOrder} className="container">
      <h2>Place Order</h2>
      <div>
        <label>Product:<br/>
          <select value={productId} onChange={e => setProductId(e.target.value)} required>
            <option value="">Select a product</option>
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>{p.name}</option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>Quantity:<br/>
          <input type="number" min={1} value={quantity} onChange={e => setQuantity(Number(e.target.value))} required />
        </label>
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Placing...' : 'Place Order'}</button>
      {message && <div className="success">{message}</div>}
      {error && <div className="error">{error}</div>}
    </form>
  );
};

export default Order;
