import { fireEvent, render, screen } from '@testing-library/react';
import io from 'socket.io-client';
import App from './App';

jest.mock('socket.io-client');

const socket = { on: jest.fn(), off: jest.fn(), emit: jest.fn(), disconnect: jest.fn() };

// CRA's jest config resets mock implementations before each test
beforeEach(() => {
  io.mockReturnValue(socket);
});

const typeName = (name) => fireEvent.change(screen.getByLabelText(/your name/i), { target: { value: name } });

test('renders the name screen', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /rock paper scissors/i })).toBeInTheDocument();
  expect(screen.getByLabelText(/your name/i)).toBeInTheDocument();
});

test('disables Play until a name is entered', () => {
  render(<App />);
  const play = screen.getByRole('button', { name: 'Play' });
  expect(play).toBeDisabled();

  typeName('   ');
  expect(play).toBeDisabled();

  typeName('Dustin');
  expect(play).toBeEnabled();
});

test('entering a name sends it and shows the game screen', () => {
  render(<App />);
  typeName('  Dustin ');
  fireEvent.click(screen.getByRole('button', { name: 'Play' }));

  expect(socket.emit).toHaveBeenCalledWith('username', 'Dustin');
  expect(screen.getByRole('button', { name: /play round/i })).toBeInTheDocument();
  expect(screen.getByText('Dustin')).toBeInTheDocument();
  expect(screen.getByText(/no streaks yet/i)).toBeInTheDocument();
});

test('game buttons emit start and reset events', () => {
  render(<App />);
  typeName('Dustin');
  fireEvent.click(screen.getByRole('button', { name: 'Play' }));

  fireEvent.click(screen.getByRole('button', { name: /play round/i }));
  expect(socket.emit).toHaveBeenCalledWith('start_game');

  fireEvent.click(screen.getByRole('button', { name: /reset scores/i }));
  expect(socket.emit).toHaveBeenCalledWith('reset_game');
});
