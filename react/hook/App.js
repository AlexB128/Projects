// original owner: https://www.youtube.com/channel/UCvc8kv-i5fvFTJBFAk6n1SA
import React, {useState, useEffect} from 'react';
import './App.css';

/*
useEffect 2nd param	componentDidMount	componentDidUpdate	useEffect return fcuntion
    n/a	                O	                    O	            componetWillUpdate
    []	                O	                    X	    compontnWillUpdate && componetWillUnmount
  [state]	            O	                    O	            componetWillUpdate
*/

function App() {
  const [show, setShow] = useState({func: true, class: true});
  console.log('app');
  return (
    <div className="container">
      <h1>Hello World</h1>
      <input type="button" value="func" onClick={() => {setShow({...show, func: !show.func})}}/>
      <input type="button" value="class" onClick={() => {setShow({...show, class: !show.class})}}/>
      {show.func ? <FuncComp initNumber={2}/> : null }
      {show.class ? <ClassComp initNumber={2}/> : null }
    </div>
  );
}

const funcStyle = 'color:blue';
let funcId = 0;
function FuncComp(props) {  //1st param is props
  const [number, setNumber] = useState(props.initNumber);
  const [date, setDate] = useState(new Date().toLocaleString());

  // componentDidMount componentDidUpdate
  useEffect(() => {
    console.log('%cfunc => useEffect: componentDidMount && componentDidUpdate' + (++funcId), funcStyle);
    document.title = date; 
    return () => {
      console.log('%cfunc => useEffect: cleanUp' + (++funcId), funcStyle);
    };
  }, [date]);

  console.log('%cfunc => render' + (++funcId), funcStyle);
  return (
    <div className="container">
      <h2>function style</h2>
      <p>Number: {number}</p>
      <p>Date: {date}</p>
      <input type="button" value="random" onClick={
          () => setNumber(Math.random())
      } />    
      <input type="button" value="Update Time" onClick={
        () => setDate(new Date().toLocaleString())
      } />          
    </div>
  );
}

const classStyle = 'color:red';
class ClassComp extends React.Component {
  constructor(props) {
    super(props);
    console.log('%cclass => constructor', classStyle);
    this.state = {
      number: props.initNumber,
      date: new Date().toLocaleString()
    }
  }
  componentWillMount() {
    console.log('%cclass => componentWillMount', classStyle);
  }
  componentDidMount() {
    console.log('%cclass => componentDidMount', classStyle);
  }
  shouldComponentUpdate() {
    console.log('%cclass => shouldComponentUpdate', classStyle);
    return true;
  }
  componentDidUpdate() {
    console.log('%cclass => componentDidUpdate', classStyle);
  }
  compo
  render() {
    console.log('%cclass => render', classStyle);
    return (
      <div className="container">
        <h2>class style</h2>
        <p>Number: {this.state.number}</p>
        <p>Date: {this.state.date}</p>
        <input type="button" value="random" onClick={
          () => this.setState({number: Math.random()})
        } />
        <input type="button" value="Update Time" onClick={
          () => this.setState({date: new Date().toLocaleString()})
        } />
      </div>
    );
  }
}

export default App;
