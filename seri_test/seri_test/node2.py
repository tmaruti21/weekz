import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Printer(Node):
    def __init__(self):
        super().__init__('printer_node')

        self.sub = self.create_subscription(
            String,
            '/esp32/raw',
            self.on_msg,
            10
        )
        self.get_logger().info("Printer Started")

    def on_msg(self, msg: String):
        self.get_logger().info(f"Received : {msg.data}")

 
def main():
    rclpy.init()
    node = Printer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()