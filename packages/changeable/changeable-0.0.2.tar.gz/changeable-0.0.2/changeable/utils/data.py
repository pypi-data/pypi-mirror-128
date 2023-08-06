# -*- coding: utf-8 -*-
# @Author  : LG

import os
from xml.etree import ElementTree as ET
from multiprocessing import Pool
import shutil

class ImageChecker(object):
    """
    图片检测器基类
    """
    def __init__(self, recursion:bool=False):
        self.all_num = 0
        self.invalid_num = 0

        self.recursion = recursion
        self.suffix = ''
        self.start_char = None
        self.end_char = None

        self.invalid_list = []

    def check(self, root):
        files = os.listdir(root)
        for file in files:
            file = os.path.join(root, file)
            if os.path.isfile(file) and file.endswith('.{}'.format(self.suffix)):
                self.all_num += 1
                try:
                    with open(file, 'rb')as f:
                        f.seek(-len(self.end_char), 2)
                        if f.read() != self.end_char:
                            print('Found error {} file:{}'.format(self.suffix, file))
                            self.invalid_list.append(file)
                            self.invalid_num += 1
                except:
                    print('Found error {} file:{}'.format(self.suffix, file))
                    self.invalid_list.append(file)
                    self.invalid_num += 1

            elif os.path.isdir(file) and self.recursion:
                self.check(file)
        return True

    def __call__(self, root:str) -> list:
        self.check(root)
        print('Found error {} file: {}/{}'.format(self.suffix, self.invalid_num, self.all_num))
        return self.invalid_list

class JpgChecker(ImageChecker):
    def __init__(self, recursion:bool=False):
        """
        检查jpg图像完整性，通过设置recursion递归处理子文件夹文件
        :param recursion:   是否递归处理子文件夹

        eg:
            递归检查 测试图片 目录下的所有.jpg后缀图片
            invalid_list = JpgChecker(recursion=True)('/测试图片')
            print(invalid_list)
        """
        super(JpgChecker, self).__init__(recursion)
        self.suffix = 'jpg'
        self.start_char = b'\xff\xd8'
        self.end_char = b'\xff\xd9'

class PngChecker(ImageChecker):
    def __init__(self, recursion:bool=False):
        """
         检查png图像完整性，通过设置recursion递归处理子文件夹文件
         :param recursion:   是否递归处理子文件夹
         """
        super(PngChecker, self).__init__(recursion)
        self.suffix = 'png'
        self.start_char = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
        self.end_char = b'\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'

class XmlOp(object):
    """
    xml检测器基类
    """
    def __init__(self, recursion:bool=False):
        self.recursion = recursion

    def work(self, xml:str):
        raise NotImplementedError

    def __call__(self, root:str):
        files = os.listdir(root)
        for file in files:
            file = os.path.join(root, file)
            if os.path.isfile(file) and file.endswith('.xml'):
                self.work(file)
            elif os.path.isdir(file) and self.recursion:
                self(file)
        print("Finished!")

class XmlReplaceName(XmlOp):
    def __init__(self, old_name:str, new_name:str, recursion:bool=False):
        """
        替换xml文件类别名
        :param old_name:    旧类别名
        :param new_name:    新类别名
        :param recursion:   是否递归处理子文件夹
        """
        super(XmlReplaceName, self).__init__(recursion)
        self.old_name = old_name
        self.new_name = new_name

    def work(self, xml:str):
        try:
            tree = ET.parse(xml)
            objs = tree.findall('object')
            for obj in objs:
                name = obj.find('name').text
                if name == self.old_name:
                    obj.find('name').text = self.new_name
            tree.write(xml)
        except Exception as e:
            print("Error {} : {}".format(xml, e))

class XmlDelObjectByName(XmlOp):
    def __init__(self, name:str, recursion:bool=False):
        """
        删除xml中指定类别名的目标
        :param name:        待删除的目标类别名
        :param recursion:   是否递归处理子文件夹
        """
        super(XmlDelObjectByName, self).__init__(recursion)
        self.name = name

    def work(self, xml:str):
        try:
            tree = ET.parse(xml)
            root = tree.getroot()
            objs = tree.findall('object')
            for obj in objs:
                name = obj.find('name').text
                if name == self.name:
                    root.remove(obj)
            tree.write(xml)
        except Exception as e:
            print("Error {} : {}".format(xml, e))

class XmlIsInvalid(XmlOp):
    def __init__(self, remove:bool=False, recursion:bool=False):
        """
        查找或删除目录下空的以及无目标的xml文件
        :param remove:      是否删除查找到的xml文件
        :param recursion:   是否递归处理子文件夹

        eg:
            # 递归删除root文件夹及其子文件夹下的所有为空的xml以及无标注目标的xml
            checker = XmlIsInvalid(remove=True, recursion=True)
            checker(root)
        """
        super(XmlIsInvalid, self).__init__(recursion)
        self.remove = remove

    def work(self, xml:str):
        try:
            tree = ET.parse(xml)
            objs = tree.findall('object')
            if len(objs) < 1:
                if self.remove:
                    try:
                        os.remove(xml)
                        print('Found and remove no object xml file: {}'.format(xml))
                    except:
                        print('Found no object xml file: {}, but remove failed.'.format(xml))
                else:
                    print('Found no object xml file: {}'.format(xml))
        except:
            if self.remove:
                try:
                    os.remove(xml)
                    print('Found and remove invalid xml file: {}'.format(xml))
                except:
                    print('Found invalid xml file: {}, but remove failed.'.format(xml))
            else:
                print('Found invalid xml file: {}'.format(xml))

class XmlInsertElement(XmlOp):
    def __init__(self, to_tag:str, tag:str, attrib:dict={}, text:str=None, recursion=True):
        """
        在指定元素内，插入新节点
        :param to_tag:      插入到该标签下， 如果存在多个，均进行插入
        :param tag:         插入元素的标签
        :param attrib:      插入元素的属性, 必须是str
        :param text:        插入元素的文本
        :param recursion:   递归处理文件夹下所有xml

        eg:
            # 对root文件夹及其子文件夹中的所有xml文件进行插入操作，将<aaa a="1">0.0</aaa>插入到object中
            inserter = XmlInsertElement(to_tag='object', tag='aaa', attrib={"a": '1'}, text="0.0", recursion=True)
            inserter(root)
        """
        super(XmlInsertElement, self).__init__(recursion)
        self.to_tag = to_tag
        self.tag = tag
        self.attrib = attrib
        self.text = text

    def work(self, xml:str):
        try:
            tree = ET.parse(xml)
            root = tree.getroot()
            if self.to_tag == root.tag:
                to_objs = [root]
            else:
                to_objs = tree.findall(self.to_tag)
            for obj in to_objs:
                insert_element = ET.Element(self.tag, self.attrib)
                insert_element.text = self.text
                insert_element.tail = list(obj)[0].tail if list(obj) else "\n"
                obj.insert(0, insert_element)
            tree.write(xml)

        except Exception as e:
            print("Error {} : {}".format(xml, e))

class CopyMultiprocess(object):
    def __init__(self, suffix:str=None, num_processes:int=10, recursion:bool=False, rename=False):
        """
        对文件夹下指定文件执行多线程复制
        :param from_root:       文件夹
        :param to_root:         目标文件夹
        :param suffix:          文件后缀，不指定则复制全部文件
        :param num_processes:   线程数
        :param recursion:       是否递归处理子文件夹(递归处理时，同名文件会被覆盖!)
        :param rename           是否重命名, 主要针对递归处理子文件夹时的重名文件。递归处理文件夹时，会将文件重命名为：文件夹名-[...]-文件名

        eg:
            cpoier = CopyMultiprocess(suffix='jpg', recursion=True, rename=True)
            cpoier(from_root, to_root)
        """
        self.suffix = suffix
        self.pool = Pool(num_processes)
        self.recursion = recursion
        self.rename = rename
        self.base_root = ""
        self.all_nums = 0
        self.current = 0
        self.bar = None

    @staticmethod
    def copy_ops(path, to_path):
        try:
            if os.path.exists(to_path):
                print("Exist {}, will overwrite!".format(to_path))
            shutil.copy(path, to_path)
            return True
        except Exception as e:
            print("Error {}: {}".format(path, e))
            return False

    def work(self, from_root:str, to_root:str):
        files = os.listdir(from_root)
        for file in files:
            file_path = os.path.join(from_root, file)
            if os.path.isfile(file_path):
                if self.suffix is not None and not file_path.endswith(self.suffix):
                    continue
                if self.rename:
                    file_name = '-'.join(file_path.lstrip(self.base_root).split('/'))
                else:
                    file_name = os.path.split(file_path)[-1]
                to_path = os.path.join(to_root, file_name)
                self.pool.apply_async(self.copy_ops, (file_path, to_path, ))
            elif os.path.isdir(file_path) and self.recursion:
                self.work(file_path, to_root)

    def __call__(self, from_root, to_root):
        self.base_root = from_root
        self.work(from_root, to_root)
        self.pool.close()
        self.pool.join()
