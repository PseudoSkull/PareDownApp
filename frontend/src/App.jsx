import { useState } from 'react'
import './App.css'
import DataForm from './components/TestItemForm'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Pare-Down App</h1>
      <DataForm />
    </>
  )
}

export default App
