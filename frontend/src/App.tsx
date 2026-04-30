import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Products from './pages/Products';
import Login from './pages/Login';
import Order from './pages/Order';
import OrderHistory from './pages/OrderHistory';
import { API_BASE_URL } from './apiBase';
import ChatWidget from './components/ChatWidget';

function App() {
  const [customerId, setCustomerId] = useState<string | null>(null);
  const [products, setProducts] = useState<any[]>([]);

  // Fetch products once after login for order page
  React.useEffect(() => {
    if (customerId) {
      fetch(`${API_BASE_URL}/products/`)
        .then(res => res.json())
        .then(setProducts);
    }
  }, [customerId]);

  return (
    <Router>
      <nav style={{padding: '1rem', background: '#f5f5f5'}}>
        <Link to="/">Home</Link> |{' '}
        <Link to="/products">Products</Link> |{' '}
        <Link to="/login">Login</Link>
        {customerId && (
          <>
            {' '}| <Link to="/order">Order</Link> |{' '}
            <Link to="/orders/history">Order History</Link>
          </>
        )}
      </nav>
      <div style={{position: 'relative', minHeight: '80vh'}}>
        <Routes>
          <Route path="/products" element={<Products />} />
          <Route path="/login" element={<Login onLogin={setCustomerId} />} />
          <Route path="/order" element={customerId ? <Order customerId={customerId} products={products} /> : <Login onLogin={setCustomerId} />} />
          <Route path="/orders/history" element={customerId ? <OrderHistory customerId={customerId} /> : <Login onLogin={setCustomerId} />} />
          <Route path="/" element={
            <div className="container" style={{textAlign: 'center'}}>
              <h1>Welcome to Meridian Electronics</h1>
              <p style={{fontSize: '1.2rem', margin: '1.5rem 0'}}>
                Your one-stop shop for computers, accessories, and more.<br/>
                Need help? Our AI-powered support chatbot is here to assist you with product info, orders, and account questions.
              </p>
              <div style={{
                background: '#f0f6ff',
                border: '1px solid #b3d1ff',
                borderRadius: 12,
                maxWidth: 520,
                margin: '2rem auto',
                padding: '1.5rem',
                boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                textAlign: 'left',
                fontSize: '1.08rem',
                color: '#1a237e',
                position: 'relative'
              }}>
                <div style={{display: 'flex', alignItems: 'flex-start', gap: 12}}>
                  <div style={{fontSize: 32, marginTop: 2}}>🤖</div>
                  <div>
                    <b>What can our AI-powered chatbot help you with?</b>
                    <ul style={{margin: '0.5rem 0 0 1.2rem', padding: 0}}>
                      <li>Checking product availability</li>
                      <li>Helping customers place orders</li>
                      <li>Looking up order history</li>
                      <li>Authenticating returning customers</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div style={{margin: '2rem 0'}}>
                <Link to="/products" className="btn-primary">Browse Products</Link>
                <span style={{margin: '0 1rem'}}></span>
                <Link to="/login" className="btn-secondary">Customer Login</Link>
              </div>
              <img src="/public/hero-electronics.svg" alt="Electronics" style={{maxWidth: 320, margin: '2rem auto', display: 'block'}} />
            </div>
          } />
        </Routes>
        <ChatWidget />
      </div>
    </Router>
  );
}

export default App;
