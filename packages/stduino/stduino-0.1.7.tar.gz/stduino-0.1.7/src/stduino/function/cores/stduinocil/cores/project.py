from cement import Controller, ex
import os
from cores import stdvarinit
class Project(Controller):
    class Meta:
        label = 'project'
        stacked_type = 'nested'
        stacked_on = 'base'


    #self.pio_env + " project init -d " + target_path + " --board " + stdinit.board_id + " -O framework=" + framework
    def is_platform_installed(self):
        curat = stdvarinit.std_platform_dir+"/"+self.app.pargs.p
        print(curat)
        if os.path.exists(curat):
            return True
        else:
            return False

        pass
    @ex(
        help='init project-command',
        arguments=[
            (['-d'],{'help': 'path of project','action': 'store','dest': 'd'}),
            (['-p'], {'help': 'platform of project', 'action': 'store', 'dest': 'p'}),
            (['-b'], {'help': 'board of project', 'action': 'store', 'dest': 'b'}),
            (['-f'], {'help': 'framework to ini of project', 'action': 'store', 'dest': 'f'}),
            (['-g'], {'help': 'debugtool to ini of project', 'action': 'store', 'dest': 'g'}),
        ]
    )
    def init(self):
        print(self.app.pargs.O)
        if self.is_platform_installed():
            print(self.app.pargs.p)
            print('project is build')
            pass
        else:
            print('cant build project')

        pass
    @ex(help='list items',
        arguments=[
            (['-d'],{'help': 'path of project','action': 'store','dest': 'd'}),
        ])
    def list(self):
        print(self.app.pargs.d)
        print('Inside Nested.cmd3()')
        pass

    @ex(help='create new item')
    def create(self):
        pass

    @ex(help='update an existing item')
    def update(self):
        pass

    @ex(help='delete an item')
    def delete(self):
        pass

    @ex(help='complete an item')
    def complete(self):
        pass
