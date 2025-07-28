import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router";
import './index.css'
import App from './App.tsx'
import LoginPage from './pages/LoginPage.tsx';
import ChatWindow from './components/ChatWindow.tsx';

const router = createBrowserRouter([
  {
    path: "/chat",
    element: <ChatWindow />,
  },
  {
    path: "/signin",
    element: <LoginPage />,
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
