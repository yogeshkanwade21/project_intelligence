import { useState } from 'react'
import './App.css'
import { handleUserQuery } from './api/service';

function App() {
  const [prompt, setPrompt] = useState('');

  const sendPrompt = async () => {
    try {
      const response = await handleUserQuery(prompt);
      console.log('response', response)
    } catch (error) {
      console.log('error', error)
    }
  }

  return (
    <>
      <h1 className='text-center mt-2'>Project Intelligence</h1>
      <div className='flex flex-row justify-center gap-x-4 w-[100%] absolute bottom-0 mb-10'>
        <div className='w-1/2'>
          <label htmlFor="input-prompt">
            <input
              className='w-full'
              name='input-prompt'
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </label>
        </div>
        
        <button
          onClick={sendPrompt}
        >
          Enter
        </button>
      </div>
    </>
  )
}

export default App
