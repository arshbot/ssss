import React, { Component } from "react";
import { render } from "react-dom";
import Button from 'react-bootstrap/Button';

import InputField from "./InputField"

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
			refund_addr: 'bitcoin addr here',
			lightning_invoice: 'ln invoice here',
    };
  }

  componentDidMount() {}

  handleRefundAddrChange(event) {
		console.log(event)
		this.setState({refund_addr: event.target.value})
  }

	handleLnInvoiceChange(event) {
		this.setState({lightning_invoice: event.target.value})
	}

	handleGenerateHTLCClick(event) {
		const requestOptions = {
			method: 'POST',
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(
				{
					"refund_address": this.state.refund_addr,
					"bolt11_invoice": this.state.lightning_invoice
				}
			),
		}
		fetch("http://127.0.0.1:8000/api/btclnswap/", requestOptions)
			.then(response => response.text())
			.then(result => console.log(result))
			.catch(error => console.log('error', error));
	}

  render() {
    return (
			<div>
				<div>
					<h1> Hello World </h1>
					<textarea value={ this.state.refund_addr } onChange={this.handleRefundAddrChange.bind(this)}/>
				</div>
				<div>
					<h1> Hello World </h1>
					<textarea value={ this.state.lightning_invoice } onChange={this.handleLnInvoiceChange.bind(this)}/>
				</div>
  			<Button variant="success" onClick={this.handleGenerateHTLCClick.bind(this)}>Genereate HTLC</Button>{' '} </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
