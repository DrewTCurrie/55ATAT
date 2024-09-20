import {Button} from 'react-bootstrap';
import axios from 'axios';
import './App.css';

function App() {


  const generateReport = () => {
    fetch("http://192.168.1.12:5000/api/generateReport").then(
      res => res.json()
    ).then(
        data => {
          console.log(data)
          axios.get(`http://192.168.1.12:5000/api/download/${data}`,{responseType: 'blob'}
          ).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${data}`);
            document.body.appendChild(link);
            link.click();
          }
          );
        }
    )
  }

  return (
    <div className="App">
      <header className="App-header">
        Excel Report Generation Prototype
        <Button variant="primary" size="lg" onClick={generateReport}>
          Generate Report
        </Button>
      </header>
    </div>
  );
}

export default App;

