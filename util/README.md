# Util File
-

This file is for storing prototypes which are used to serially send data over USART.

Basically we're using [Google's Protocol Buffer](https://developers.google.com/protocol-buffers/). In short we're using a 
message format that is platform independent to transmit data between our Vortex (using C) and our MissionControl app (using Python).
The flow of bits and bytes works as such:
- Our data object is created
- Data is stored in the object
- We serialize the data using protobuf
- Then we send the size of our data by [packing it](http://en.wikipedia.org/wiki/Data_structure_alignment)
- Now it's time to send it over the wire!
- After reciving it, it's a simple matter to unpack
- Then unserialize the data to a usable form
