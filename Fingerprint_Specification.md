#Fingerprint Specification

Specifivation of how each fingerprint is organized.

##File
 The fingerprint will be a json file containing all the information making up the finger print.
 
 The top level dictionary inside the file contains two dictionaries one holds all the classes and their data, the other holds hashes for all none class files in the jar. 
 
##Classes
 Each class is a dictionary consisting of a few items:
 
 The item with the key "hash" this is the md5 (I know not that good..) hash of the class file.
 
 The item with the key "access_flags" is the access_flags for the class. (More about this later)
 
 The item "super" is the super class of the class.
 
 There is an optional item "interfaces" with contains a list of all interfaces this class implements.
 
 The item that has the key "methods" this is all the methods with the class. (More about them later)
 
 The item "fields" is all the fields defined in the class. (More on them later)
 
 The item "constants" is a dictionary.  It can conatin a entry named "numbers" and an entry named "strings" and finally an entry named "classes".
 
   These are all the numbers, strings and, classes that appear inside the classes constant pool.

##Access Flags
 The access flags determine the modifiers on the class, method or field.
 
 In the finger print they are saved as a number in which each bit of the number specifies the type of flag and if it is true or not.
 
 The following list is taken from JAWA source code. They show each flag with a hex value assocated to it.
 
 'acc_public': 0x0001,  
 
 'acc_private': 0x0002,
 
 'acc_protected': 0x0004,
 
 'acc_static': 0x0008,
 
 'acc_final': 0x0010,
 
 'acc_synchronized': 0x0020,
 
 'acc_bridge': 0x0040,
 
 'acc_varargs': 0x0080,
 
 'acc_native': 0x0100,
 
 'acc_abstract': 0x0400,
 
 'acc_strict': 0x0800,
 
 'acc_synthetic': 0x1000
 
 
##Methods
 Within the Methods array there are arrays.
 
 Each array consists of firstly the name of the method. Then its descriptors (Return types and argument types). And lastly its Access 
 Flags.
 
##Fields
 Within the Fields array there are arrays, much like with methods.
 
 Each array contains the name, the descriptors (The type) and its access flags.
