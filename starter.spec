# -*- mode: python -*-

block_cipher = None


a = Analysis(['starter.py'],
             pathex=['h:\\Repos\\winwin\\winwin\\winwin'],
             binaries=None,
             datas=None,
             hiddenimports=['commctrl', 'win32gui', 'pywinauto'],
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
          name='starter',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='winwin.ico')
