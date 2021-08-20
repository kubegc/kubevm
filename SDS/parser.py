import argparse

try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET

tree = ET.parse('cmd.xml')
root = tree.getroot()


# --------------------------- cmd line parser ---------------------------------------
parser = argparse.ArgumentParser(prog="kubesds-adm", description="All storage adaptation tools")

subparsers = parser.add_subparsers(help="sub-command help")

pool = root.find('pool')
ops = pool.findall("operation")
for op in ops:
    # -------------------- add sub cmd ----------------------------------
    name = "%sPool" % op.attrib['name']
    sub_parser = subparsers.add_parser(name, help="%s help" % name)

    args = op.findall('args')
    args_check = {}
    for arg in args:
        sub_parser.add_argument("--%s" % arg.attrib['name'], metavar="[dir|uus|nfs|glusterfs|uraid]", type=eval(arg.attrib['type']),
                                help="storage pool type to use")
        args_check[arg.attrib['name']] = eval(arg.attrib['require'])
def executor(args_check, ):
    pass
    # if 'disk' == disk.attrib['device']:
    #     source_element = disk.find("source")
    #     if source_element.get("file") == source:
    #         source_element.set("file", target)
    #         tree.write('/tmp/%s.xml' % vm)


