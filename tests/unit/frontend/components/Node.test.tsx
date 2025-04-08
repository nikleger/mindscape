import { render, screen, fireEvent } from '@testing-library/react';
import { Node } from '../../../../packages/frontend/src/components/Node';

describe('Node Component', () => {
  const mockNode = {
    id: '1',
    content: 'Test Node',
    x: 0,
    y: 0,
    width: 100,
    height: 50,
  };

  it('renders node content correctly', () => {
    render(<Node node={mockNode} />);
    expect(screen.getByText('Test Node')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Node node={mockNode} onClick={handleClick} />);
    fireEvent.click(screen.getByText('Test Node'));
    expect(handleClick).toHaveBeenCalledWith(mockNode.id);
  });

  it('applies correct styles based on position', () => {
    render(<Node node={mockNode} />);
    const nodeElement = screen.getByText('Test Node').parentElement;
    expect(nodeElement).toHaveStyle({
      position: 'absolute',
      left: '0px',
      top: '0px',
      width: '100px',
      height: '50px',
    });
  });
}); 