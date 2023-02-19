# Markdown排版

`markdown`源文件为`Typora`生成的为准.

`Typora`虽然支持目录生成, `TOC`方式生成的目录, 使用也很不方便, 而且目录没有编号还是有点不习惯.

[![pSLP6Y9.png](https://s1.ax1x.com/2023/02/18/pSLP6Y9.png)](https://imgse.com/i/pSLP6Y9)

## feature

- 标题自动编号
  - 具有细微修正编号异常能力例如: 在二级标题下, 准备使用 \#\#\#, 但是敲多了 \#\#\#\#.
  - 支持多次使用相同文件进行编号.
- 常见中文符号转为英文符号.
- 行首行尾的空格清理.
- 清理隐藏的零宽字符(*zero-width character*, 这个东东相当恶心, 假如出现在代码上, 假如编辑器没有显示的话).
- 清理多余的空行, 多行, 保留一行.
- 清理多余空格. 将连续的空格, 保留一个.

对于代码区块, 数学公式, 链接, 图片等内容进行了特殊的处理.

数学公式默认的标识符为`$$`

## how

```bash
# -f, filepth, 文件路径
# -i, inplace, 是否更新源文件, 默认为0, 将排版后的内容写入新的文件; 1, 覆盖源文件
# -c, contents, 是否在文件标题下添加目录, 默认为0, 不添加; 1 添加

python main.py -f "Git使用指南.md" -i 0 -c 0
```

## question

- `python`版本要求: `>= 3.9`

  ```bash
  # requirements.txt
  pip install loguru
  ```

- 如产生异常见`logs`文件夹下的日志.



