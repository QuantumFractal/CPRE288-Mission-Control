""" Proto tester """

import usart_pb2

depth_data = usart_pb2.depth_data()

depth_data.depth_array.extend([12,20,30,40])

print depth_data.SerializeToString()