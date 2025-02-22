import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml

from enum import Enum

class EntryType(Enum):
    """
    EntryType: Enum for the type of the entry
    
    UINT8: 8-bit unsigned integer
    UINT16: 16-bit unsigned integer
    UINT32: 32-bit unsigned integer
    REAL: 32-bit float
    """
    UINT8 = "UINT8"
    UINT16 = "UINT16"
    UINT32 = "UINT32"
    REAL = "REAL"

    def bitlen(self):
        if self == self.UINT8:
            return "8"
        if self == self.UINT16:
            return "16"
        if self == self.UINT32:
            return "32"
        if self == self.REAL:
            return "32"

class SyncManagerType(Enum):
    """
    SyncManagerType: Enum for the type of the Sync Manager
    
    MAILBOX: Mailbox type
    BUFFERED: Buffered type
    """
    MAILBOX= 0,
    BUFFERED= 1
    
class SyncManagerDir(Enum):
    """
    SyncManagerDir: Enum for the direction of the Sync Manager
    
    Rx: Receive
    Tx: Transmit
    """
    Rx= 0,
    Tx= 1
    
class SyncManager:
    """
    SyncManager: Class for the Sync Manager 
    
    name: Name of the Sync Manager
    sm_type: Type of the Sync Manager
    address: Address of the Sync Manager
    enabled: Enable the Sync Manager
    default_size: Default size of the Sync Manager
    control_byte: Control byte of the Sync Manager
    dir: Direction of the Sync Manager
    """
        
    name = "Sync Manager"
    sm_type = SyncManagerType.BUFFERED
    address = "1000"
    enabled = True
    default_size = 128
    control_byte = "#x64"
    dir = SyncManagerDir.Rx
    
    def __init__(self, name, address, sm_type, sm_dir, default_size = None, enabled = 1):
        self.name = name
        self.sm_type = sm_type
        self.address = address
        self.default_size = default_size
        self.enabled = enabled
        self.dir = sm_dir
        if sm_type == SyncManagerType.MAILBOX:
            if sm_dir == SyncManagerDir.Rx:
                self.control_byte = "#x26"
            else: # Tx
                self.control_byte = "#x22"
        else: # BUFFERED
            if sm_dir == SyncManagerDir.Rx:
                self.control_byte = "#x64"
            else: # Tx
                self.control_byte = "#x20"



class Entry:
    """
    Entry: Class for the entry of the PDO
    
    name: Name of the entry
    bitlen: Bit length of the entry
    type: Type of the entry
    index: Index of the entry
    sub_index: Sub index of the entry
    """
    
    name = "Test Entry"
    bitlen = "8"
    type = EntryType.UINT8
    index = None
    sub_index = 0

    def __init__(self, name, type, index =None, sub_index = 0):
        self.name = name
        self.type = type
        self.index = index
        self.sub_index = sub_index

class PDOs:
    """
    Class representing a PDO group
    
    name: Name of the PDO group
    sm_index: Index of the Sync Manager
    entries: List of entries in the PDO group
    """
    
    name = "Test PDOs"
    sm_index = 0
    entries = []

    def __init__(self):
        self.entries = []


class Device:
    """
    Device: Class representing a slave device
    
    name: Name of the device
    TxPdos: List of Transmit PDOs
    RxPdos: List of Receive PDOs
    enable_sdos: Enable SDOs
    enable_foe: Enable FoE
    """
    
    name = "Test Device"
    
    sync_managers = []
    
    TxPdos = []
    RxPdos = []
    
    enable_sdos = False
    enable_foe = False

    def __init__(self):
        self.TxPdos = []
        self.RxPdos = []


class ESI:
    """
    ESI: Class representing the EtherCAT Slave Information
    
    vendor_id: Vendor ID
    vendor_name: Vendor Name
    lan9252: Is LAN9252
    group_type: Group Type
    group_name: Group Name
    devices: List of devices
    """
        
    vendor_id = "Test"
    vendor_name = "Test Name"

    group_type = "SSC_Device"
    group_name = "Test Group Name"
    
    lan9252 = True

    devices = []

    def __init__(self):
        self.devices = []


    # def __init__(self, device_type, device_name, product_code, revision_no, check_revision_no, group_type, pdos):

    def create_vendor(self):
        """
        create_vendor: Create the vendor element
        
        return: The vendor element
        """
        vendor = ET.Element("Vendor")
        ET.SubElement(vendor, "Id").text = self.vendor_id
        ET.SubElement(vendor, "Name").text = self.vendor_name
        ET.SubElement(vendor, "ImageData16x14").text = (
            "424dd6020000000000003600000028000000100000000e0000000100180000000000a0020000c40e0000c40e000000000000000000004cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb1224cb122ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff241cedffffff241cedffffff241ced241cedffffffffffffffffff241ced241ced241cedffffff241cedffffffffffff241cedffffff241cedffffff241cedffffff241cedffffff241cedffffff241cedffffffffffff241cedffffffffffff241cedffffff241cedffffff241cedffffff241cedffffff241cedffffff241cedffffffffffff241cedffffffffffff241cedffffff241cedffffff241cedffffff241cedffffffffffff241cedffffffffffffffffff241cedffffffffffff241ced241ced241cedffffff241ced241cedffffffffffff241cedffffff241cedffffffffffff241cedffffffffffff241cedffffff241cedffffff241cedffffff241cedffffff241cedffffff241cedffffffffffff241cedffffffffffff241cedffffff241cedffffff241cedffffff241cedffffffffffff241cedffffffffffffffffff241cedffffffffffff241cedffffff241cedffffff241cedffffff241cedffffffffffffffffffffffffffffffffffff241cedffffffffffffffffff241cedffffffffffffffffff241cedffffffffffffffffffffffffffffffffffff241ced241ced241cedffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        )
        return vendor

    def create_group(self):
        """
        create_group: Create the group element
        
        return: The group element
        """
        group = ET.Element("Group", SortOrder="0")
        ET.SubElement(group, "Type").text =  self.group_type
        ET.SubElement(group, "Name", LcId="1033").text = self.group_name
        ET.SubElement(group, "ImageData16x14").text = (
        "424dd6020000000000003600000028000000100000000e0000000100180000000000a0020000c40e0000c40e00000000000000000000241ced241ced241ced241cedffffff241cedffffffffffffffffff241cedffffffffffffffffff241cedffffffffffff241cedffffffffffffffffffffffff241cedffffffffffffffffff241cedffffffffffffffffff241cedffffffffffff241cedffffffffffffffffffffffff241ced241ced241ced241ced241cedffffffffffffffffff241cedffffffffffff241cedffffffffffffffffffffffff241cedffffffffffffffffff241cedffffffffffffffffff241cedffffffffffff241cedffffffffffffffffffffffff241ced241cedffffff241ced241cedffffff241cedffffff241cedffffff241ced241ced241ced241ced241cedffffffffffff241ced241ced241cedffffffffffff241ced241ced241ced241ced241cedffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff241ced241ced241cedffffffffffff241ced241ced241cedffffff241ced241ced241cedffffff241ced241ced241ced241cedffffffffffffffffff241cedffffffffffff241cedffffffffffffffffff241cedffffffffffffffffff241ced241cedffffffffffffffffffffffff241ced241cedffffffffffff241ced241ced241cedffffff241ced241ced241ced241ced241cedffffffffffffffffffffffffffffff241cedffffff241cedffffffffffffffffff241cedffffff241ced241cedffffffffffffffffffffffff241ced241ced241cedffffff241ced241ced241cedffffff241cedffffff241ced241cedffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff241ced241ced241cedffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        )
        return group

    def create_device(self, device):
        """
        create_device: Create the device element
        
        device: The device to create
        
        return: The device element
        """
        
        device_element = ET.Element("Device", Physics="YY")
        device_element.append(ET.Comment(f"{device.name} Device"))
        ET.SubElement(device_element, "Type", ProductCode="#x1", RevisionNo="#x1", CheckRevisionNo="EQ_OR_G").text = f'{device.name}'
        ET.SubElement(device_element, "Name", LcId="1033").text = f"{device.name}"
        ET.SubElement(device_element, "GroupType").text = "SSC_Device"

        # Add Fmmu units
        for fmmu in device.sync_managers:
            ET.SubElement(device_element, "Fmmu").text = fmmu.name

        # Add Sync Managers
        for sm in device.sync_managers:
            if sm.default_size is None:
                ET.SubElement(device_element, "Sm", StartAddress=f'#x{sm.address}', ControlByte=sm.control_byte, Enable=f"{sm.enabled}").text = sm.name
            else:
                ET.SubElement(device_element, "Sm", StartAddress=f'#x{sm.address}', DefaultSize=f"{sm.default_size}", ControlByte=sm.control_byte, Enable=f"{sm.enabled}").text = sm.name
        
        # Add RxPDOs
        pdo_index = 1600
        entry_index = 10
        for pdo in device.RxPdos:
            device_element.append(ET.Comment(f"{pdo.name} PDOs" ))
            rxpdo = ET.SubElement(device_element, "RxPdo", Fixed="1", Mandatory="1", Sm=f"{pdo.sm_index}")
            ET.SubElement(rxpdo, "Index").text = f"#x{pdo_index}"
            ET.SubElement(rxpdo, "Name").text = pdo.name
            pdo_index += 100
            for i, entry in enumerate(pdo.entries):
                e = ET.SubElement(rxpdo, "Entry")
                if entry.index is not None:
                    ET.SubElement(e, "Index").text = f"#x{entry.index}"
                else:
                    ET.SubElement(e, "Index").text = f"#x{entry_index}"
                    entry_index += 1
                ET.SubElement(e, "SubIndex").text = f"{entry.sub_index}"
                ET.SubElement(e, "BitLen").text = entry.type.bitlen()
                ET.SubElement(e, "Name").text = entry.name
                ET.SubElement(e, "DataType").text = entry.type.value

        # Add TxPDOs
        for pdo in device.TxPdos:
            device_element.append(ET.Comment(f"{pdo.name} PDOs" ))
            txpdo = ET.SubElement(device_element, "TxPdo", Fixed="1", Mandatory="1", Sm=f"{pdo.sm_index}")
            ET.SubElement(txpdo, "Index").text = f"#x{pdo_index}"
            ET.SubElement(txpdo, "Name").text = pdo.name
            pdo_index += 100
            for i, entry in enumerate(pdo.entries):
                e = ET.SubElement(txpdo, "Entry")
                if entry.index is not None:
                    ET.SubElement(e, "Index").text = f"#x{entry.index}"
                else:
                    ET.SubElement(e, "Index").text = f"#x{entry_index}"
                    entry_index += 1
                ET.SubElement(e, "SubIndex").text = f"{entry.sub_index}"
                ET.SubElement(e, "BitLen").text = entry.type.bitlen()
                ET.SubElement(e, "Name").text = entry.name
                ET.SubElement(e, "DataType").text = entry.type.value
        
        # Add Mailbox SDO and FOE if enabled
        if device.enable_sdos:
            device_element.append(self.generate_mailbox_config(device.enable_foe))
        
        # configure LAN9252
        device_element.append(self.generate_sync_manager_config())
        if self.lan9252:
            device_element.append(self.generate_ln9252_config())

        return device_element


    def generate_mailbox_config(self, enable_foe):
        """
        generate_mailbox_config: Generate the mailbox configuration
        
        enable_foe: Enable FoE
        
        return: The mailbox configuration element
        """
        mailbox_config = ET.Element("Mailbox", DataLinkLayer="true")
        ET.SubElement(mailbox_config, "CoE", SdoInfo="true", PdoAssign="false", PdoConfig="false", CompleteAccess="false", SegmentedSdo="true")
        if enable_foe:
            ET.SubElement(mailbox_config, "FoE")
        return mailbox_config

    def generate_sync_manager_config(self):
        """
        generate_sync_manager_config: Generate the sync manager configuration
        
        return: The sync manager configuration element
        """
        sync_manager = ET.Element("Dc")


        op_mode1 = ET.SubElement(sync_manager, "OpMode")
        ET.SubElement(op_mode1, "Name").text = "SM_Sync or Async"
        ET.SubElement(op_mode1, "Desc").text = "SM_Sync or Async"
        ET.SubElement(op_mode1, "AssignActivate").text = "#x0000"


        op_mode = ET.SubElement(sync_manager, "OpMode")
        ET.SubElement(op_mode, "Name").text = "DC_Sync"
        ET.SubElement(op_mode, "Desc").text = "DC_Sync"
        ET.SubElement(op_mode, "AssignActivate").text = "#x300"
        ET.SubElement(op_mode, "CycleTimeSync0", Factor="1").text = "0"
        ET.SubElement(op_mode, "ShiftTimeSync0").text = "2000200000"
        return sync_manager
 
    def generate_ln9252_config(self):
        """
        generate_ln9252_config: Generate the LAN9252 configuration
        
        return: The LAN9252 configuration element
        """
        eeprom = ET.Element("Eeprom")
        ET.SubElement(eeprom, "ByteSize").text = "4096"
        ET.SubElement(eeprom, "ConfigData").text = "8003006EFF00FF000000"
        eeprom.append(ET.Comment("0x140   0x80 PDI type LAN9252 Spi  "))
        eeprom.append(ET.Comment("0x141   0x03 device emulation     "))
        eeprom.append(ET.Comment("        enhanced link detection        "))
        eeprom.append(ET.Comment("0x150   0x00 not used for LAN9252 Spi  "))
        eeprom.append(ET.Comment("0x151   0x6E map Sync0 to AL event     "))
        eeprom.append(ET.Comment("        Sync0/Latch0 assigned to Sync0 "))
        eeprom.append(ET.Comment("        Sync1/Latch1 assigned to Sync1 "))
        eeprom.append(ET.Comment("        Sync0/1 push/pull active high  "))
        eeprom.append(ET.Comment("0x982-3 0x00FF Sync0/1 lenght = 2.5uS  "))
        eeprom.append(ET.Comment("0x152   0xFF all GPIO set to out       "))
        eeprom.append(ET.Comment("0x153   0x00 reserved                  "))
        eeprom.append(ET.Comment("0x12-13 0x0000 alias address           "))
        eeprom.append(ET.Comment("see more here: https://ww1.microchip.com/downloads/en/AppNotes/00001920A.pdf"))
        ET.SubElement(eeprom, "BootStrap").text = "0010800080108000"
        return eeprom

    def to_xml(self):
        """
        to_xml: Generate the XML tree
        
        return: The XML tree
        """
        root = ET.Element("EtherCATInfo")
        root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
        root.set('xsi:noNamespaceSchemaLocation',"EtherCATInfo.xsd")
        root.set("Version", "1.6")

        
        root.append(self.create_vendor())

        description = ET.Element("Descriptions")
        groups = ET.Element("Groups")
        groups.append(self.create_group())
        description.append(groups)

        devices = ET.Element("Devices")
        for device in self.devices:
            devices.append(self.create_device(device))
        description.append(devices)

        root.append(description)

        tree = ET.ElementTree(root)
        return tree

def prettify_xml(tree):
    """
    prettify_xml: Prettify the XML tree
    
    tree: The XML tree
    
    return: The prettified XML
    """
    raw_xml = ET.tostring(tree.getroot(), 'utf-8')
    parsed = minidom.parseString(raw_xml)
    return parsed.toprettyxml(indent="  ")


def write_xml( tree, filename):
    """
    write_xml: Write the XML tree to a file
    
    tree: The XML tree
    filename: The file name
    """
    pretty_xml = prettify_xml(tree)
    with open(filename, "w") as f:
        f.write(pretty_xml)

# Main code
if __name__ == "__main__":

    # Generate XML for the master with two slaves
    esi = ESI()
    esi.vendor_id = "#xF3F"
    esi.vendor_name = "Pollen Robotcs SAS"

    slave = Device()
    slave.name = "MyDevice"

    pdos = PDOs()
    pdos.name = "MyInputPDO"
    pdos.address = "1000"
    pdos.entries = [Entry(name="MyInput", type=EntryType.UINT32)]
    slave.TxPdos.append(pdos)

    pdos = PDOs()
    pdos.name = "MyOutputPDOs"
    pdos.address = "1200" 
    pdos.entries = [Entry(name="MyOutput", type=EntryType.UINT32)]
    slave.RxPdos.append(pdos)

    esi.devices.append(slave)
    tree = esi.to_xml()
    write_xml(tree, "myslave.xml")
    print("XML file generated successfully.")