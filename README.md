# Copy4bk - 自动复制最新版本文件工具

一个用于自动将源目录下每个子目录中的最新版本文件复制到目标目录对应文件夹的 Python 工具。

## 功能特性

- 🔍 **自动识别最新版本**：根据文件修改时间自动识别每个子目录中的最新版本文件
- 📁 **保持目录结构**：自动在目标目录中创建对应的子目录结构
- ⚙️ **配置文件驱动**：通过配置文件管理源目录和目标目录，无需修改代码
- 🕒 **保留时间戳**：复制文件时保留原始文件的修改时间
- 📝 **详细日志**：显示每个子目录的处理过程和文件复制信息

## 使用方法

### 1. 环境要求

- Python 3.6 或更高版本
- 无需额外依赖包（使用 Python 标准库）

### 2. 配置设置

编辑 `copy4bk.txt` 配置文件，设置源目录和目标目录：

```txt
# 使用英文键名格式
source=D:\work\RiderProjects\butter-knife-win\Publish
target=D:\Resilio Sync\Resilio\QuantEdge\Apps\Windows
```

### 打包

使用**pyinstaller**打包成exe文件，打开**PyCharm**的`Terminal`输入：

```shell
pyinstaller --onefile --name Copy4bk --icon app.ico main.py
```

如果需要在exe文件名中添加版本号、版权、公司等版本信息，可以使用`--version-file`参数，例如：

```shell
pyinstaller --onefile --version-file version.txt --name Copy4bk --icon app.ico main.py
```
