File Time Modification Tool (文件时间修改工具)
---

English|简体中文

---

This tool can modify the creation time, modification time, and access time of files and folders on Windows and Linux.
*⚠️On Linux, the touch command cannot directly modify the creation time of files and folders. The creation time (also known as the birth time or crtime) is usually read-only and cannot be modified by conventional commands.*

## Function Introduction

### Existing Functions

#### 1. Support batch modification of the creation time, modification time, and access time of folders and files.

#### 2. Support selecting folders and modifying the time of the folder and its contents together or only modifying the time of the folder's contents.

### Optimization Functions

#### 1. Modifying the time of the folder only, not the time of its contents

#### 2. Supporting modification of the creation time on Linux environments.

## System Commands for Modifying File Times

### 1. Modifying the creation time of a file:

`$(Get-Item “file path”).creationtime=$(Get-Date “11/04/2019 20:42:23”)`

### 2. Modifying the last access time of a file:

`$(Get-Item “file path”).lastaccesstime=$(Get-Date “11/04/2019 20:42:23”)`

### 3. Modifying the last modification time of a file:

`$(Get-Item “file path”).lastwritetime=$(Get-Date “11/04/2019 20:42:23”)`
