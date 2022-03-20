#!/usr/bin/env python3
# Tiger3018, Mar 20th, MIT License
import rospy
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped, Pose, Vector3
from gazebo_msgs.msg import LinkState

pub : rospy.Publisher = None
pub_beat : rospy.Publisher = None

def bridge_callback(data : TFMessage) -> None:
    global pub 
    global pub_beat
    data.transforms.reverse()
    # father_frame_name = "qqq::zhou_Link"
    for i in data.transforms[ 1 : ]: # jizuo_Link, base_link, jizuo_Link error
        iTf : TransformStamped = i
        if iTf.header.frame_id == "jizuo_Link":
            iTf.header.frame_id = "base_link"
        elif iTf.header.frame_id == "base_footprint":
            continue
        # if father_frame_name == "qqq:" + iTf.child_frame_id:
            # rospy.WARN("same?")
        pub.publish(LinkState(
            link_name = "qqq::" + iTf.child_frame_id,
            pose = Pose(iTf.transform.translation, iTf.transform.rotation),
            reference_frame = "qqq::" + iTf.header.frame_id
        ))
        # father_frame_name = "qqq::" + iTf.header.frame_id
    pub.publish(LinkState(
        link_name = "qqq::" + "base_link",
        pose = Pose(position = Vector3(0, 0, 0.6)),
        reference_frame = "ground_plane::" + "link"
    ))
    # pub_beat.publish("live")
    # wait_to_pub = LinkState()
    # pub.publish(data.transforms)

def talker():
    global pub
    global pub_beat
    rospy.init_node('march-bridge-tiger')
    pub = rospy.Publisher('gazebo/set_link_state', LinkState, queue_size=10)
    pub_beat = rospy.Publisher('march-bridge', String, queue_size=10)
    rospy.Subscriber("tf", TFMessage, bridge_callback)
    rate = rospy.Rate(1000) # 10hz
    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass