import React, { Component } from "react";
import 'antd/dist/antd.css';


export default class Divider extends Component {
  render() {
    return (
        <div style={htlcdivider}>
        <h2 style={h2}>
          <span style={span}>
            H T L C&nbsp;&nbsp;&nbsp;&nbsp;C O N S T R U C T I O N
          </span>
        </h2>
      </div>
    );
  }
}


const h2 = {
    width: "80%",
    textAlign: "center",
    borderBottom: "1px solid #DCDCDC",
    lineHeight: "0.1em",
    margin: "10px 0 20px",
    // color: "#DCD",
    // background: "#DCDCDC",
    display: "inline-block",
  }
  
  const span = {
    background: "#fff",
    padding: "0 10px",
    color: "#DCDCDC",
    fontSize: "13px",
    fontWeight: "normal",
  }
  const htlcdivider = {
    marginTop: "60px",
    position: "relative",
    marginBottom: "20px",
    width: "100%",
    textAlign: "center",
    // color: "#DCDCDC",
  }