import os

folderName = "src"

# os.mkdir( )
# os.makedirs('./src/components')
# os.('ejemplo.txt')
file = open('ejemplo.txt', "w")
file.write("console.log('hola')")
file.close()
os.rename('ejemplo.txt','ejemplo.ts')