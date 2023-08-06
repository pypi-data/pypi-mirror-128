from cement import App, Controller, ex
from cores.project import Project
from cores.download import StdDownload

from cores import stdvarinit
class Base(Controller):
    class Meta:
        label = 'base'
    @ex(help='example sub-command')
    def cmd1(self):
        print('Inside Base.cmd1()')


class Stduino(App):
    class Meta:
        label = 'stduino'
        handlers = [
            Base,
            Project,
            StdDownload,
        ]

with Stduino() as app:
    app.run()


# from cement import App, Controller, ex
#
#
# class Base(Controller):
#     class Meta:
#         label = 'base'
#
#
#
#
#         arguments = [
#             # list of tuples in the format `( [], {} )`
#             ( [ '-dir', '--dir' ],{ 'help' : 'dir option','dest' : 'dir' } ),
#             ( [ '-project', '--project' ],{ 'help' : 'project option','dest' : 'project' } ),
#
#         ]
#
#
#
#     @ex(help='example sub-command')
#     def cmd1(self):
#         print('Inside Base.cmd1()')
#
#     @ex(hide=True)
#     def _default(self):
#         print('Inside BaseController._default()')
#
#         # do something with parsed arguments
#         if self.app.pargs.dir is not None:
#             print("Foo Argument => %s" % self.app.pargs.dir)
#             self.test()
#
#     @ex(help='example sub-command')
#     def test(self):
#         print(self.app.pargs.dir)
#
#
#
#
#
#
# class Stduino(App):
#     class Meta:
#         label = 'stduino'
#         handlers = [Base]
#
#
#
# with Stduino() as app:
#     app.run()