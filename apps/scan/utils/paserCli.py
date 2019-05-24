from configparser import ConfigParser


class ConfigParserCli(object):
    def __init__(self, file):
        """
        导入一个文件 生成我们需要的json
        :param file:
        """
        self.file = file
        self.cfg = ConfigParser(allow_no_value=True)

    def cfg_load(self):
        """
        # 把 文件导入管理对象中，把文件内容load到内存中
        :return:
        """
        self.cfg.read(self.file)

    def cfg_dump(self):
        se_list = self.cfg.sections()  # cfg.sections()显示文件中的所有 section
        print('<======CONFIG=====>')
        for se in se_list:
            print("\t\t<= " + se + " =>")
            print(dict(self.cfg.items(se)))
        print('</=====END-CONFIG=====>')


    def add_section_items(self, section, temp_dict):
        """

        :param section: 单个选项. 就是增加一个[]
        :param temp_dict: 导入的字典列表
        :return:
        """
        if not self.cfg.has_section(section):
            self.add_section(section)
        for key in temp_dict.keys():
            self.set_item(section, key, temp_dict[key])

    def dump_by_json_config(self, res_json):
        """
        通过JSON导入到ini
        :param res_json: json 对象
        :return:
        """
        for section in res_json.keys():
            self.add_section_items(section, res_json[section])

    def delete_item(self, se, key):
        """
         # 在 section 中删除一个 item
        :param se:
        :param key:
        :return:
        """
        self.cfg.remove_option(se, key)

    def delete_section(self, se):
        """
         # 删除一个 section
        :param se:
        :return:
        """
        self.cfg.remove_section(se)

    def add_section(self, se):
        """
        # 添加一个 section
        :param se:
        :return:
        """
        self.cfg.add_section(se)

    def set_item(self, se, key, value):
        self.cfg.set(se, key, value)

    def save(self):
        fd = open(self.file, 'w')
        self.cfg.write(fd)
        fd.close()


def demo_test():
    ## print(s.encode('gbk').decode('utf-8'))
    info = ConfigParserCli('settings.ini')
    info.cfg_load()
    info.dump_by_json_config({
        "manager": {
            "name": 'actanble',
            "email": "actanble@gmail.com",
            "personal_net": 'http://www.kac.fun',
        },
        "deppend_url": {
            "url": 'blog.csdn.net/actanble',
            "desc": 'No_add_desc',
        },
    })
    info.cfg_dump()
    info.save()