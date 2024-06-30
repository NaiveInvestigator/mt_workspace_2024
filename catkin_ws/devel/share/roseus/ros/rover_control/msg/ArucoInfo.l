;; Auto-generated. Do not edit!


(when (boundp 'rover_control::ArucoInfo)
  (if (not (find-package "ROVER_CONTROL"))
    (make-package "ROVER_CONTROL"))
  (shadow 'ArucoInfo (find-package "ROVER_CONTROL")))
(unless (find-package "ROVER_CONTROL::ARUCOINFO")
  (make-package "ROVER_CONTROL::ARUCOINFO"))

(in-package "ROS")
;;//! \htmlinclude ArucoInfo.msg.html


(defclass rover_control::ArucoInfo
  :super ros::object
  :slots (_detected _distance _x _y _id ))

(defmethod rover_control::ArucoInfo
  (:init
   (&key
    ((:detected __detected) nil)
    ((:distance __distance) 0.0)
    ((:x __x) 0)
    ((:y __y) 0)
    ((:id __id) 0)
    )
   (send-super :init)
   (setq _detected __detected)
   (setq _distance (float __distance))
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _id (round __id))
   self)
  (:detected
   (&optional (__detected :null))
   (if (not (eq __detected :null)) (setq _detected __detected)) _detected)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:serialization-length
   ()
   (+
    ;; bool _detected
    1
    ;; float64 _distance
    8
    ;; int32 _x
    4
    ;; int32 _y
    4
    ;; int32 _id
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _detected
       (if _detected (write-byte -1 s) (write-byte 0 s))
     ;; float64 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int32 _x
       (write-long _x s)
     ;; int32 _y
       (write-long _y s)
     ;; int32 _id
       (write-long _id s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _detected
     (setq _detected (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float64 _distance
     (setq _distance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int32 _x
     (setq _x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _y
     (setq _y (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _id
     (setq _id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get rover_control::ArucoInfo :md5sum-) "2fc9308a0b3197eeb33075d3be520061")
(setf (get rover_control::ArucoInfo :datatype-) "rover_control/ArucoInfo")
(setf (get rover_control::ArucoInfo :definition-)
      "bool detected
float64 distance
int32 x
int32 y
int32 id
")



(provide :rover_control/ArucoInfo "2fc9308a0b3197eeb33075d3be520061")


