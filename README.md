# pybind11 vs ctypes 性能对比测试

本项目用于对比 Python 通过 pybind11 和 ctypes 调用 C 函数的性能差异，测试场景为字符串传入与返回操作。

## 项目结构

```
bench-py/
├── src/
│   ├── string_func.c          # C 函数实现
│   ├── string_func.h          # C 函数头文件
│   └── pybind11_module.cpp    # pybind11 包装模块
├── benchmark.py                # 性能测试脚本
├── CMakeLists.txt             # CMake 构建配置
└── README.md                  # 项目说明文档
```

## 构建要求

- CMake 3.15 或更高版本
- C/C++ 编译器（支持 C++11）
- Python 3.8 或更高版本
- pybind11（已包含在项目中）

## 构建步骤

1. 创建构建目录：
```bash
mkdir build
cd build
```

2. 运行 CMake 配置：
```bash
cmake ..
```

3. 编译项目：
```bash
make
```

或者使用 CMake 的构建命令：
```bash
cmake --build .
```

## 运行测试

构建完成后，在项目根目录运行：

```bash
python3 benchmark.py
```

或者从构建目录运行（需要设置 PYTHONPATH）：

```bash
PYTHONPATH=build python3 benchmark.py
```

## 测试内容

性能测试包括以下场景：

1. **短字符串**：长度约 13 字符
2. **中等字符串**：长度 100 字符
3. **长字符串**：长度 1000 字符
4. **超长字符串**：长度 10000 字符

每个测试会运行 100,000 次迭代，并统计：
- 平均执行时间（微秒）
- 标准差
- 最小/最大执行时间
- 性能对比（pybind11 相对于 ctypes 的加速比）

## 实现细节

### C 函数

`process_string()` 函数接受一个字符串参数，返回一个复制的字符串。调用者负责释放返回的字符串内存。

### pybind11 实现

使用 pybind11 包装 C 函数，自动处理 Python 字符串与 C 字符串的转换和内存管理。

### ctypes 实现

使用 ctypes 直接调用编译好的共享库，需要手动处理：
- 字符串编码/解码（UTF-8）
- 内存管理（调用 `free_string()` 释放内存）

## 预期结果

通常，pybind11 的性能会优于 ctypes，因为：
- pybind11 在编译时进行类型检查和优化
- pybind11 自动处理类型转换，减少运行时开销
- ctypes 需要在运行时进行类型检查和转换

但实际性能差异取决于：
- 字符串长度
- 调用频率
- 系统架构
- 编译器优化选项

## 故障排除

### 找不到 pybind11 模块

确保已正确构建项目，并且 Python 可以找到生成的模块。检查 `build/` 目录中是否存在 `string_module*.so`（Linux）或 `string_module*.pyd`（Windows）。

### 找不到 ctypes 库

确保共享库已正确编译。在 Linux 上查找 `libstring_func.so`，在 macOS 上查找 `libstring_func.dylib`，在 Windows 上查找 `string_func.dll`。

### 内存泄漏

如果使用 ctypes，确保正确调用 `free_string()` 释放内存。pybind11 会自动处理内存管理。

## 许可证

本项目使用与 pybind11 相同的 BSD 许可证。

