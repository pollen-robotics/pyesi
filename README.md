# PyEsi package - simple EtherCAT Slave Information (ESI) XML file generator

This package is very simple and allows to create the ESI XML files for the EtherCAT slaves. 

The package builds the XML files that are to be used with LAN9252 EtherCAT slave controller.

## Installation

```bash
pip install git+git@github.com:pollen-robotics/pyesi.git
```

or just clone the repository and run the following command in the root directory:

```bash
git clone git@github.com:pollen-robotics/pyesi.git
cd pyesi
```

and then install the package:

```bash
pip install -e .
```

## Examples


### Example 1: Simple slave with buffered PDOs

```python
from pyesi.generator import *

# some global info
esi = ESI()
esi.vendor_id = "#xF3F"
esi.vendor_name = "Pollen Robotcs SAS"

# create the slave 0
slave = Device()
slave.name = "MyDevice"

# sync managers - only buffered PDOs
slave.sync_managers= [
    SyncManager("MyPDOIn",1300, SyncManagerType.BUFFERED, SyncManagerDir.Rx),
    SyncManager("MyPDOOut",1400, SyncManagerType.BUFFERED, SyncManagerDir.Tx),
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

```
### Example 2: Slave with buffered PDOs and mailbox SDOs and FoE enabled

```python
from pyesi.generator import *

# some global info
esi = ESI()
esi.vendor_id = "#xF3F"
esi.vendor_name = "Pollen Robotcs SAS"

# create the slave 0
slave = Device()
slave.name = "MyDevice"

# sync managers with the mailbox
slave.sync_managers= [
    SyncManager("MBoxOut",1000, SyncManagerType.MAILBOX, SyncManagerDir.Rx, 128),
    SyncManager("MBoxIn",1180, SyncManagerType.MAILBOX, SyncManagerDir.Tx, 128),
    SyncManager("MyPDOIn",1300, SyncManagerType.BUFFERED, SyncManagerDir.Rx),
    SyncManager("MyPDOOut",1400, SyncManagerType.BUFFERED, SyncManagerDir.Tx),
]

# create its input PDOS
pdos = PDOs()
pdos.name = "MyInputPDOs"
pdos.sm_index = 0
pdos.entries = [Entry(name="MyInput", type=EntryType.UINT32)]
slave.RxPdos.append(pdos)

# create its output PDOS
pdos = PDOs()
pdos.name = "MyOutputPDOs"
pdos.sm_index = 1
pdos.entries = [Entry(name="MyOutput", type=EntryType.UINT32)]
slave.TxPdos.append(pdos)

# enable sdos 
device.enable_sdo = True
#enable foe
device.enable_foe = True

# add it to the ESI file
esi.devices.append(slave)
tree = esi.to_xml()
write_xml(tree, "myslave.xml")
print("XML file generated successfully.")

```
    