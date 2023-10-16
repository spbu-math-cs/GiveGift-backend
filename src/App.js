import React, {useState, useEffect} from 'react'
import './App.css';

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/app").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await axios.get('http://localhost:5000')
  //       setData(response.data)
  //     } catch (error) {
  //       console.error('Error', error)
  //     }
  //   };

  //   fetchData()
  // }, [])

  return (
    <div>

      <div className='upper'>
        <p>Lorum ipsum что-то там хз что</p>
      </div>
      
      <div className='field'>
        {(typeof data.members === 'undefined') ? (
          <p>Loading...</p>
        ): (
        data.members.map((members, i) => (
          <p key={i}>{members}</p>
          ))
        )}
      </div>

    </div>
  );
}

export default App;
