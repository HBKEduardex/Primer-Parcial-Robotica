import rclpy
from rclpy.node import Node
from examen_msgs.msg import Tipico


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('nodo5_sub')
        self.subscription = self.create_subscription(
            Tipico,
            'filtered_sensor',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg:Tipico):
        print(f'PROMEDIO={msg.sensor_value:.3f}  name="{msg.name}"')


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()