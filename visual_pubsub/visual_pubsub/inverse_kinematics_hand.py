import math
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point

class IndexIK:
    def __init__(self):
        self.q = np.array([-0.22, 0.7, 0.03], dtype=float)  # [q11, q12, q13]
        self.l1, self.l2, self.l3 = 2.0, 1.5, 0.8
        self.damping = 0.1
        self.step = 0.05
        self.tol = 1e-2

    def fk(self, q):
        q1, q2, q3 = q
        x = self.l1*np.cos(q1) + self.l2*np.cos(q1+q2) + self.l3*np.cos(q1+q2+q3)
        y = self.l1*np.sin(q1) + self.l2*np.sin(q1+q2) + self.l3*np.sin(q1+q2+q3)
        z = 0.0
        return np.array([x, y, z])

    def J(self, q):
        q1, q2, q3 = q
        j11 = -self.l1*np.sin(q1) - self.l2*np.sin(q1+q2) - self.l3*np.sin(q1+q2+q3)
        j12 = -self.l2*np.sin(q1+q2) - self.l3*np.sin(q1+q2+q3)
        j13 = -self.l3*np.sin(q1+q2+q3)
        j21 =  self.l1*np.cos(q1) + self.l2*np.cos(q1+q2) + self.l3*np.cos(q1+q2+q3)
        j22 =  self.l2*np.cos(q1+q2) + self.l3*np.cos(q1+q2+q3)
        j23 =  self.l3*np.cos(q1+q2+q3)
        return np.array([[j11, j12, j13],
                         [j21, j22, j23],
                         [0.0,  0.0,  0.0]])

    def step_ik(self, target):
        cur = self.fk(self.q)
        e = target - cur
        if np.linalg.norm(e) < self.tol:
            return self.q
        J = self.J(self.q)
        JtJ = J.T @ J
        dq = np.linalg.solve(JtJ + self.damping*np.eye(3), J.T @ e)
        self.q = self.q + self.step * dq
        return self.q


class ThumbIK:
    def __init__(self):
        self.q = np.array([-0.22, 0.7, 0.03], dtype=float)  # [q20, q21, q22]
        self.l1, self.l2, self.l3 = 0.5, 1.3, 0.9
        self.damping = 0.1
        self.step = 0.05
        self.tol = 1e-2

    def fk(self, q):
        q1, q2, q3 = q
        r = self.l2*np.cos(q2) + self.l3*np.cos(q2+q3)
        x = r*np.cos(q1)
        y = r*np.sin(q1)
        z = self.l2*np.sin(q2) + self.l3*np.sin(q2+q3) + self.l1
        return np.array([x, y, z])

    def J(self, q):
        q1, q2, q3 = q
        j11 = -(self.l2*np.cos(q2) + self.l3*np.cos(q2+q3)) * np.sin(q1)
        j12 = -(self.l2*np.sin(q2) + self.l3*np.sin(q2+q3)) * np.cos(q1)
        j13 = - self.l3*np.sin(q2+q3) * np.cos(q1)

        j21 =  (self.l2*np.cos(q2) + self.l3*np.cos(q2+q3)) * np.cos(q1)
        j22 = -(self.l2*np.sin(q2) + self.l3*np.sin(q2+q3)) * np.sin(q1)
        j23 = - self.l3*np.sin(q2+q3) * np.sin(q1)

        j31 = 0.0
        j32 =  self.l2*np.cos(q2) + self.l3*np.cos(q2+q3)
        j33 =  self.l3*np.cos(q2+q3)

        return np.array([[j11, j12, j13],
                         [j21, j22, j23],
                         [j31, j32, j33]])

    def step_ik(self, target):
        cur = self.fk(self.q)
        e = target - cur
        if np.linalg.norm(e) < self.tol:
            return self.q
        J = self.J(self.q)
        JtJ = J.T @ J
        dq = np.linalg.solve(JtJ + self.damping*np.eye(3), J.T @ e)
        self.q = self.q + self.step * dq
        return self.q


class DualInverseKinematics(Node):
    def __init__(self):
        super().__init__('inverse_kinematics_hand')

        self.pub_index = self.create_publisher(JointState, '/index/joint_states', 10)
        self.pub_thumb = self.create_publisher(JointState, '/thumb/joint_states', 10)

        self.sub_index_tgt = self.create_subscription(
            Point, '/index/target_position', self.cb_index_tgt, 10)
        self.sub_thumb_tgt = self.create_subscription(
            Point, '/thumb/target_position', self.cb_thumb_tgt, 10)

        self.index = IndexIK()
        self.thumb = ThumbIK()

        self.tgt_index = np.array([3.5, 0.5, 0.0], dtype=float)
        self.tgt_thumb = np.array([3.2, 1.5, -0.5], dtype=float)

        self.timer = self.create_timer(0.02, self.loop) 

        self.index_names = ['q11', 'q12', 'q13']
        self.thumb_names = ['q20', 'q21', 'q22']

    def cb_index_tgt(self, msg: Point):
        self.tgt_index = np.array([msg.x, msg.y, msg.z], dtype=float)

    def cb_thumb_tgt(self, msg: Point):
        self.tgt_thumb = np.array([msg.x, msg.y, msg.z], dtype=float)

    def loop(self):
        qi = self.index.step_ik(self.tgt_index)
        qt = self.thumb.step_ik(self.tgt_thumb)

        now = self.get_clock().now().to_msg()

        msg_i = JointState()
        msg_i.header.stamp = now
        msg_i.name = self.index_names
        msg_i.position = qi.tolist()
        self.pub_index.publish(msg_i)

        msg_t = JointState()
        msg_t.header.stamp = now
        msg_t.name = self.thumb_names
        msg_t.position = qt.tolist()
        self.pub_thumb.publish(msg_t)


def main():
    rclpy.init()
    node = DualInverseKinematics()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
