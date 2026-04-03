import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8

class number_node(Node):
    def __init__(self):
        super().__init__('number_node')
        self.number_pub = self.create_publisher(Int8, '/number', 10)
        self.number_sub = self.create_subscription(Int8, '/count', self.number_callback, 10)
        self.n = 0
        self.init_timer = self.create_timer(0.5, self.init_callback)
    
    def number_callback(self, msg):
        if msg.data < self.n:
            pass
        elif msg.data == self.n:
            self.n += 1  
        self.get_logger().info(f'Recieved count: {msg.data}, Publsihed n: {self.n}')
        out_msg = Int8()
        out_msg.data = self.n
        self.number_pub.publish(out_msg)

    def init_callback(self):
        self.init_timer.cancel()
        self.get_logger().info(f'Initial n: {self.n}')
        out_msg = Int8()
        out_msg.data = self.n
        self.number_pub.publish(out_msg)

def main(args = None):
    rclpy.init(args = args)
    numbernode = number_node()
    rclpy.spin(numbernode)
    numbernode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        