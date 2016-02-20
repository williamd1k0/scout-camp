from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os, tempfile, logging
import urllib2
import urlparse

class Download(object):

    __template_source = "https://github.com/TheTimeTunnel/scout-camp-template/archive/master.zip"
    __template_file = "base_project.zip"
    __version_source = "https://github.com/TheTimeTunnel/scout-camp-template/raw/version/VERSION"
    __version_file = "temp_version.sc"


    @classmethod
    def get_template(cls):
        template_file = os.path.dirname(sys.argv[0])
        if len(template_file) > 0:
            template_file += '/'

        if os.path.isfile(template_file+cls.__template_file):


    @classmethod
    def get_template_version(cls):
        pass

    @classmethod
    def download_version(cls):
        return cls.download_file(cls.__version_source, cls.__version_file)


    @classmethod
    def download_template(cls):
        return cls.download_file(cls.__template_source, cls.__template_file)


    @staticmethod
    def download_file(url, desc=None):
        try:
            u = urllib2.urlopen(url)

            scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
            filename = os.path.basename(path)
            if not filename:
                filename = 'downloaded.file'
            if desc:
                filename = os.path.join(desc, filename)

            with open(filename, 'wb') as f:
                meta = u.info()
                meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
                meta_length = meta_func("Content-Length")
                file_size = None
                if meta_length:
                    file_size = int(meta_length[0])
                print("Downloading: {0} Bytes: {1}".format(url, file_size))

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
                    print(status, end="")
                print()

        except Exception as e:
            raise

        return filename
