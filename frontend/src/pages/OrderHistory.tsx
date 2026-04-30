import React, { useEffect, useState } from 'react';
import '../styles/modern.css';
import { API_BASE_URL } from '../apiBase';

interface Order {
  order_id: string;
  product_id: string;
  quantity: number;
  status?: string;
}

const OrderHistory: React.FC<{ customerId: string }> = ({ customerId }) => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/orders/history?customer_id=${customerId}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch orders');
        return res.json();
      })
      .then(setOrders)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [customerId]);

  if (loading) return <div className="container">Loading order history...</div>;
  if (error) return <div className="container error">Error: {error}</div>;

  return (
    <div className="container">
      <h2>Order History</h2>
      <table>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Product ID</th>
            <th>Quantity</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(o => (
            <tr key={o.order_id}>
              <td>{o.order_id}</td>
              <td>{o.product_id}</td>
              <td>{o.quantity}</td>
              <td>{o.status || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OrderHistory;
