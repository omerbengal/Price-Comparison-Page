import { useState } from 'react';
import axios from 'axios';
import styles from "@/styles/Table.module.css"; // Adjust the path based on your project structure

export default function Home() {
  const [productName, setProductName] = useState('');
  const [tableData, setTableData] = useState({ 'Best Buy': { 'Item title name': '', 'Price(USD)': '' }, 'Walmart': { 'Item title name': '', 'Price(USD)': '' }, 'Newegg': { 'Item title name': '', 'Price(USD)': '' } });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchtableData = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.get(`http://127.0.0.1:8000/tableData?item=${encodeURIComponent(productName)}`);
      setTableData(response.data);
    } catch (err) {
      setError('Failed to fetch data. Please check the product name and try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchtableData();
  };

  return (
    <div className={styles.tableContainer}>
      <h1 className={styles.h1}>Product Prices Comparison</h1>
      <br />
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          className={styles.input}
          type="text"
          placeholder="Enter a product name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          required
        />
        <button type="submit" disabled={loading} className={styles.button}>
          {loading ? 'Loading...' : 'Compare Prices'}
        </button>
      </form>
      <br />
      <text className={styles.text}>
        {error && <p>{error}</p>}
      </text>
      <br />
      <table className={styles.table}>
        <thead>
          <tr className={styles.tr}>
            <th className={styles.th}>Site</th>
            <th className={styles.th}>Product</th>
            <th className={styles.th}>Price</th>
          </tr>
        </thead>
        <tbody>
          {
            Object.entries(tableData).map(([site, data]) => (
              <tr key={site} className={styles.tr}>
                <td className={styles.td}>{site}</td>
                <td className={styles.td}>{data['Item title name'] ? <a href={data['Item title name']} target="_blank" className={styles.a}>{data['Item title name']}</a> : 'N/A'}</td>
                <td className={styles.td}>{data['Price(USD)'] ? `$${data['Price(USD)']}` : 'N/A'}</td>
              </tr>
            ))
          }
        </tbody>
      </table>
    </div>
  );
}
