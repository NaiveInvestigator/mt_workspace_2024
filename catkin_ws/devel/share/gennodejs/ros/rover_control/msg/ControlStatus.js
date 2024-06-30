// Auto-generated. Do not edit!

// (in-package rover_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class ControlStatus {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.left_speed = null;
      this.right_speed = null;
      this.act1_speed = null;
      this.act2_speed = null;
      this.act3_speed = null;
      this.claw_spin_speed = null;
      this.base_speed = null;
      this.claw_grip_speed = null;
    }
    else {
      if (initObj.hasOwnProperty('left_speed')) {
        this.left_speed = initObj.left_speed
      }
      else {
        this.left_speed = 0;
      }
      if (initObj.hasOwnProperty('right_speed')) {
        this.right_speed = initObj.right_speed
      }
      else {
        this.right_speed = 0;
      }
      if (initObj.hasOwnProperty('act1_speed')) {
        this.act1_speed = initObj.act1_speed
      }
      else {
        this.act1_speed = 0;
      }
      if (initObj.hasOwnProperty('act2_speed')) {
        this.act2_speed = initObj.act2_speed
      }
      else {
        this.act2_speed = 0;
      }
      if (initObj.hasOwnProperty('act3_speed')) {
        this.act3_speed = initObj.act3_speed
      }
      else {
        this.act3_speed = 0;
      }
      if (initObj.hasOwnProperty('claw_spin_speed')) {
        this.claw_spin_speed = initObj.claw_spin_speed
      }
      else {
        this.claw_spin_speed = 0;
      }
      if (initObj.hasOwnProperty('base_speed')) {
        this.base_speed = initObj.base_speed
      }
      else {
        this.base_speed = 0;
      }
      if (initObj.hasOwnProperty('claw_grip_speed')) {
        this.claw_grip_speed = initObj.claw_grip_speed
      }
      else {
        this.claw_grip_speed = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ControlStatus
    // Serialize message field [left_speed]
    bufferOffset = _serializer.int16(obj.left_speed, buffer, bufferOffset);
    // Serialize message field [right_speed]
    bufferOffset = _serializer.int16(obj.right_speed, buffer, bufferOffset);
    // Serialize message field [act1_speed]
    bufferOffset = _serializer.int16(obj.act1_speed, buffer, bufferOffset);
    // Serialize message field [act2_speed]
    bufferOffset = _serializer.int16(obj.act2_speed, buffer, bufferOffset);
    // Serialize message field [act3_speed]
    bufferOffset = _serializer.int16(obj.act3_speed, buffer, bufferOffset);
    // Serialize message field [claw_spin_speed]
    bufferOffset = _serializer.int16(obj.claw_spin_speed, buffer, bufferOffset);
    // Serialize message field [base_speed]
    bufferOffset = _serializer.int16(obj.base_speed, buffer, bufferOffset);
    // Serialize message field [claw_grip_speed]
    bufferOffset = _serializer.int16(obj.claw_grip_speed, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ControlStatus
    let len;
    let data = new ControlStatus(null);
    // Deserialize message field [left_speed]
    data.left_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [right_speed]
    data.right_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [act1_speed]
    data.act1_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [act2_speed]
    data.act2_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [act3_speed]
    data.act3_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [claw_spin_speed]
    data.claw_spin_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [base_speed]
    data.base_speed = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [claw_grip_speed]
    data.claw_grip_speed = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'rover_control/ControlStatus';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '69100b553df4a1337bbe8ccb7c455a89';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int16 left_speed
    int16 right_speed
    int16 act1_speed
    int16 act2_speed
    int16 act3_speed
    int16 claw_spin_speed
    int16 base_speed
    int16 claw_grip_speed
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ControlStatus(null);
    if (msg.left_speed !== undefined) {
      resolved.left_speed = msg.left_speed;
    }
    else {
      resolved.left_speed = 0
    }

    if (msg.right_speed !== undefined) {
      resolved.right_speed = msg.right_speed;
    }
    else {
      resolved.right_speed = 0
    }

    if (msg.act1_speed !== undefined) {
      resolved.act1_speed = msg.act1_speed;
    }
    else {
      resolved.act1_speed = 0
    }

    if (msg.act2_speed !== undefined) {
      resolved.act2_speed = msg.act2_speed;
    }
    else {
      resolved.act2_speed = 0
    }

    if (msg.act3_speed !== undefined) {
      resolved.act3_speed = msg.act3_speed;
    }
    else {
      resolved.act3_speed = 0
    }

    if (msg.claw_spin_speed !== undefined) {
      resolved.claw_spin_speed = msg.claw_spin_speed;
    }
    else {
      resolved.claw_spin_speed = 0
    }

    if (msg.base_speed !== undefined) {
      resolved.base_speed = msg.base_speed;
    }
    else {
      resolved.base_speed = 0
    }

    if (msg.claw_grip_speed !== undefined) {
      resolved.claw_grip_speed = msg.claw_grip_speed;
    }
    else {
      resolved.claw_grip_speed = 0
    }

    return resolved;
    }
};

module.exports = ControlStatus;
