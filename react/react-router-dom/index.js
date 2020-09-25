// original owner: https://www.youtube.com/channel/UCvc8kv-i5fvFTJBFAk6n1SA
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';
import {HashRouter, Route, Switch, Link, NavLink, useParams} from 'react-router-dom';

function Home() {
  return (
    <div>
      <h2>Home</h2>
      Home...
    </div>
  );
}

const contents = [
  {id:1, title:'HTML', description:'HTML is ...'},
  {id:2, title:'JS', description:'JS is ...'},
  {id:3, title:'CSS', description:'CSS is ...'}
]

function Topic() {
  const params = useParams();
  const desc = contents.filter(c => c.id == params.topic_id)[0].description;
  return (
    <div>
      <h3>Topic</h3>
      {desc}
    </div>
  );
}

function Topics() {
  return (
    <div>
      <h2>Topics</h2>
      <ul>
        {contents.map(c  => (<li><NavLink to={"/topics/" + c.id}>{c.title}</NavLink></li>))}
      </ul>
      <Route path="/topics/:topic_id"><Topic/></Route>
    </div>
  );
}
function Contact() {
  return (
    <div>
      <h2>Contact</h2>
      Contact...
    </div>
  );
}

function App() {
  return (
    <div>
      <h1>React Router DOM example</h1>
      <ul>
      <li><NavLink exact to="/">Home</NavLink></li>
      <li><NavLink to="/topics">Topics</NavLink></li>
      <li><NavLink to="/contact">Contact</NavLink></li>
      </ul>
      <Switch>
        <Route exact path="/"><Home/></Route>
        <Route path="/topics"><Topics/></Route>
        <Route path="/contact"><Contact/></Route>
        <Route path="/">Not Found</Route>
      </Switch>
    </div>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <HashRouter>
      <App />
    </HashRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorker.unregister();
