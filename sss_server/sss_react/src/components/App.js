import React, { Component } from "react";
import { render } from "react-dom";
import Button from 'react-bootstrap/Button';
import TextField from '@material-ui/core/TextField';


import HeaderText from "./HeaderText"
import SSSSInputs from "./SSSSInputs"

class App extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {}

  render() {

    return (
			<div style={{fontFamily: 'Roboto'}}>
        <HeaderText/>
        <SSSSInputs/>
      </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
