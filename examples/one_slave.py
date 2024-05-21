from pyesi.generator import *

# some global info
esi = ESI()
esi.vendor_id = "#xF3F"
esi.vendor_name = "Pollen Robotcs SAS"

# create the slave 0
slave = Device()
slave.name = "MyDevice"

# create its input PDOS
pdos = PDOs()
pdos.name = "MyInputPDO"
pdos.address = "1000"
pdos.entries = [Entry(name="MyInput", type=EntryType.UINT32)]
slave.RxPdos.append(pdos)

# create its output PDOS
pdos = PDOs()
pdos.name = "MyOutputPDOs"
pdos.address = "1200"
pdos.entries = [Entry(name="MyOutput", type=EntryType.UINT32)]
slave.TxPdos.append(pdos)

# add it to the ESI file
esi.devices.append(slave)
tree = esi.to_xml()
write_xml(tree, "myslave.xml")
print("XML file generated successfully.")