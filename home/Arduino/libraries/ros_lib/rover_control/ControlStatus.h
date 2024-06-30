#ifndef _ROS_rover_control_ControlStatus_h
#define _ROS_rover_control_ControlStatus_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace rover_control
{

  class ControlStatus : public ros::Msg
  {
    public:
      typedef int16_t _left_speed_type;
      _left_speed_type left_speed;
      typedef int16_t _right_speed_type;
      _right_speed_type right_speed;
      typedef int16_t _act1_speed_type;
      _act1_speed_type act1_speed;
      typedef int16_t _act2_speed_type;
      _act2_speed_type act2_speed;
      typedef int16_t _act3_speed_type;
      _act3_speed_type act3_speed;
      typedef int16_t _claw_spin_speed_type;
      _claw_spin_speed_type claw_spin_speed;
      typedef int16_t _base_speed_type;
      _base_speed_type base_speed;
      typedef int16_t _claw_grip_speed_type;
      _claw_grip_speed_type claw_grip_speed;

    ControlStatus():
      left_speed(0),
      right_speed(0),
      act1_speed(0),
      act2_speed(0),
      act3_speed(0),
      claw_spin_speed(0),
      base_speed(0),
      claw_grip_speed(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      union {
        int16_t real;
        uint16_t base;
      } u_left_speed;
      u_left_speed.real = this->left_speed;
      *(outbuffer + offset + 0) = (u_left_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_left_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->left_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_right_speed;
      u_right_speed.real = this->right_speed;
      *(outbuffer + offset + 0) = (u_right_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_right_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->right_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_act1_speed;
      u_act1_speed.real = this->act1_speed;
      *(outbuffer + offset + 0) = (u_act1_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_act1_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->act1_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_act2_speed;
      u_act2_speed.real = this->act2_speed;
      *(outbuffer + offset + 0) = (u_act2_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_act2_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->act2_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_act3_speed;
      u_act3_speed.real = this->act3_speed;
      *(outbuffer + offset + 0) = (u_act3_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_act3_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->act3_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_claw_spin_speed;
      u_claw_spin_speed.real = this->claw_spin_speed;
      *(outbuffer + offset + 0) = (u_claw_spin_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_claw_spin_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->claw_spin_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_base_speed;
      u_base_speed.real = this->base_speed;
      *(outbuffer + offset + 0) = (u_base_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_base_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->base_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_claw_grip_speed;
      u_claw_grip_speed.real = this->claw_grip_speed;
      *(outbuffer + offset + 0) = (u_claw_grip_speed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_claw_grip_speed.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->claw_grip_speed);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      union {
        int16_t real;
        uint16_t base;
      } u_left_speed;
      u_left_speed.base = 0;
      u_left_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_left_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->left_speed = u_left_speed.real;
      offset += sizeof(this->left_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_right_speed;
      u_right_speed.base = 0;
      u_right_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_right_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->right_speed = u_right_speed.real;
      offset += sizeof(this->right_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_act1_speed;
      u_act1_speed.base = 0;
      u_act1_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_act1_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->act1_speed = u_act1_speed.real;
      offset += sizeof(this->act1_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_act2_speed;
      u_act2_speed.base = 0;
      u_act2_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_act2_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->act2_speed = u_act2_speed.real;
      offset += sizeof(this->act2_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_act3_speed;
      u_act3_speed.base = 0;
      u_act3_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_act3_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->act3_speed = u_act3_speed.real;
      offset += sizeof(this->act3_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_claw_spin_speed;
      u_claw_spin_speed.base = 0;
      u_claw_spin_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_claw_spin_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->claw_spin_speed = u_claw_spin_speed.real;
      offset += sizeof(this->claw_spin_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_base_speed;
      u_base_speed.base = 0;
      u_base_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_base_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->base_speed = u_base_speed.real;
      offset += sizeof(this->base_speed);
      union {
        int16_t real;
        uint16_t base;
      } u_claw_grip_speed;
      u_claw_grip_speed.base = 0;
      u_claw_grip_speed.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_claw_grip_speed.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->claw_grip_speed = u_claw_grip_speed.real;
      offset += sizeof(this->claw_grip_speed);
     return offset;
    }

    virtual const char * getType() override { return "rover_control/ControlStatus"; };
    virtual const char * getMD5() override { return "69100b553df4a1337bbe8ccb7c455a89"; };

  };

}
#endif
