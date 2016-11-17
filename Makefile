# mabozen

# modified on 2014-04-26 21:47:34

ALL: ;

starter:
	pyinstaller --onefile --icon=app.ico maboio/starter.py
    
ziyan0:
	pyinstaller --onefile --hidden-import=maboio.resources.ak_query --hidden-import=maboio.resources.bep_query --icon=chitu3.ico maboio/ziyan.py

chitu:
	pyinstaller --onefile --hidden-import=influxdb --icon=chitu3.ico maboio/chitu.py

watchman:
	pyinstaller --onefile --hidden-import=requests --icon=io.ico maboio/watchman.py

ziyan:
	pyinstaller --onefile --hidden-import=commctrl --hidden-import=win32gui --hidden-import=pywinauto --hidden-import=maboio.lib --icon=winwin.ico start.py
    
chitu_spec:
	pyinstaller chitu_m.spec

install:
	c:\python27\python setup.py install

run:
	python setup.py install
	python maboio/chitu.py -c conf/chitu.toml
    
mon_chitu:
	nodemon -e py,toml,json --ignore logs/ --exec "make" run

mon_ziyan0:
	nodemon -e py,toml --exec "python.exe" maboio/ziyan.py

mon_ziyan:
	nodemon -e py,lua,toml --exec "c:/python27/python.exe" starter.py
    
mon_watchman:
	make install
	nodemon -e py,toml --exec "python.exe" maboio/watchman.py

test:
	py.test test

benchmark:
	python benchmark/benchmark3.py

nose:
	nosetests -v -x

.PHONY: test  benchmark