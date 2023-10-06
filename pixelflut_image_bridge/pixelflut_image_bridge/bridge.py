#!/usr/bin/env python3

import rclpy
from cv_bridge import CvBridge
from PIL import Image as PILImage
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import Image as SensorMsgsImage

from pixelflut_image_bridge.draw_image import draw_image
from pixelflut_image_bridge.pixelflut_image_bridge_parameters import pixelflut_image_bridge


class BridgeNode(Node):
    """
    Bridge Node class that receives Image messages and floods them to a Pixelflut server.
    """

    def __init__(self) -> None:
        node_name = "pixelflut_image_bridge_node"
        super().__init__(node_name)
        self.get_logger().info(f"Starting {node_name}...")

        self.cv_bridge = CvBridge()
        self.param_listener = pixelflut_image_bridge.ParamListener(self)
        self.params = self.param_listener.get_params()
        self.create_subscription(SensorMsgsImage, self.params.image_topic, self.image_callback, 1)

    def image_callback(self, msg: SensorMsgsImage) -> None:
        """
        Callback that is called when a new Image message is received.
        This converts the Image message to a PIL Image and sends it to the Pixelflut server.

        :param msg SensorMsgsImage: The Image message that was received.
        """
        self.get_logger().info("Image received")
        self.send_image_to_pixelflut_server(self.convert_to_pil_image(msg))

    def convert_to_pil_image(self, msg: SensorMsgsImage) -> PILImage.Image:
        """
        Converts an Image message to a PIL Image using the cv_bridge.

        :param msg SensorMsgsImage: The Image message to convert.
        :return PILImage: The converted PIL Image.
        """
        print(msg.width, msg.height)
        return PILImage.fromarray(self.cv_bridge.imgmsg_to_cv2(msg, "bgr8"))

    def send_image_to_pixelflut_server(self, image: PILImage.Image) -> None:
        """
        Sends a PIL Image to the Pixelflut server.

        :param image PILImage: The PIL Image to send.
        """
        draw_image(self.params.host, self.params.port, image)
        self.get_logger().info(f"Sent image to Pixelflut server at {self.params.host}:{self.params.port}.")


def main(args=None):
    rclpy.init(args=args)
    node = BridgeNode()
    ex = MultiThreadedExecutor(num_threads=2)
    ex.add_node(node)
    ex.spin()
    node.destroy_node()
    rclpy.shutdown()
