
from pyesi.generator import *

#take input from user
name = input("Enter the name of the orbita: ")
orbita_type = int(input("Enter the number of orbita: "))


# Generate XML for the master with two slaves
esi = ESI()
esi.vendor_id = "0xF3F"
esi.vendor_name = "Pollen Robotcs SAS"
esi.group_name = "Pollen PYESI"
# esi.devices = []

slave = Device()
slave.name = f"{name}Orbita{orbita_type}d"

slave.sync_managers= [
    SyncManager("MBoxOut",1000, SyncManagerType.MAILBOX, SyncManagerDir.Rx, 128),
    SyncManager("MBoxIn",1180, SyncManagerType.MAILBOX, SyncManagerDir.Tx, 128),
    SyncManager("OrbitaIn",1300, SyncManagerType.BUFFERED, SyncManagerDir.Rx),
    SyncManager("OrbitaOut",1400, SyncManagerType.BUFFERED, SyncManagerDir.Tx),
]


pdos = PDOs()
pdos.sm_index = 2
pdos.name = "OrbitaIn"
pdos.entries = [Entry(name="controlword", type=EntryType.UINT16, index="0x6041")]
pdos.entries.append(Entry(name="mode_of_operation", type=EntryType.UINT8, index="0x6060"))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="target_position", type=EntryType.REAL, index="0x607A", sub_index=i+1)) 
for i in range(orbita_type):
    pdos.entries.append(Entry(name="target_velocity", type=EntryType.REAL, index="0x60FF", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="velocity_limit", type=EntryType.REAL, index="0x607F", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="target_torque", type=EntryType.REAL, index="0x6071", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="torque_limit", type=EntryType.REAL, index="0x6072", sub_index=i+1))
slave.RxPdos.append(pdos)


pdos = PDOs()
pdos.sm_index = 3
pdos.name = "OrbitaOut"
pdos.entries = [Entry(name="statusword", type=EntryType.UINT16, index="0x6040")]
pdos.entries.append(Entry(name="mode_of_operation_display", type=EntryType.UINT8, index="0x6061"))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="actual_position", type=EntryType.REAL, index="0x6064", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="actual_velocity", type=EntryType.REAL, index="0x606C", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="actual_torque", type=EntryType.REAL, index="0x6077", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="actual_axis_position", type=EntryType.REAL, index="0x6063", sub_index=i+1))
slave.TxPdos.append(pdos)


pdos = PDOs()
pdos.sm_index = 3
pdos.name = "OrbitaState"
pdos.entries.append(Entry(name="error_code", type=EntryType.UINT16, index="0x603F"))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="error_code", type=EntryType.UINT16, index="0x603F", sub_index=i+1))
pdos.entries.append(Entry(name="actuator_type", type=EntryType.UINT8, index="0x6402"))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="axis_position_zero_offset", type=EntryType.REAL, index="0x607C", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="board_temperatures", type=EntryType.REAL, index="0x6500", sub_index=i+1))
for i in range(orbita_type):
    pdos.entries.append(Entry(name="motor_temperatures", type=EntryType.REAL, index="0x6501", sub_index=i+1))
slave.TxPdos.append(pdos)

slave.enable_sdos = True
slave.enable_foe = True

esi.devices.append(slave)
tree = esi.to_xml()
print(tree)
write_xml(tree, slave.name+".xml")
print("XML file generated successfully: "+slave.name+".xml")