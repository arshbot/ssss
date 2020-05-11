import React, { Component } from "react";
import { Modal, Input, Button } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import 'antd/dist/antd.css';
const { TextArea } = Input;


export default class InputItem extends Component {
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
          {/* <Tooltip title="Extra information"> */}
              <InfoCircleOutlined
              style={{ color: 'rgba(0,0,0,.45)' }}
              />
          {/* </Tooltip> */}
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
        <TextArea
          rows={this.props.rows}
          value={this.props.value}
          onChange={this.props.onChange}
          disabled={this.props.disable}
          style={textBox}/>
      </div>
    );
  }
}

InputItem.defaultProps = {
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