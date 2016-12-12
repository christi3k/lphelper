import cmd, sys, subprocess, re, inspect

class LphShell(cmd.Cmd):
    intro = 'Welcome to the lp-helper shell.  Type help or ? to list commands.\n'
    prompt = '(lph) '
    file = None

    def do_lpass(self, arg):
        'Invoke lastpass cli'

    def do_ls(self, args):
        'Refresh list of items, or groups. (Default: groups.)'

        # ls (no arguments): list of all groups
        # ls <groupname>: list of all items in that group

        #print(inspect.getargspec(self.get_groups))
        if len(args) == 0:
            self.get_groups()
        else:
            self.get_items(args)

    def do_show(self, args):
        'Display details for a given entry id'

        if len(args) == 0:
            return True
        else:
            self.get_item(args)

    def do_exit(self, arg):
        return True

    def get_groups(self):
        groups = []
        try:
            output = subprocess.check_output(["lpass", "ls"], universal_newlines=True)
            lines = output.splitlines()
            
            for line in lines:
                m = re.search(r"(?P<group_name>\(*\w+\)*)/(?P<item_name>.*(?=\s+\[id+:\s*\d*\]))", line)
                if m:
                    line_dict = m.groupdict()
                    if line_dict['group_name'] not in groups:
                        groups.append(line_dict['group_name'])
            groups.sort()
            groups_count = len(groups)
            print('\n')
            print('There are {0} group(s):\n'.format(groups_count))
            i = 1
            for group in groups:
                print('{0}. {1}'.format(i,group))
                i += 1
        except subprocess.CalledProcessError as err:
            print("Command error: ", err)
            print(err.output)

    def get_items(self, args):
        print("\nHere we will print a list of items beloning to group [{0}]".format(args))
        try:
            output = subprocess.check_output(["lpass", "ls", args], universal_newlines=True)
            lines = output.splitlines()
            print("\n{0} item(s) found belonging to [{1}] group:\n".format(len(lines), args))
            print("\nID\t\tNAME\n")
            print("============================================")
            for line in lines:
                m = re.search(r"(?P<group_name>\(*\w+\)*)/(?P<item_name>.+?) \[id: (?P<item_id>(?<=\s\[id:\s).*(?=\]))", line)
                if m:
                    line_dict = m.groupdict()
                    print("{0}\t{1}".format(line_dict['item_id'], line_dict['item_name']))
        except subprocess.CalledProcessError as err:
            print("Command error: ", err)
            print(err.output)

        return True

    def get_item(self, args):
        print("\nHere we will print the detail for a given item id: [{0}]".format(args))
        try:
            output = subprocess.check_output(["lpass", "show", "--all", args], universal_newlines=True)
            lines = output.splitlines()
            for line in lines:
                print(line)
        except subprocess.CalledProcessError as err:
            print("Command error: ", err)
            print(err.output)

        return True

if __name__ == '__main__':
    LphShell().cmdloop()
