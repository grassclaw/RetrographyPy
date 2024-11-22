import ctypes
import mmap
import os

# Define constants for mmap
PROT_READ = 0x1
PROT_WRITE = 0x2
MAP_SHARED = 0x01
MAP_ANON = 0x1000

# Get a reference to the C standard library
libc = ctypes.CDLL("libc.dylib")

# Allocate 1 page (4096 bytes) of shared anonymous memory
size = 4096
memory = libc.mmap(None, size, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANON, -1, 0)

if memory == -1:
    raise OSError("mmap failed")

# Write data to the memory using ctypes
ctypes.memset(memory, 0, size)  # Initialize memory to zero
ctypes.cast(memory, ctypes.POINTER(ctypes.c_char))[0] = 65  # Write 'A' (ASCII 65) to the first byte

# Read data back
value = ctypes.cast(memory, ctypes.POINTER(ctypes.c_char))[0]
print(f"Read value from memory: {chr(value)}")

# Free memory
libc.munmap(memory, size)
