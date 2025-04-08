import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MindMap } from '../../components/MindMap';
import { MockedProvider } from '@apollo/client/testing';
import { useRouter } from 'next/router';

// Mock next/router
jest.mock('next/router', () => ({
  useRouter: jest.fn(),
}));

// Mock WebSocket
global.WebSocket = jest.fn();

describe('MindMap Component', () => {
  const mockMindMap = {
    id: '1',
    title: 'Test Mind Map',
    description: 'Test Description',
    nodes: [
      {
        id: '1',
        content: 'Root Node',
        position: { x: 0, y: 0 },
      },
      {
        id: '2',
        content: 'Child Node',
        position: { x: 100, y: 100 },
      },
    ],
    edges: [
      {
        id: '1',
        source: '1',
        target: '2',
      },
    ],
  };

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({
      query: { id: '1' },
      push: jest.fn(),
    });
  });

  it('renders mind map title and description', () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    expect(screen.getByText('Test Mind Map')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('renders nodes and edges', () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    expect(screen.getByText('Root Node')).toBeInTheDocument();
    expect(screen.getByText('Child Node')).toBeInTheDocument();
  });

  it('handles node creation', async () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    const addButton = screen.getByTestId('add-node-button');
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(screen.getByText('New Node')).toBeInTheDocument();
    });
  });

  it('handles node editing', async () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    const node = screen.getByText('Root Node');
    fireEvent.click(node);

    const editButton = screen.getByTestId('edit-node-button');
    fireEvent.click(editButton);

    const input = screen.getByTestId('node-content-input');
    fireEvent.change(input, { target: { value: 'Updated Node' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    await waitFor(() => {
      expect(screen.getByText('Updated Node')).toBeInTheDocument();
    });
  });

  it('handles node deletion', async () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    const node = screen.getByText('Root Node');
    fireEvent.click(node);

    const deleteButton = screen.getByTestId('delete-node-button');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(screen.queryByText('Root Node')).not.toBeInTheDocument();
    });
  });

  it('handles edge creation', async () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    const sourceNode = screen.getByText('Root Node');
    const targetNode = screen.getByText('Child Node');

    fireEvent.mouseDown(sourceNode);
    fireEvent.mouseMove(targetNode);
    fireEvent.mouseUp(targetNode);

    await waitFor(() => {
      expect(screen.getByTestId('edge-1-2')).toBeInTheDocument();
    });
  });

  it('handles edge deletion', async () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    const edge = screen.getByTestId('edge-1-2');
    fireEvent.click(edge);

    const deleteButton = screen.getByTestId('delete-edge-button');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(screen.queryByTestId('edge-1-2')).not.toBeInTheDocument();
    });
  });

  it('handles real-time updates', async () => {
    const mockWebSocket = {
      send: jest.fn(),
      close: jest.fn(),
    };
    (global.WebSocket as jest.Mock).mockImplementation(() => mockWebSocket);

    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    // Simulate WebSocket message
    const wsMessage = {
      type: 'node_created',
      node: {
        id: '3',
        content: 'New Node',
        position: { x: 200, y: 200 },
      },
    };

    mockWebSocket.onmessage({ data: JSON.stringify(wsMessage) });

    await waitFor(() => {
      expect(screen.getByText('New Node')).toBeInTheDocument();
    });
  });

  it('handles collaboration', async () => {
    const mockWebSocket = {
      send: jest.fn(),
      close: jest.fn(),
    };
    (global.WebSocket as jest.Mock).mockImplementation(() => mockWebSocket);

    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    // Simulate collaborator joining
    const collaboratorMessage = {
      type: 'collaborator_joined',
      user: {
        id: '2',
        name: 'Collaborator',
      },
    };

    mockWebSocket.onmessage({ data: JSON.stringify(collaboratorMessage) });

    await waitFor(() => {
      expect(screen.getByText('Collaborator')).toBeInTheDocument();
    });
  });

  it('handles undo/redo', async () => {
    render(
      <MockedProvider>
        <MindMap mindMap={mockMindMap} />
      </MockedProvider>
    );

    // Create a new node
    const addButton = screen.getByTestId('add-node-button');
    fireEvent.click(addButton);

    // Undo the action
    const undoButton = screen.getByTestId('undo-button');
    fireEvent.click(undoButton);

    await waitFor(() => {
      expect(screen.queryByText('New Node')).not.toBeInTheDocument();
    });

    // Redo the action
    const redoButton = screen.getByTestId('redo-button');
    fireEvent.click(redoButton);

    await waitFor(() => {
      expect(screen.getByText('New Node')).toBeInTheDocument();
    });
  });
}); 