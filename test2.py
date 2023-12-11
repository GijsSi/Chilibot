import can

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native')# socketcan_nativ
msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], extended_id=False)
can0.send(msg)