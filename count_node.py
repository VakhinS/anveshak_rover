import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8

class count_node(Node):
    def __init__(self):
        super().__init__('count_node_pub')
        self.publisher = self.create_publisher(Int8, '/count', 10)
        self.subscriber = self.create_subscription(Int8, '/number', self.callback, 10)
        self.counter = 0
    
    def callback(self, msg):
        self.counter += 1
        self.get_logger().info(f'Recieved number = {msg.data} , Publishing count = {self.counter}')
        msg_out = Int8()
        msg_out.data = self.counter
        self.publisher.publish(msg_out)

def main(args = None):
    rclpy.init(args = args)
    countnode = count_node()
    rclpy.spin(countnode)
    countnode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        