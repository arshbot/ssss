import React, { Component } from "react";
import { Modal, Input, Button, Tooltip } from 'antd';
import { InfoCircleOutlined, QrcodeOutlined } from '@ant-design/icons';
import 'antd/dist/antd.css';


export default class HTLCOutputItem extends Component {
  constructor(props) {
    super(props)
    this.state = {
      visible: false
    }
  }

  showModal = () => {
    this.setState({
      visible: true,
    })
  }

  handleExit = e => {
    console.log(e);
    this.setState({
      visible: false,
    })
  }

  render() {
    return (
      <div style={style}>
        <label style={textBoxLabel}>{this.props.inputName}</label>
        <div style={tooltip} onClick={this.showModal}>
          <InfoCircleOutlined style={{ color: 'rgba(0,0,0,.45)' }}/>
        </div>
        <Modal
          title={this.props.modalTitle}
          visible={this.state.visible}
          onCancel={this.handleExit}
          footer={[
            <Button key="back" onClick={this.handleExit} type="primary">
              OK
            </Button>,
          ]}
        >
          <pre>{this.props.helpModalText}</pre>
        </Modal>
        <Input
          value={this.props.value}
          disabled={this.props.disable}
          style={textBox}
          prefix={
            <Tooltip title="Extra information">
              <div>
                <QrcodeOutlined style={{ color: 'rgba(0,0,0,.45)' }} />
              </div>
            </Tooltip>
          }/>

      </div>
    );
  }
}

HTLCOutputItem.defaultProps = {
  disable: false,
}

const style = {
  marginTop: '30px',
  display: 'flex',
  justifyContent: 'flex-end',
}

const tooltip = {
  marginRight: '20px',
}

const textBoxLabel = {
  marginRight: '5px',
  marginLeft: '15%'
}

const textBox = {
  width: '60%',
  float: 'right',
  marginRight: '15%',
}