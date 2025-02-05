import unittest
import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml
import os

from pyesi.generator import *

class TestEntryType(unittest.TestCase):
    def test_bitlen(self):
        self.assertEqual(EntryType.UINT8.bitlen(), "8")
        self.assertEqual(EntryType.UINT32.bitlen(), "32")
        self.assertEqual(EntryType.REAL.bitlen(), "32")

class TestEntry(unittest.TestCase):
    def test_entry_initialization(self):
        entry = Entry(name="TestEntry", type=EntryType.UINT8)
        self.assertEqual(entry.name, "TestEntry")
        self.assertEqual(entry.type, EntryType.UINT8)

class TestESI(unittest.TestCase):
    def setUp(self):
        self.esi = ESI()
        self.esi.vendor_id = "#xF3F"
        self.esi.vendor_name = "Pollen Robotics SAS"

        self.device = Device()
        self.device.name = "MyDevice"

        pdos = PDOs()
        pdos.name = "MyInputPDO"
        pdos.entries = [Entry(name="MyInput", type=EntryType.UINT32)]
        self.device.TxPdos.append(pdos)

        pdos = PDOs()
        pdos.name = "MyOutputPDO"
        pdos.entries = [Entry(name="MyOutput", type=EntryType.UINT32)]
        self.device.RxPdos.append(pdos)

        self.esi.devices.append(self.device)

    def test_create_vendor(self):
        vendor = self.esi.create_vendor()
        self.assertEqual(vendor.find("Id").text, "#xF3F")
        self.assertEqual(vendor.find("Name").text, "Pollen Robotics SAS")

    def test_create_group(self):
        group = self.esi.create_group()
        self.assertEqual(group.find("Type").text, "SSC_Device")
        self.assertEqual(group.find("Name").text, "Test Group Name")

    def test_create_device(self):
        device_element = self.esi.create_device(self.device)
        self.assertEqual(device_element.get("Physics"), "YY")
        self.assertEqual(device_element.find("Type").text, "MyDevice")

    def test_to_xml(self):
        tree = self.esi.to_xml()
        root = tree.getroot()
        self.assertEqual(root.tag, "EtherCATInfo")
        self.assertEqual(root.get("Version"), "1.6")

    def test_prettify_xml(self):
        tree = self.esi.to_xml()
        pretty_xml = prettify_xml(tree)
        self.assertIn("<EtherCATInfo", pretty_xml)

    def test_write_xml(self):
        tree = self.esi.to_xml()
        write_xml(tree, "test.xml")
        with open("test.xml", "r") as f:
            content = f.read()
            self.assertIn("<EtherCATInfo", content)
        # delete the file
        os.remove("test.xml")