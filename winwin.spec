# -*- mode: python -*-

block_cipher = None


a = Analysis(['winwin\\winwin.py'],
             pathex=['h:\\Repos\\winwin\\winwin\\winwin'],
             binaries=None,
             datas=None,
             hiddenimports=['commctrl', 'win32gui', 'pywinauto', 'maboio'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='winwin',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='winwin.ico')
