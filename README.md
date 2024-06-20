# Windows File Time Modification Tool（Windows 文件时间修改工具）
---
## 工具介绍
此工具只能修改Windows文件资源管理器里看到的文件时间。想要修改文件时间，在网上找了很多工具都要收费，找到一个免费的但是很复杂，所以自己找了相关的Windows系统命令，用AI写了一个python工具，分享给有需要的人。
## 功能介绍
### 现有功能
1.支持批量修改文件夹和文件的创建时间、修改时间和访问时间。
2.支持选择文件夹和文件夹里的内容一起修改时间和只修改文件夹里的内容的时间。
### 待优化功能
1.只修改文件夹时间不修改文件夹里内容时间
## 修改文件时间的系统命令
### 1.修改文件创建时间：
`$(Get-Item “文件路径”).creationtime=$(Get-Date "11/04/2019 20:42:23")`
### 2.修改文件最后访问时间：
`$(Get-Item “文件路径”).lastaccesstime=$(Get-Date "11/04/2019 20:42:23")`
### 3.修改文件最后修改时间：
`$(Get-Item “文件路径”).lastwritetime=$(Get-Date "11/04/2019 20:42:23")`
