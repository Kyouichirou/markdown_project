# Markdown排版

`markdown`源文件为`Typora`生成的为准.

`Typora`虽然支持目录生成, `TOC`方式生成的目录(但是移植也是问题), 使用也很不方便, 而且目录没有编号还是有点不习惯.

目录编号采用以下规则:

- 一级目录, 不操作, 默认为内容的主标题
- 二级目录采用中文的`一, 二, 三...十...`
- 二级目录以下, 采用数字`1.1, 1.1.1, 1.1.1.1, ....`

[![pSLP6Y9.png](https://s1.ax1x.com/2023/02/18/pSLP6Y9.png)](https://imgse.com/i/pSLP6Y9)

## Features

- 标题自动编号
  - 尝试修正编号异常, 例如: 在二级标题下, 准备使用 \#\#\#, 但是敲多了 \#\#\#\#, 避免在嵌套层级过深时, 敲少 `#`符号.
  - 支持多次使用相同文件进行编号, 原先的编号将自动撤销.
- 添加目录到文件内容(非`TOC`标签)
- **常见中文符号转为英文符号**.(默认开启)
- 行首行尾的空格清理.(默认开启)
- 清理隐藏的零宽字符(*zero-width character*, 这个东东相当恶心, 假如出现在代码上, 假如编辑器没有显示的话)(默认开启).
- 清理多余的空行, 多行, 保留一行.
- **清理多余空格**. 将连续的空格, 保留一个.
- 侦测代码区间的标签闭合情况, 提示异常出现的位置.

对于代码区块, 数学公式, 链接, 图片等内容进行了特殊的处理, 数学公式默认的标识符为`$$`.

## How

```bash
# -f, filepth, 文件路径

# -i, inplace, 内容写入方式, 默认为0, 将排版后的内容写入新的文件(recommend); 1, 覆盖原文件

# -c, contents, 是否在文件标题下添加目录, 默认为0, 不添加; 1 添加

python main.py -f "Git使用指南.md" -i 0 -c 0
```

## Question

- `python`版本要求: `>= 3.9`

  ```bash
  # requirements.txt
  pip install loguru
  ```

- 如产生异常见`logs`文件夹下的日志.

### 关于`Typora`代码区间标签闭合

`Typora`显示代码块并不一定需要标签的闭合

[![pSOsLqJ.png](https://s1.ax1x.com/2023/02/20/pSOsLqJ.png)](https://imgse.com/i/pSOsLqJ)

由于需要使用两个闭合的标签来判断代码的区间进行排版, 假如没有闭合将导致排版的异常, 简易开启`语法自动成对`

[![pSOsXZ9.png](https://s1.ax1x.com/2023/02/20/pSOsXZ9.png)](https://imgse.com/i/pSOsXZ9)

在代码中也将尝试侦测代码区间的闭合情况

[![pSOyeit.png](https://s1.ax1x.com/2023/02/20/pSOyeit.png)](https://imgse.com/i/pSOyeit)
