import React, { Component } from "react";
import { Modal, Input, Select, Button } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import 'antd/dist/antd.css';
const { TextArea } = Input;


export default class InputOptionsItem extends Component {
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
        <Input.Group compact style={textBox}>
          <Select defaultValue="Select One" style={{width:'100%'}} onChange={this.props.onChange}>
            {this.props.options.map(name => {
              return <Select.Option key={name} value={name}>{name}</Select.Option>
            })}
          </Select>
        </Input.Group>
      </div>
    );
  }
}

InputOptionsItem.defaultProps = {
  rows: 4,
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