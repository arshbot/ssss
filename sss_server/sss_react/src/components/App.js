import React, { Component } from "react";
import { render } from "react-dom";
import Button from 'react-bootstrap/Button';

import InputField from "./InputField"

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
			refund_addr: '1NiNja1bUmhSoTXozBRBEtR8LeF9TGbZBN',
			lightning_invoice: 'lntb1500n1p0trcq7pp5h78cqzkdasysywc88y70zk54hr6sr5fphh9uhz6fsg0n26rlwrzsdqh2fjkzep6yppxzapqwdhh2uqcqzpgxqr23ssp5ccp9g66p03jny6vk3qzzthwqd0d4wqlwfsp50g8c8ykfqhm7e50s9qy9qsqep9r0ffppp5075puvr32609zznduh70mfewwkp4c5qd53j7vge0r5gjw8ewd57pdf4mqwdlleafp4v4f7k9mwdzvcwmtz473p9nvvpqpeqjqrc',
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
      .then(response => JSON.parse(response))
			.then(result => { 
          this.setState({htlc_p2sh: result.htlc_p2sh})
        }
      )
			.catch(error => console.log('error', error));
	}

  render() {
    console.log(this.state.htlc_p2sh)
    return (
			<div>
				<div>
					<h1> Hello TOOL </h1>
					<textarea value={ this.state.refund_addr } onChange={this.handleRefundAddrChange.bind(this)}/>
				</div>
				<div>
					<h1> Hello World </h1>
					<textarea value={ this.state.lightning_invoice } onChange={this.handleLnInvoiceChange.bind(this)}/>
				</div>
        <div>
          <Button variant="success" onClick={this.handleGenerateHTLCClick.bind(this)}>Genereate HTLC</Button>{' '}
        </div>
        <div>
          { this.state.htlc_p2sh ? <label> { this.state.htlc_p2sh } </label> : null }
        </div>
      </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
