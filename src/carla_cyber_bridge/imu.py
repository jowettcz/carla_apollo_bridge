#!usr/bin/env python
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
"""
Classes to handle Carla imu sensor
"""

from transforms3d.euler import euler2quat

import carla_common.transforms as trans
from carla_common import constants

from .sensor import Sensor

from modules.drivers.gnss.proto.imu_pb2 import Imu
from modules.localization.proto.imu_pb2 import CorrectedImu


class ImuSensor(Sensor):

    """
    Actor implementation details for imu sensor
    """

    def __init__(self, uid, name, parent, relative_spawn_pose, node, carla_actor, synchronous_mode):
        """
        Constructor

        :param uid: unique identifier for this object
        :type uid: int
        :param name: name identiying this object
        :type name: string
        :param parent: the parent of this
        :type parent: carla_cyber_bridge.Parent
        :param relative_spawn_pose: the relative spawn pose of this
        :type relative_spawn_pose: geometry_msgs.Pose
        :param node: node-handle
        :type node: CompatibleNode
        :param carla_actor : carla actor object
        :type carla_actor: carla.Actor
        :param synchronous_mode: use in synchronous mode?
        :type synchronous_mode: bool
        """
        super(ImuSensor, self).__init__(uid=uid,
                                        name=name,
                                        parent=parent,
                                        relative_spawn_pose=relative_spawn_pose,
                                        node=node,
                                        carla_actor=carla_actor,
                                        synchronous_mode=synchronous_mode)

        # self.imu_writer = node.new_writer(self.get_topic_prefix(), Imu, qos_depth=10)
        self.imu_writer = node.new_writer(constants.CHANNEL_SENSOR +  'gnss/corrected_imu', CorrectedImu, qos_depth=20)
        self.listen()

    def destroy(self):
        super(ImuSensor, self).destroy()

    def get_topic_prefix(self):
        """
        get the topic name of the current entity.

        :return: the final topic name of this object
        :rtype: string
        """
        return constants.CHANNEL_SENSOR + self.name

    # pylint: disable=arguments-differ
    def sensor_data_updated(self, carla_imu_measurement):
        """
        Function to transform a received imu measurement into a ROS Imu message

        :param carla_imu_measurement: carla imu measurement object
        :type carla_imu_measurement: carla.IMUMeasurement
        """
        imu_msg = CorrectedImu()
        imu_msg.header.CopyFrom(self.get_msg_header(timestamp=carla_imu_measurement.timestamp))

        # Carla uses a left-handed coordinate convention (X forward, Y right, Z up).
        # Here, these measurements are converted to the right-handed ROS convention
        #  (X forward, Y left, Z up).
        imu_msg.imu.angular_velocity.x = -carla_imu_measurement.gyroscope.x
        imu_msg.imu.angular_velocity.y = carla_imu_measurement.gyroscope.y
        imu_msg.imu.angular_velocity.z = -carla_imu_measurement.gyroscope.z

        imu_msg.imu.linear_acceleration.x = carla_imu_measurement.accelerometer.x
        imu_msg.imu.linear_acceleration.y = -carla_imu_measurement.accelerometer.y
        imu_msg.imu.linear_acceleration.z = carla_imu_measurement.accelerometer.z

        imu_msg.imu.euler_angles.x = carla_imu_measurement.transform.rotation.roll / 180 * 3.14
        imu_msg.imu.euler_angles.y = carla_imu_measurement.transform.rotation.pitch / 180 * 3.14
        imu_msg.imu.euler_angles.z = carla_imu_measurement.transform.rotation.yaw / 180 * 3.14

        self.imu_writer.write(imu_msg)
