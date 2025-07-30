import React, { useState } from 'react';
import { handleUserQuery } from '../api/service';

const ChatWindow = () => {
    const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState<{
    id: string;
    role: string;
    content: string;
  }[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendPrompt();
    }
  }

  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    setPrompt('');
    setMessages((messages) => [...messages, { id: Date.now().toString() + '_user', role: 'user', content: prompt }]);
    try {
      const response = await handleUserQuery(prompt);
      setMessages((messages) => [...messages, { id: Date.now().toString() + '_assistant', role: 'assistant', content: response?.map((item: any) => <li>{item.summary}</li>) }]);
      console.log('response', response)
    } catch (error) {
      console.log('error', error)
    }
  }
    return (
    <>
      <h1 className='text-center mt-2'>Project Intelligence</h1>
      <div
        data-testid='message-list'
        className="flex flex-col min-h-[75vh] max-h-[75vh] overflow-y-scroll px-4"
      >
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-2`}
          >
            <div
              className={`max-w-[70%] px-4 py-2 rounded-2xl ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-none'
                  : 'bg-gray-200 text-black rounded-bl-none'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
      </div>
      <div className='flex flex-row justify-center gap-x-4 w-[100%] absolute bottom-0 mb-10'>
        <div className='w-1/2'>
          <label htmlFor="input-prompt">
            <input
              data-testid='chat-input'
              className='w-full'
              name='input-prompt'
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyDown}
            />
          </label>
        </div>
        
        <button
          data-testid='send-button'
          onClick={sendPrompt}
          disabled={prompt.trim() === ''}
        >
          Enter
        </button>
      </div>
    </>
  )
}

export default ChatWindow;