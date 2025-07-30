import { render, screen, fireEvent } from '@testing-library/react';
import ChatPage from '../ChatWindow';
import '@testing-library/jest-dom';
import { describe, expect, test } from 'vitest';

describe('ChatPage', () => {

  test('should not send empty messages', () => {
    render(<ChatPage />);

    const input = screen.getByTestId('chat-input');
    const button = screen.getByTestId('send-button');

    fireEvent.change(input, { target: { value: '  ' } });
    fireEvent.click(button);

    const list = screen.getByTestId('message-list');
    expect(list).toBeEmptyDOMElement();
  });
});
