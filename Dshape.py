import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class Dshape_node(Node):
    def __init__(self):
        super().__init__('Dshape_node')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.callback)
        self.linear_speed = 1.0
        self.radius = 2.5
        self.angular_speed = self.linear_speed/self.radius
        self.straight_time = 2 * self.radius/self.linear_speed
        self.curve_time = math.pi * self.radius/self.linear_speed
        self.rotate_time = math.pi /(2 * self.angular_speed)
        self.state = 1 #1 for straight and 2 for semicircle 3 for rotating
        self.state_time = self.get_clock().now()

    def callback(self):
        elapsed = (self.get_clock().now() - self.state_time).nanoseconds / 1e9
        msg = Twist()

        if self.state == 1:
            if elapsed < self.straight_time:
                msg.linear.x = self.linear_speed
                msg.angular.z = 0.0
                self.pub.publish(msg)
            else:
                msg.linear.x = 0.0      
                msg.angular.z = 0.0
                self.pub.publish(msg)
                self.state = 3
                self.state_time = self.get_clock().now()
                
        elif self.state == 3:
            if elapsed < self.rotate_time:
                msg.linear.x = 0.0
                msg.angular.z = self.angular_speed
                self.pub.publish(msg)
            else:
                msg.linear.x = 0.0      
                msg.angular.z = 0.0
                self.pub.publish(msg)
                self.state = 2
                self.state_time = self.get_clock().now()

        elif self.state == 2:
            if elapsed < self.curve_time:
                msg.linear.x = self.linear_speed
                msg.angular.z = self.angular_speed
                self.pub.publish(msg)
            else:
                msg.linear.x = 0.0      # stop
                msg.angular.z = 0.0
                self.pub.publish(msg)
                


def main(args = None):
    rclpy.init(args = args)
    dshape_node = Dshape_node()
    rclpy.spin(dshape_node)
    dshape_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
