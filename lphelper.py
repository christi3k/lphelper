import cmd, sys, subprocess, re

class LphShell(cmd.Cmd):
    intro = 'Welcome to the lp-helper shell.  Type help or ? to list commands.\n'
    prompt = '(lph) '
    file = None

    def do_lpass(self, arg):
        'Invoke lastpass cli'

    def do_groups(self, arg):
        'Refresh list of groups.'

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

    def do_exit(sef, arg):
        return True

if __name__ == '__main__':
    LphShell().cmdloop()
