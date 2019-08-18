import { useState, useEffect } from 'react';
import base_url from './base_url';


// Function inside useEffect (()=>{})() declared and executed like this
// because it is async, then the [] will allow to only make request first time.
const LoadEnvs = () => {
  const [ envs, setEnvs ] = useState([]);

  useEffect(() => {
    (async () => {
      const response =  await base_url.get('/allenvs');
      setEnvs(response.data);
    })()
  }, [])

  return envs
}

export default LoadEnvs;
