import pefile

pe = pefile.PE("/Users/raz.shenkman/Desktop/SharedFiles.exe")

for entry in pe.DIRECTORY_ENTRY_IMPORT:
  print entry.dll.decode('utf-8') + " imports:"
  for imp in entry.imports:
    print '\t', hex(imp.address), imp.name