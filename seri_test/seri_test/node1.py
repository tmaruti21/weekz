import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import threading

class esp32_node(Node):
    def __init__(self):
        super().__init__('esp32_serial_node')

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baud', 9600)
        self.declare_parameter('topic', '/esp32/raw')

        port = self.get_parameter('port').value
        baud = self.get_parameter('baud').value
        topic = self.get_parameter('topic').value

        self.pub = self.create_publisher(String, topic, 10)

        self.get_logger().info(f'Opening Serial: {port} @ {baud}')
        try:
            self.ser = serial.Serial(port, baudrate = baud, timeout = 1.0)
        except Exception as e:
            self.get_logger().error(f'failed to open serial port: {e}')
            raise

        self._stop = False
        self.thread = threading.Thread(target=self.read_loop, daemon= True)
        self.thread.start()

    def read_loop(self):
        while rclpy.ok() and not self._stop:
            try:
                line = self.ser.readline().decode('utf-8', errors='replace').strip()
                if not line:
                    continue
                msg = String()
                msg.data = line
                self.pub.publish(msg)
            except Exception as e:
                self.get_logger().warn(f'Serial read error: {e}')
    
    def destroy_node(self):
        self._stop = True
        try:
            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()
        except Exception:
            pass
        super().destroy_node()
 
def main():
    rclpy.init()
    node = esp32_node()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()