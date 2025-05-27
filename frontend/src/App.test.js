import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

test('renders learn react link', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
  const linkElements = screen.getAllByText(/рецепты/i);
  expect(linkElements.length).toBeGreaterThan(0);
});
