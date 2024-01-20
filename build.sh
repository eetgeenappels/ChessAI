rm -r dist
rm -r build
pyinstaller --onedir --windowed --add-data "assets/wit_Stalin.png:." --add-data "assets/:assets/" --osx-bundle-identifier me.eetgeenappels.nathanchess --target-architecture x86_64 nathan_chess.py 
