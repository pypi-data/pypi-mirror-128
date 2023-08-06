from cores import stdvarinit
from cement import Controller,ex
import os
import urllib.request
import tarfile
class StdDownload(Controller):
    class Meta:
        label = 'stddownload'
        stacked_type = 'nested'
        stacked_on = 'base'
        arguments = [
            (['-t'], {'help': 'type of package file', 'action': 'store', 'dest': 'type'}),
            (['-n'], {'help': 'name of package file', 'action': 'store', 'dest': 'name'}),
        ]
    plat=None

    @ex(hide=True)
    def _default(self):
        self.downfile()
    def geturl(self):
        if self.app.pargs.type=="platform":
            print("plat")
            return "https://stduino-generic.pkg.coding.net/stduino_packages/stdplatforms/" + self.app.pargs.name

        else:
            return "https://stduino-generic.pkg.coding.net/stduino_packages/stdpackages/" + self.app.pargs.name

        pass
    def downfile(self):

        pa=stdvarinit.stdcache_dir+"/"+ self.app.pargs.name
        pas = stdvarinit.std_platform_dir + "/" + self.app.pargs.name
        ud="https://stduino-generic.pkg.coding.net/stduino_packages/piopackages/framework-lgt8fx-1.0.6.tar.gz?version=latest"
        url=self.geturl()
        urllib.request.urlretrieve(ud, pa)
        self.untar_file(pa, pas)

        # with zipfile.ZipFile(pa, mode="r") as f:
        #     f.extractall(pas)

    def untar_file(self,file,tarpath):
        t = tarfile.open(file)
        t.extractall(path=tarpath)
        pass
    def tar_file(self,tarfile,tarpath):
        pass
    def delfile(self):
        pass



