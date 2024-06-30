; Auto-generated. Do not edit!


(cl:in-package rover_control-msg)


;//! \htmlinclude ControlStatus.msg.html

(cl:defclass <ControlStatus> (roslisp-msg-protocol:ros-message)
  ((left_speed
    :reader left_speed
    :initarg :left_speed
    :type cl:fixnum
    :initform 0)
   (right_speed
    :reader right_speed
    :initarg :right_speed
    :type cl:fixnum
    :initform 0)
   (act1_speed
    :reader act1_speed
    :initarg :act1_speed
    :type cl:fixnum
    :initform 0)
   (act2_speed
    :reader act2_speed
    :initarg :act2_speed
    :type cl:fixnum
    :initform 0)
   (act3_speed
    :reader act3_speed
    :initarg :act3_speed
    :type cl:fixnum
    :initform 0)
   (claw_spin_speed
    :reader claw_spin_speed
    :initarg :claw_spin_speed
    :type cl:fixnum
    :initform 0)
   (base_speed
    :reader base_speed
    :initarg :base_speed
    :type cl:fixnum
    :initform 0)
   (claw_grip_speed
    :reader claw_grip_speed
    :initarg :claw_grip_speed
    :type cl:fixnum
    :initform 0))
)

(cl:defclass ControlStatus (<ControlStatus>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ControlStatus>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ControlStatus)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rover_control-msg:<ControlStatus> is deprecated: use rover_control-msg:ControlStatus instead.")))

(cl:ensure-generic-function 'left_speed-val :lambda-list '(m))
(cl:defmethod left_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:left_speed-val is deprecated.  Use rover_control-msg:left_speed instead.")
  (left_speed m))

(cl:ensure-generic-function 'right_speed-val :lambda-list '(m))
(cl:defmethod right_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:right_speed-val is deprecated.  Use rover_control-msg:right_speed instead.")
  (right_speed m))

(cl:ensure-generic-function 'act1_speed-val :lambda-list '(m))
(cl:defmethod act1_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:act1_speed-val is deprecated.  Use rover_control-msg:act1_speed instead.")
  (act1_speed m))

(cl:ensure-generic-function 'act2_speed-val :lambda-list '(m))
(cl:defmethod act2_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:act2_speed-val is deprecated.  Use rover_control-msg:act2_speed instead.")
  (act2_speed m))

(cl:ensure-generic-function 'act3_speed-val :lambda-list '(m))
(cl:defmethod act3_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:act3_speed-val is deprecated.  Use rover_control-msg:act3_speed instead.")
  (act3_speed m))

(cl:ensure-generic-function 'claw_spin_speed-val :lambda-list '(m))
(cl:defmethod claw_spin_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:claw_spin_speed-val is deprecated.  Use rover_control-msg:claw_spin_speed instead.")
  (claw_spin_speed m))

(cl:ensure-generic-function 'base_speed-val :lambda-list '(m))
(cl:defmethod base_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:base_speed-val is deprecated.  Use rover_control-msg:base_speed instead.")
  (base_speed m))

(cl:ensure-generic-function 'claw_grip_speed-val :lambda-list '(m))
(cl:defmethod claw_grip_speed-val ((m <ControlStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rover_control-msg:claw_grip_speed-val is deprecated.  Use rover_control-msg:claw_grip_speed instead.")
  (claw_grip_speed m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ControlStatus>) ostream)
  "Serializes a message object of type '<ControlStatus>"
  (cl:let* ((signed (cl:slot-value msg 'left_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'right_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'act1_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'act2_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'act3_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'claw_spin_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'base_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'claw_grip_speed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ControlStatus>) istream)
  "Deserializes a message object of type '<ControlStatus>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'left_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'right_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'act1_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'act2_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'act3_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'claw_spin_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'base_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'claw_grip_speed) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ControlStatus>)))
  "Returns string type for a message object of type '<ControlStatus>"
  "rover_control/ControlStatus")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ControlStatus)))
  "Returns string type for a message object of type 'ControlStatus"
  "rover_control/ControlStatus")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ControlStatus>)))
  "Returns md5sum for a message object of type '<ControlStatus>"
  "69100b553df4a1337bbe8ccb7c455a89")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ControlStatus)))
  "Returns md5sum for a message object of type 'ControlStatus"
  "69100b553df4a1337bbe8ccb7c455a89")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ControlStatus>)))
  "Returns full string definition for message of type '<ControlStatus>"
  (cl:format cl:nil "int16 left_speed~%int16 right_speed~%int16 act1_speed~%int16 act2_speed~%int16 act3_speed~%int16 claw_spin_speed~%int16 base_speed~%int16 claw_grip_speed~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ControlStatus)))
  "Returns full string definition for message of type 'ControlStatus"
  (cl:format cl:nil "int16 left_speed~%int16 right_speed~%int16 act1_speed~%int16 act2_speed~%int16 act3_speed~%int16 claw_spin_speed~%int16 base_speed~%int16 claw_grip_speed~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ControlStatus>))
  (cl:+ 0
     2
     2
     2
     2
     2
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ControlStatus>))
  "Converts a ROS message object to a list"
  (cl:list 'ControlStatus
    (cl:cons ':left_speed (left_speed msg))
    (cl:cons ':right_speed (right_speed msg))
    (cl:cons ':act1_speed (act1_speed msg))
    (cl:cons ':act2_speed (act2_speed msg))
    (cl:cons ':act3_speed (act3_speed msg))
    (cl:cons ':claw_spin_speed (claw_spin_speed msg))
    (cl:cons ':base_speed (base_speed msg))
    (cl:cons ':claw_grip_speed (claw_grip_speed msg))
))
