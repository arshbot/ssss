import React, { Component } from "react";
import { render } from "react-dom";

export default class InputField extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
  }

  componentDidMount() {
  }

  render() {
    return (
      <div>
        <textarea value='bitcoin refund address here tattere'/>
      </div>
    );
  }
}

