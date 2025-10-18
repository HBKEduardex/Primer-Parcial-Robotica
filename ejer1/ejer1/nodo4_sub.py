import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from examen_msgs.msg import Tipico



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('nodo4_sub')

        self.ultimo = {'sensor_1': None, 'sensor_2': None, 'sensor_3': None}

        self.subscription1 = self.create_subscription( Float64,'sensor_1',self.listener_callback('sensor_1'),
            10)
        self.subscription2 = self.create_subscription( Float64,'sensor_2',self.listener_callback('sensor_2'),
            10)
        self.subscription3 = self.create_subscription( Float64,'sensor_3',self.listener_callback('sensor_3'),
            10)
        ########
        self.publisher= self.create_publisher(Tipico, 'filtered_sensor', 10)

    def listener_callback(self, sensor_name: str):
        
        def aux(msg: Float64):
            self.promedio(sensor_name, msg)
        return aux
    
    def promedio(self, sensor_name: str, msg: Float64):

        self.ultimo[sensor_name] = float(msg.data)

        if None not in self.ultimo.values():
            s1 = self.ultimo['sensor_1']
            s2 = self.ultimo['sensor_2']
            s3 = self.ultimo['sensor_3']
            promedio = (s1 + s2 + s3) / 3.0
            print("PROMEDIO =", promedio, "(s1=", s1, ", s2=", s2, ", s3=", s3, ")")
            out = Tipico(sensor_value= promedio, name='avg(sensor_1,sensor_2,sensor_3)')
            self.publisher.publish(out)

            self.get_logger().info(f'→ /filtered_sensor: {out.sensor_value:.3f} ({out.name})')

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