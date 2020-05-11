import React, { Component } from "react";
import { render } from "react-dom";

export default class HeaderText extends Component {
  constructor(props) {
    super(props)
  }

  componentDidMount() {}

  render() {
    return (
      <div style={header}>
        <div>
          <h1> Simple Subswap Server </h1>
          <label>This site exists to demo and debug submarine swaps</label>
        </div>
      </div>
    );
  }
}

const header = {
  marginTop: '20px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}