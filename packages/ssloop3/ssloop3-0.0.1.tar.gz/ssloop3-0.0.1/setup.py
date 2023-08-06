#!/usr/bin/env python
from setuptools import setup, Extension


setup(
    name='ssloop3',
    version='0.0.1',
    packages=['ssloop3', 'ssloop3.impl'],
    package_data={
        'ssloop3': ['README.md'],
    },
    install_requires=[],
    author='mtclinton',
    author_email='max@mtclinton.com',
    url='http://github.com/mtclinton/ssloop3',
    license='MIT',
    description='super lightweight event loop',
    long_description=""" super simple event loop
                        ssloop3 is a super simple event loop that is ported from clowwindy ssloop for python3
                        
                        example::
                        
                            import sys
                            import ssloop3
                            import logging
                        
                            logging.basicConfig(level=logging.DEBUG)
                        
                            loop = ssloop3.instance()
                        
                        
                            def on_connect(s):
                                print('on_connect')
                                s.write('GET / HTTP/1.0\\r\\nHost: www.google.com\\r\\nConnection: Close\\r\\n\\r\\n')
                        
                        
                            def on_data(s, data):
                                print('on_data')
                                sys.stdout.write(data)
                        
                        
                            def on_end(s):
                                print('on_end')
                        
                        
                            def on_close(s):
                                print('on_close')
                                global loop
                                loop.stop()
                        
                        
                            def on_error(s, e):
                                print('on_error')
                                print(e)
                        
                            s = ssloop3.Socket()
                            s.on('connect', on_connect)
                            s.on('data', on_        print('on_e
                                print(e)
                            s = ssloop3.Soc
                            s.on('connect',
                            s.on('data', on
                            s.on('end', on_
                            s.on('close', o
                            s.on('error', o
                            s.connect(('www
                            loop.start()data)
                            s.on('end', on_end)
                            s.on('close', on_close)
                            s.on('error', on_error)
                            s.connect(('www.google.com', 80))
                        
                            loop.start()

    """,
    long_description_content_type='text/markdown',
)
