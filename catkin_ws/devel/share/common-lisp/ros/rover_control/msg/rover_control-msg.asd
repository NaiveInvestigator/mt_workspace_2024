
(cl:in-package :asdf)

(defsystem "rover_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ArucoGate" :depends-on ("_package_ArucoGate"))
    (:file "_package_ArucoGate" :depends-on ("_package"))
    (:file "ArucoInfo" :depends-on ("_package_ArucoInfo"))
    (:file "_package_ArucoInfo" :depends-on ("_package"))
    (:file "ArucoPost" :depends-on ("_package_ArucoPost"))
    (:file "_package_ArucoPost" :depends-on ("_package"))
    (:file "ControlStatus" :depends-on ("_package_ControlStatus"))
    (:file "_package_ControlStatus" :depends-on ("_package"))
  ))