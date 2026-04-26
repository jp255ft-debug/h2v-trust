export default function TestPage() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Test Page - H2V Trust</h1>
      <p>If you can see this, Next.js is working correctly!</p>
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f9ff', border: '1px solid #bae6fd', borderRadius: '8px' }}>
        <h3>System Status:</h3>
        <ul>
          <li>✅ Next.js: Running</li>
          <li>✅ React: Loaded</li>
          <li>✅ TypeScript: Configured</li>
          <li>✅ Tailwind: Ready</li>
        </ul>
      </div>
    </div>
  );
}