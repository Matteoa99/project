from clover import srv
from std_srvs.srv import Trigger
import rospy
import math

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)

def navigate_wait(x=0, y=0, z=0, speed=0.5, frame_id='body', auto_arm=False):
    res = navigate(x=x, y=y, z=z, yaw=float('nan'), speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    if not res.success:
        raise Exception(res.message)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < 0.2:
            return
        rospy.sleep(0.2)

def land_wait():
    land()
    while get_telemetry().armed:
        rospy.sleep(0.2)

def wait_arrival():
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < 0.2:
            return
        rospy.sleep(0.2)

navigate_wait(z=1, frame_id='body', auto_arm=True)
navigate_wait(x=4, y=0, z=1.5, frame_id='aruco_map', speed=1.5)
wait_arrival()
navigate_wait(x=0, y=2, z=0, frame_id='navigate_target', speed=1.5)
wait_arrival()
navigate_wait(x=-4, y=0, z=0, frame_id='navigate_target', speed=1.5)
wait_arrival()
navigate_wait(x=0, y=-2, z=0, frame_id='navigate_target', speed=1.5)
land_wait()