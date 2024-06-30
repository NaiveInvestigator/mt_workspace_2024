import sys
import numpy as np
import cv2
import pyzed.sl as sl
import argparse
import ogl_viewer.viewer as gl
import cv_viewer.tracking_viewer as cv_viewer
import platform
from collections import deque

is_jetson = platform.uname().machine.startswith('aarch64')


def parse_args(init):
    if len(opt.input_svo_file) > 0 and opt.input_svo_file.endswith(".svo"):
        init.set_from_svo_file(opt.input_svo_file)
        print("[Sample] Using SVO File input: {0}".format(opt.input_svo_file))
    elif len(opt.ip_address) > 0:
        ip_str = opt.ip_address
        if ip_str.replace(':', '').replace('.', '').isdigit() and len(ip_str.split('.')) == 4 and len(ip_str.split(':')) == 2:
            init.set_from_stream(ip_str.split(':')[0], int(ip_str.split(':')[1]))
            print("[Sample] Using Stream input, IP : ", ip_str)
        elif ip_str.replace(':', '').replace('.', '').isdigit() and len(ip_str.split('.')) == 4:
            init.set_from_stream(ip_str)
            print("[Sample] Using Stream input, IP : ", ip_str)
        else:
            print("Invalid IP format. Using live stream")
    if "resolution" in opt.resolution:
        init.camera_resolution = sl.RESOLUTION.HD2K
        print("[Sample] Using Camera in resolution HD2K")
    elif "HD1200" in opt.resolution:
        init.camera_resolution = sl.RESOLUTION.HD1200
        print("[Sample] Using Camera in resolution HD1200")
    elif "HD1080" in opt.resolution:
        init.camera_resolution = sl.RESOLUTION.HD1080


def main():
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.coordinate_units = sl.UNIT.METER
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP  
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.depth_maximum_distance = 10.0
    parse_args(init_params)
    
    is_playback = len(opt.input_svo_file) > 0
    
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : " + repr(status) + ". Exit program.")
        exit()
    
    positional_tracking_parameters = sl.PositionalTrackingParameters()
    zed.enable_positional_tracking(positional_tracking_parameters)

    batch_parameters = sl.BatchParameters()
    batch_parameters.enable = opt.enable_batching_reid
    batch_parameters.latency = 3.0 if opt.enable_batching_reid else 0.0
    obj_param = sl.ObjectDetectionParameters(batch_trajectories_parameters = batch_parameters)
    obj_param.detection_model = sl.OBJECT_DETECTION_MODEL.MULTI_CLASS_BOX_FAST if is_jetson else sl.OBJECT_DETECTION_MODEL.MULTI_CLASS_BOX_ACCURATE
    obj_param.enable_tracking = True
    
    returned_state = zed.enable_object_detection(obj_param)
    camera_configuration = zed.get_camera_information().camera_configuration

    if returned_state != sl.ERROR_CODE.SUCCESS:
        print("enable_object_detection", returned_state, "\nExit program.")
        zed.close()
        exit()

    detection_confidence = 60
    detection_parameters_rt = sl.ObjectDetectionRuntimeParameters(detection_confidence)
    detection_parameters_rt.object_class_filter = [sl.OBJECT_CLASS.VEHICLE, sl.OBJECT_CLASS.PERSON]
    detection_parameters_rt.object_class_detection_confidence_threshold[sl.OBJECT_CLASS.PERSON] = detection_confidence
    detection_parameters_rt.object_class_detection_confidence_threshold[sl.OBJECT_CLASS.VEHICLE] = detection_confidence

    quit_bool = False

    if not opt.disable_gui:
        image_aspect_ratio = camera_configuration.resolution.width / camera_configuration.resolution.height
        requested_low_res_w = min(1280, camera_configuration.resolution.width)
        display_resolution = sl.Resolution(requested_low_res_w, requested_low_res_w / image_aspect_ratio)
        image_scale = [display_resolution.width / camera_configuration.resolution.width, display_resolution.height / camera_configuration.resolution.height]
        image_left_ocv = np.full((display_resolution.height, display_resolution.width, 4), [245, 239, 239, 255], np.uint8)

        camera_config = zed.get_camera_information().camera_configuration
        tracks_resolution = sl.Resolution(400, display_resolution.height)
        track_view_generator = cv_viewer.TrackingViewer(tracks_resolution, camera_config.fps, init_params.depth_maximum_distance * 1000, batch_parameters.latency)
        track_view_generator.set_camera_calibration(camera_config.calibration_parameters)
        image_track_ocv = np.zeros((tracks_resolution.height, tracks_resolution.width, 4), np.uint8)

        global_image = np.full((display_resolution.height, display_resolution.width + tracks_resolution.width, 4), [245, 239, 239, 255], np.uint8)
        viewer = gl.GLViewer()
        pc_resolution = sl.Resolution(requested_low_res_w, requested_low_res_w / image_aspect_ratio)
        viewer.init(zed.get_camera_information().camera_model, pc_resolution, obj_param.enable_tracking)
        point_cloud = sl.Mat(pc_resolution.width, pc_resolution.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)
        objects = sl.Objects()
        image_left = sl.Mat()
        cam_w_pose = sl.Pose()
        image_scale = (display_resolution.width / camera_config.resolution.width, display_resolution.height / camera_config.resolution.height)

    id_counter = {}
    objects = sl.Objects()
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.confidence_threshold = 50
    window_name = "ZED| 3D View tracking"
    gl_viewer_available = True
    printHelp()

    while True:
        if not opt.disable_gui and (zed.grab(runtime_parameters) != sl.ERROR_CODE.SUCCESS or quit_bool):
            break 
        if opt.disable_gui and (zed.grab(runtime_parameters) != sl.ERROR_CODE.SUCCESS or quit_bool or not gl_viewer_available):
            break 
        if len(detection_parameters_rt.object_class_filter) == 0:
            detection_parameters_rt.detection_confidence_threshold = detection_confidence
        else:
            for parameter in detection_parameters_rt.object_class_filter:
                detection_parameters_rt.object_class_detection_confidence_threshold[parameter] = detection_confidence
        
        returned_state = zed.retrieve_objects(objects, detection_parameters_rt)
        if returned_state == sl.ERROR_CODE.SUCCESS:
            if opt.enable_batching_reid:
                for obj in objects.object_list:
                    id_counter[str(obj.id)] = 1

                objects_batch = []
                if zed.get_objects_batch(objects_batch) == sl.ERROR_CODE.SUCCESS:
                    if len(objects_batch) > 0:
                        print("During last batch processing: ", len(id_counter), " Objects were detected: ", end=" ")
                        for it in id_counter:
                            print(it, end=" ")
                        print("\nWhile", len(objects_batch), "different only after reID:", end=" ")
                        for it in objects_batch:
                            print(it.id, end=" ")
                        print()
                        id_counter.clear()
            
            if not opt.disable_gui:
                zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, pc_resolution)
                zed.get_position(cam_w_pose, sl.REFERENCE_FRAME.WORLD)
                zed.retrieve_image(image_left, sl.VIEW.LEFT, sl.MEM.CPU, display_resolution)
                image_render_left = image_left.get_data()
                np.copyto(image_left_ocv, image_render_left)
                track_view_generator.generate_view(objects, image_left_ocv, image_scale, cam_w_pose, image_track_ocv, objects.is_tracked)
                global_image = cv2.hconcat([image_left_ocv, image_track_ocv])
                viewer.updateData(point_cloud, objects)
                gl_viewer_available = viewer.is_available()
                cv2.imshow(window_name, global_image)
                key = cv2.waitKey(10)
                if key == 113: # 'q' key
                    quit_bool = True
                elif key == 105: # 'i' key
                    track_view_generator.zoomIn()
                elif key == 111: # 'o' key
                    track_view_generator.zoomOut()
                elif key == 112: # 'p' key
                    detection_parameters_rt.object_class_filter = [sl.OBJECT_CLASS.PERSON]
                    detection_parameters_rt.object_class_detection_confidence_threshold[sl.OBJECT_CLASS.PERSON] = detection_confidence
                    print("Person only")
                elif key == 118: # 'v' key
                    detection_parameters_rt.object_class_filter = [sl.OBJECT_CLASS.VEHICLE]
                    detection_parameters_rt.object_class_filter.append(sl.OBJECT_CLASS.VEHICLE)
                    detection_parameters_rt.object_class_detection_confidence_threshold[sl.OBJECT_CLASS.VEHICLE] = detection_confidence
                    print("Vehicle only")
                elif key == 99: # 'c' key
                    detection_parameters_rt.object_class_filter = []
                    detection_parameters_rt.object_class_detection_confidence_threshold.clear()
                    print("Clear Filters")
        
        if is_playback and zed.get_svo_position() == zed.get_svo_number_of_frames() - 1:
            quit_bool = True

    if not opt.disable_gui:
        viewer.exit()
        point_cloud.free()
        image_left.free()
    
    zed.disable_object_detection()
    zed.close()


if __name__=="__main__":
    main()