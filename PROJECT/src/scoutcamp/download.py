
import sys, os, tempfile, logging
from urllib import request, parse


class TemplateUpdate(object):

    __template_source = "https://github.com/williamd1k0/scout-camp-template/archive/master.zip"
    __template_file = "base_project.zip"
    __version_source = "https://github.com/williamd1k0/scout-camp-template/raw/version/VERSION"
    __version_file = ".template_version"


    @staticmethod
    def get_main_path():
        path = os.path.dirname(sys.argv[0])
        if len(path) > 0:
            path += '/'
        return path


    @classmethod
    def has_update(cls):
        versions = cls.get_template_versions()
        return versions[0] < versions[1]


    @classmethod
    def get_template_versions(cls):
        version_file = cls.get_main_path()+cls.__version_file

        if not os.path.isfile(version_file):
            cls.download_version()

        open_version = open(version_file, 'r')
        version = int(open_version.read())
        open_version.close()

        cls.download_version()
        open_version = open(version_file, 'r')
        version_origin = int(open_version.read())
        open_version.close()

        open_version = open(version_file, 'w')
        open_version.write(str(version))
        open_version.close()

        cls.local_version = version
        cls.origin_version = version_origin

        return [version, version_origin]



    @classmethod
    def download_version(cls):
        return cls.download_file(cls.__version_source, cls.__version_file, False)


    @classmethod
    def download_template(cls):
        template = cls.download_file(cls.__template_source, cls.__template_file)
        cls.download_version()
        return template


    @classmethod
    def download_file(cls, url, desc=None, progress=True):
        try:
            u = request.urlopen(url)

            scheme, netloc, path, query, fragment = parse.urlsplit(url)
            filename = os.path.basename(path)
            if not filename:
                filename = 'downloaded.file'
            if desc:
                filename = cls.get_main_path()+desc

            with open(filename, 'wb') as f:
                meta = u.info()
                meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
                meta_length = meta_func("Content-Length")
                file_size = None
                if meta_length:
                    file_size = int(meta_length[0])
                if progress:
                    print(" Downloading: {0} Bytes: {1}".format(desc, file_size))

                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)

                    status = "{0:16}".format(file_size_dl)
                    if file_size:
                        status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                    status += chr(13)
                    if progress:
                        print(status, end="")
                if progress:
                    print()

        except Exception as e:
            raise

        return filename



if __name__ == '__main__':
    pass
