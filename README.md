# File Time Modification Tool（文件时间修改工具）

---

[English](https://github.com/Cheng-MaoMao/Windows-File-Time-Modification-Tool/blob/main/README_en.md)|简体中文

---

## 工具介绍

此工具可以修改Windows和Linux上的文件和文件夹的创建时间、修改时间和访问时间。

*⚠️Linux环境下，touch命令无法直接修改文件和文件夹的创建时间。创建时间（也称为birth time或crtime）通常是只读的，无法通过常规命令修改。*

## 功能介绍

### 现有功能

#### 1.支持批量修改文件夹和文件的创建时间、修改时间和访问时间。

#### 2.支持选择文件夹和文件夹里的内容一起修改时间和只修改文件夹里的内容的时间。

### 待优化功能

#### 1.只修改文件夹时间不修改文件夹里内容时间

#### 2.在Linux环境下支持修改创建时间

## 修改文件时间的系统命令

### 1.修改文件创建时间：

`$(Get-Item “文件路径”).creationtime=$(Get-Date "11/04/2019 20:42:23")`

### 2.修改文件最后访问时间：

`$(Get-Item “文件路径”).lastaccesstime=$(Get-Date "11/04/2019 20:42:23")`

### 3.修改文件最后修改时间：

`$(Get-Item “文件路径”).lastwritetime=$(Get-Date "11/04/2019 20:42:23")`
