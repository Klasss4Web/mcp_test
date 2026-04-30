import React, { useState } from 'react';
import '../styles/modern.css';
import { API_BASE_URL } from '../apiBase';

const Login: React.FC<{ onLogin: (customerId: string) => void }> = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [pin, setPin] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      // Step 1: Get customer
      const res1 = await fetch(`${API_BASE_URL}/auth/customer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const customerText = await res1.text();
      let customer;
      try {
        customer = JSON.parse(customerText);
      } catch (err) {
        console.error('Customer response is not JSON:', customerText);
        throw new Error('Customer lookup failed');
      }
      console.log('Customer lookup response:', customer);
      if (!res1.ok || !customer.customer_id) throw new Error('Customer not found');

      // Step 2: Verify PIN
      console.log('Verifying PIN for:', customer.customer_id, pin);
      const res2 = await fetch(`${API_BASE_URL}/auth/verify-pin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_id: customer.customer_id, pin })
      });
      const verifyText = await res2.text();
      let verifyResult;
      try {
        verifyResult = JSON.parse(verifyText);
      } catch (err) {
        console.error('Verify PIN response is not JSON:', verifyText);
        throw new Error('PIN verification failed');
      }
      console.log('Verify PIN response:', verifyResult);
      if (!res2.ok) throw new Error('Invalid PIN');
      onLogin(customer.customer_id);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="container">
      <h2>Customer Login</h2>
      <div>
        <label>Email:<br/>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </label>
      </div>
      <div>
        <label>PIN:<br/>
          <input type="password" value={pin} onChange={e => setPin(e.target.value)} required />
        </label>
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
};

export default Login;
