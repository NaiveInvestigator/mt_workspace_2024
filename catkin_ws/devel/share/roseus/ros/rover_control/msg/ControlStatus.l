;; Auto-generated. Do not edit!


(when (boundp 'rover_control::ControlStatus)
  (if (not (find-package "ROVER_CONTROL"))
    (make-package "ROVER_CONTROL"))
  (shadow 'ControlStatus (find-package "ROVER_CONTROL")))
(unless (find-package "ROVER_CONTROL::CONTROLSTATUS")
  (make-package "ROVER_CONTROL::CONTROLSTATUS"))

(in-package "ROS")
;;//! \htmlinclude ControlStatus.msg.html


(defclass rover_control::ControlStatus
  :super ros::object
  :slots (_left_speed _right_speed _act1_speed _act2_speed _act3_speed _claw_spin_speed _base_speed _claw_grip_speed ))

(defmethod rover_control::ControlStatus
  (:init
   (&key
    ((:left_speed __left_speed) 0)
    ((:right_speed __right_speed) 0)
    ((:act1_speed __act1_speed) 0)
    ((:act2_speed __act2_speed) 0)
    ((:act3_speed __act3_speed) 0)
    ((:claw_spin_speed __claw_spin_speed) 0)
    ((:base_speed __base_speed) 0)
    ((:claw_grip_speed __claw_grip_speed) 0)
    )
   (send-super :init)
   (setq _left_speed (round __left_speed))
   (setq _right_speed (round __right_speed))
   (setq _act1_speed (round __act1_speed))
   (setq _act2_speed (round __act2_speed))
   (setq _act3_speed (round __act3_speed))
   (setq _claw_spin_speed (round __claw_spin_speed))
   (setq _base_speed (round __base_speed))
   (setq _claw_grip_speed (round __claw_grip_speed))
   self)
  (:left_speed
   (&optional __left_speed)
   (if __left_speed (setq _left_speed __left_speed)) _left_speed)
  (:right_speed
   (&optional __right_speed)
   (if __right_speed (setq _right_speed __right_speed)) _right_speed)
  (:act1_speed
   (&optional __act1_speed)
   (if __act1_speed (setq _act1_speed __act1_speed)) _act1_speed)
  (:act2_speed
   (&optional __act2_speed)
   (if __act2_speed (setq _act2_speed __act2_speed)) _act2_speed)
  (:act3_speed
   (&optional __act3_speed)
   (if __act3_speed (setq _act3_speed __act3_speed)) _act3_speed)
  (:claw_spin_speed
   (&optional __claw_spin_speed)
   (if __claw_spin_speed (setq _claw_spin_speed __claw_spin_speed)) _claw_spin_speed)
  (:base_speed
   (&optional __base_speed)
   (if __base_speed (setq _base_speed __base_speed)) _base_speed)
  (:claw_grip_speed
   (&optional __claw_grip_speed)
   (if __claw_grip_speed (setq _claw_grip_speed __claw_grip_speed)) _claw_grip_speed)
  (:serialization-length
   ()
   (+
    ;; int16 _left_speed
    2
    ;; int16 _right_speed
    2
    ;; int16 _act1_speed
    2
    ;; int16 _act2_speed
    2
    ;; int16 _act3_speed
    2
    ;; int16 _claw_spin_speed
    2
    ;; int16 _base_speed
    2
    ;; int16 _claw_grip_speed
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _left_speed
       (write-word _left_speed s)
     ;; int16 _right_speed
       (write-word _right_speed s)
     ;; int16 _act1_speed
       (write-word _act1_speed s)
     ;; int16 _act2_speed
       (write-word _act2_speed s)
     ;; int16 _act3_speed
       (write-word _act3_speed s)
     ;; int16 _claw_spin_speed
       (write-word _claw_spin_speed s)
     ;; int16 _base_speed
       (write-word _base_speed s)
     ;; int16 _claw_grip_speed
       (write-word _claw_grip_speed s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _left_speed
     (setq _left_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _right_speed
     (setq _right_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _act1_speed
     (setq _act1_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _act2_speed
     (setq _act2_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _act3_speed
     (setq _act3_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _claw_spin_speed
     (setq _claw_spin_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _base_speed
     (setq _base_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _claw_grip_speed
     (setq _claw_grip_speed (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get rover_control::ControlStatus :md5sum-) "69100b553df4a1337bbe8ccb7c455a89")
(setf (get rover_control::ControlStatus :datatype-) "rover_control/ControlStatus")
(setf (get rover_control::ControlStatus :definition-)
      "int16 left_speed
int16 right_speed
int16 act1_speed
int16 act2_speed
int16 act3_speed
int16 claw_spin_speed
int16 base_speed
int16 claw_grip_speed
")



(provide :rover_control/ControlStatus "69100b553df4a1337bbe8ccb7c455a89")


