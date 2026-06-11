import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/inter/700.css';
import '@fontsource/geist-sans/400.css';
import '@fontsource/geist-sans/500.css';
import '@fontsource/geist-mono/400.css';
import { App } from './App';
import './demo.css';

const container = document.getElementById('root');
if (!container) {
  throw new Error('Demo root element not found.');
}
createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
