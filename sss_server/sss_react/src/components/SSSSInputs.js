import React, { Component } from "react";

import InputItem from './InputItem'
import OutputItem from './OutputItem'
import HTLCOutputItem from './HTLCOutputItem'
import Divider from './Divider'
import InputOptionsItem from './InputOptionsItem'

export default class SSSSInputs extends Component {
  constructor(props) {
    super(props)
    this.state = {
			refund_addr: '1NiNja1bUmhSoTXozBRBEtR8LeF9TGbZBN',
			lightning_invoice: 'lntb1500n1p0trcq7pp5h78cqzkdasysywc88y70zk54hr6sr5fphh9uhz6fsg0n26rlwrzsdqh2fjkzep6yppxzapqwdhh2uqcqzpgxqr23ssp5ccp9g66p03jny6vk3qzzthwqd0d4wqlwfsp50g8c8ykfqhm7e50s9qy9qsqep9r0ffppp5075puvr32609zznduh70mfewwkp4c5qd53j7vge0r5gjw8ewd57pdf4mqwdlleafp4v4f7k9mwdzvcwmtz473p9nvvpqpeqjqrc',
      disableP2SH: true
    }

    this.handleRefundAddrChange = this.handleRefundAddrChange.bind(this)
    this.handleLnInvoiceChange = this.handleLnInvoiceChange.bind(this)
    this.handleLockTimeSelect = this.handleLockTimeSelect.bind(this)
    this.handleTypeSelect = this.handleTypeSelect.bind(this)
    this.checkForm = this.checkForm.bind(this)
    this.submitInvoice = this.submitInvoice.bind(this)
  }

  componentDidMount() {}

  handleRefundAddrChange(event) {
    this.setState({refund_addr: event.target.value}, this.checkForm)
  }

	handleLnInvoiceChange(event) {
    this.setState({lightning_invoice: event.target.value}, this.checkForm)
  }

  handleTypeSelect(event) {
    this.setState({htlc_type: event}, this.checkForm)
  }

  handleLockTimeSelect(event) {
    this.setState({locktime_value: event}, this.checkForm)
  }

  checkForm() {
    console.log(this.state)
    if (!this.state.lightning_invoice) {
      return
    }
    if (!this.state.refund_addr) {
      return
    }
    if (!this.state.htlc_type) {
      return
    }
    if (!this.state.locktime_value) {
      return
    }

    this.submitInvoice()
  }

	submitInvoice() {
		const requestOptions = {
			method: 'POST',
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(
				{
					"refund_address": this.state.refund_addr,
          "bolt11_invoice": this.state.lightning_invoice,
          "lockduration": this.state.locktime_value,
          "htlc_type": this.state.htlc_type
				}
			),
		}
		fetch("http://127.0.0.1:8000/api/btclnswap/", requestOptions)
			.then(response => response.text())
      .then(response => JSON.parse(response))
			.then(result => { 
          this.setState({htlc_p2sh: result.htlc_p2sh, disableP2SH: false})
        }
      )
			.catch(error => console.log('error', error));
  }

  render() {
    return (
      <div>
        <InputItem
          rows={2}
          inputName='refund address'
          value={this.state.refund_addr}
          onChange={this.handleRefundAddrChange}
          modalTitle={'Refund address'}
          helpModalText={
          `
The refund address is the bitcoin address the funds go
update all this 
          `}
        />
        <InputItem
          inputName='lightning address'
          value={this.state.lightning_invoice}
          onChange={this.handleLnInvoiceChange}
        />
        <HTLCOutputItem
          inputName='HTLC P2SH'
          value={this.state.htlc_p2sh}
          disable={this.state.enableP2SH}
          onChange={this.handleLnInvoiceChange}
        />
    </div>
    );
  }
}