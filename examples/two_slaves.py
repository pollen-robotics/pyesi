from pyesi.generator import *

# some global info
esi = ESI()
esi.vendor_id = "#xF3F"
esi.vendor_name = "Pollen Robotcs SAS"

for i in range(2):
    # create the slave 0
    slave = Device()
    slave.name = f"MyDevice {i}"

    # sync managers - only buffered PDOs
    slave.sync_managers= [
        SyncManager("MyPDOIn",1000, SyncManagerType.BUFFERED, SyncManagerDir.Rx),
        SyncManager("MyPDOOut",1200, SyncManagerType.BUFFERED, SyncManagerDir.Tx),
    ]
    
    # create its input PDOS
    pdos = PDOs()
    pdos.name = "MyInputPDO"
    pdos.sm_index = 0
    pdos.entries = [Entry(name="MyInput", type=EntryType.UINT32)]
    slave.RxPdos.append(pdos)

    # create its output PDOS
    pdos = PDOs()
    pdos.name = "MyOutputPDOs"
    pdos.sm_index = 1
    pdos.entries = [Entry(name="MyOutput", type=EntryType.UINT32)]
    slave.TxPdos.append(pdos)

    # add it to the ESI file
    esi.devices.append(slave)
    
tree = esi.to_xml()
write_xml(tree, "myslave.xml")
print("XML file generated successfully.")