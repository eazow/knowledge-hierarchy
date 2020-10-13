# 介绍

本文档给出了Python代码的编码约定。

该样式指南会随着时间的流逝而发展，因为会发现其他约定，而过去的约定由于语言本身的更改而变得过时。

许多项目都有自己的编码风格准则。如有任何冲突，此类项目特定的指南优先于该项目。

# 一致性

代码的读取次数比编写的次数多。此处提供的指南旨在提高代码的可读性，并使其在各种Python代码中保持一致。正如[PEP 20](https://www.python.org/dev/peps/pep-0020/)所说，“可读性至关重要”。

样式指南是关于一致性的。与该样式指南的一致性很重要。项目内的一致性更为重要。一个模块或功能内的一致性是最重要的。

但是，要知道何时会出现不一致的情况-有时样式指南的建议并不适用。如有疑问，请运用最佳判断。查看其他示例并确定最合适的方法。

特别是：不要仅仅为了遵守本PEP而向后兼容

忽略特定准则的其他一些好的理由：

1. 应用指南时，即使对于那些习惯阅读遵循此PEP的代码的人来说，也会使代码的可读性降低。
2. 为了与周围的代码一致（也可能是出于历史原因），该代码也会破坏它（尽管这也是清理别人的混乱的机会）。
3. 由于所讨论的代码早于准则的引入，因此没有其他理由修改该代码。
4. 当代码需要与不支持样式指南建议的功能的Python的较旧版本兼容时。

# 代码布局

## 缩进

每个缩进级别使用4个空格。

续行应该使用在括号，括号和花括号内连接的Python隐式线垂直对齐包裹的元素，或使用*悬挂式缩进* [3](https://pep8.org/#fn3)。使用悬挂式缩进时，应考虑以下几点：第一行不应有任何论点，而应使用进一步的缩进来清楚地将其区分为延续行。

Yes：

```python
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# More indentation included to distinguish this from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

No：

```python
# Arguments on first line forbidden when not using vertical alignment.
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

对于连续行，4空格规则是可选的。

可选的：

```python
# Hanging indents *may* be indented to other than 4 spaces.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```



当`if`语句的条件部分足够长而要求将其写成多行时，可接受的选项包括但不限于：

```python
# No extra indentation.
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# Add a comment, which will provide some distinction in editors
# supporting syntax highlighting.
if (this_is_one_thing and
    that_is_another_thing):
    # Since both conditions are true, we can frobnicate.
    do_something()

# Add some extra indentation on the conditional continuation line.
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

（另请参见下面有关在二进制运算符之前还是之后中断的讨论。）

多行构造的右花括号/括号/括号可以在列表最后一行的第一个非空白字符下对齐，如下所示：

```python
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```

或者可以将其排在开始多行构造的行的第一个字符下，例如：

```python
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

## 制表符或空格？

空格是首选的缩进方法。

制表符应仅用于与已经用制表符缩进的代码保持一致。

Python 3不允许混合使用制表符和空格进行缩进。

缩进制表符和空格混合在一起的Python 2代码应仅转换为使用空格。

使用该`-t`选项调用Python 2命令行解释器时，它会发出有关非法混用制表符和空格的代码的警告。使用`-tt`这些警告时会出错。强烈建议您使用这些选项！

## 最大长度

限制所有行最多79个字符。

为了使较长的文本块具有较少的结构限制（文档字符串或注释），行长应限制为72个字符。

通过限制所需的编辑器窗口宽度，可以并排打开多个文件，并且在使用在相邻列中显示两个版本的代码查看工具时，效果很好。

大多数工具中的默认包装会破坏代码的视觉结构，使其更难以理解。选择这些限制是为了避免在窗口宽度设置为80的编辑器中进行换行，即使在换行时该工具在最后一列中放置了标志符号也是如此。某些基于Web的工具可能根本不提供动态换行。

一些团队强烈喜欢更长的线长。对于专门或主要由可以在此问题上达成协议的团队维护的代码，可以将标称行长度从80个字符增加到100个字符（有效地将最大长度增加到99个字符），前提是注释和文档字符串仍被包装为72个字符。

Python标准库是保守的，需要将行数限制为79个字符（文档字符串/注释数限制为72个）。

换行的首选方法是在括号，方括号和花括号内使用Python的隐含行连续性。通过将表达式包装在括号中，可以将长行分成多行。应优先使用这些，而不是使用反斜杠进行行连续。

有时反斜杠仍然适用。例如，长的多`with`语句不能使用隐式连续，因此可以使用反斜杠：

```python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

（有关缩进多行[语句](https://pep8.org/#if-statements)缩进的进一步思考，请参见前面关于[多行if语句的](https://pep8.org/#if-statements)讨论`with`。）

另一个这样的情况是with`assert`语句。

确保适当缩进续行。

## 换行符应该在二进制运算符之前还是之后？

几十年来，推荐的样式是二元运算符之后的突破。但这会以两种方式损害可读性：运算符趋向于分散在屏幕上的不同列上，并且每个运算符都从其操作数移至上一行。在这里，眼睛必须做额外的工作才能分辨出添加了哪些项目和减去了哪些项目：

```python
# No: operators sit far away from their operands
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

为了解决此可读性问题，数学家及其发布者遵循相反的约定。Donald Knuth在他的“*计算机和排版”*系列中解释了传统规则：

> “尽管段落中的公式总是在二进制运算和关系之后中断，但显示的公式总是在二进制运算和关系之前中断” [4](https://pep8.org/#fn4)。

遵循数学的传统，通常会导致代码更具可读性：

```python
# Yes: easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

在Python代码中，只要约定在本地是一致的，就可以在二进制运算符之前或之后中断。对于新代码，建议使用Knuth的样式。

## 空行

用两个空行包围顶级函数和类定义。

类内的方法定义由单个空白行包围。

多余的空白行可以（分别）用于分隔相关功能组。一堆相关的单线（例如，一组虚拟实现）之间可以省略空白行。

在函数中使用空白行，以节省空间，以指示逻辑部分。

Python接受control-L（即^ L）换页字符作为空格；许多工具将这些字符视为页面分隔符，因此您可以使用它们来分隔文件相关部分的页面。请注意，某些编辑器和基于Web的代码查看器可能不会将control-L识别为换页，而将在其位置显示另一个标志符号。

## 源文件编码

核心Python发行版中的代码应始终使用UTF-8（或Python 2中的ASCII）。

使用ASCII（在Python 2中）或UTF-8（在Python 3中）的文件不应具有编码声明。

在标准库中，非默认编码仅应用于测试目的，或者在注释或文档字符串需要提及包含非ASCII字符的作者姓名时；否则，使用`\x`，`\u`，`\U`，或`\N`逃逸是包含在字符串非ASCII数据的首选方式。

对于Python 3.0及更高版本，标准库规定了以下策略（请参阅[PEP 3131](https://www.python.org/dev/peps/pep-3131)）：Python标准库中的所有标识符务必使用纯ASCII标识符，并且在可行的情况下应使用英文单词（在许多情况下，缩写和技术使用的术语不是英语）。此外，字符串文字和注释也必须使用ASCII。唯一的例外是（a）测试非ASCII功能的测试用例，以及（b）作者的姓名。名称不基于拉丁字母的作者必须提供其姓名的拉丁音译。

鼓励具有全球受众的开源项目采取类似的政策。

## Import

- 导入通常应放在单独的行上，例如：

  Yes：

  ```python
  import os
  import sys
  ```

  No：

  ```python
  import os, sys
  ```

  可以这样说：

  ```python
  from subprocess import Popen, PIPE
  ```

- 导入总是放在文件的顶部，紧随任何模块注释和文档字符串之后，以及模块全局变量和常量之前。

  导入应按以下顺序分组：

  1. 标准库导入
  2. 相关第三方进口
  3. 本地应用程序/特定于库的导入

  您应该在每组导入之间放置一个空白行。

- 推荐使用绝对导入，因为如果导入系统配置不正确（例如，程序包中的目录最终位于时`sys.path`），则它们通常更易于阅读，并且通常表现得更好（或至少会提供更好的错误消息）：

  ```python
  import mypkg.sibling
  from mypkg import sibling
  from mypkg.sibling import example
  ```

  但是，显式相对导入是绝对导入的一种可接受的替代方法，尤其是在处理复杂的包装布局时，使用绝对导入会不必要地冗长：

  ```python
  from . import sibling
  from .sibling import example
  ```

  标准库代码应避免复杂的程序包布局，并始终使用绝对导入。

  *绝对*不要使用隐式相对导入，并且在Python 3中已将其删除。

- 从包含类的模块中导入类时，通常可以这样拼写：

  ```python
  from myclass import MyClass
  from foo.bar.yourclass import YourClass
  ```

  如果此拼写引起本地名称冲突，请拼写它们：

  ```python
  import myclass
  import foo.bar.yourclass
  ```

  并使用`myclass.MyClass`和`foo.bar.yourclass.YourClass`。

- `from <module> import *`应避免使用通配符导入（），因为通配符不能弄清楚名称空间中存在哪些名称，这会混淆阅读器和许多自动化工具。通配符导入有一个合理的用例，它是将内部接口重新发布为公共API的一部分（例如，使用可选加速器模块中的定义覆盖接口的纯Python实现，以及确切的定义将是事先未知）。

  以这种方式重新发布名称时，以下有关公共和内部接口的准则仍然适用。

## 模块级dunder名称

模块级“dunders”（即名称具有两个前缘和两个纵下划线），例如`__all__`，`__author__`，`__version__`等应被放置在模块文档字符串之后，但在任何导入语句*除了* `from __future__`进口。Python要求将来导入必须在模块中出现在除文档字符串以外的任何其他代码之前。

例如：

```python
"""This is the example module.

This module does stuff.
"""

from __future__ import barry_as_FLUFL

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```



# 字符串引号

在Python中，单引号字符串和双引号字符串是相同的。本PEP对此不做任何建议。选择一条规则并坚持下去。但是，当字符串包含单引号或双引号字符时，请使用另一个以避免在字符串中使用反斜杠。它提高了可读性。

对于三引号字符串，请始终使用双引号字符以与[PEP 257中](https://www.python.org/dev/peps/pep-0257/)的docstring约定一致。



# 表达式和语句中的空格

## Pet Peeves

在以下情况下，请避免使用多余的空格：

- 紧靠在括号，方括号或大括号内：

  Yes：

  ```python
  spam(ham[1], {eggs: 2})
  ```

  No：

  ```python
  spam( ham[ 1 ], { eggs: 2 } )
  ```

- 在尾随逗号和后面的右括号之间：

  Yes：

  ```python
  foo = (0,)
  ```

  No：

  ```python
  bar = (0, )
  ```

- 在逗号，分号或冒号之前：

  Yes：

  ```python
  if x == 4: print x, y; x, y = y, x
  ```

  No：

  ```python
  if x == 4 : print x , y ; x , y = y , x
  ```

- 但是，在切片中，冒号的行为类似于二元运算符，并且在每一侧都应具有相等的数量（将其视为优先级最低的运算符）。在扩展切片中，两个冒号必须应用相同的间距。例外：省略slice参数时，将省略空格。

  Yes：

  ```python
  ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
  ham[lower:upper], ham[lower:upper:], ham[lower::step]
  ham[lower+offset : upper+offset]
  ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
  ham[lower + offset : upper + offset]
  ```

  No：

  ```python
  ham[lower + offset:upper + offset]
  ham[1: 9], ham[1 :9], ham[1:9 :3]
  ham[lower : : upper]
  ham[ : upper]
  ```

- 在打开圆括号之前，该圆括号开始一个函数调用的参数列表：

  Yes：

  ```python
  spam(1)
  ```

  No：

  ```python
  spam (1)
  ```

- 在开括号之前立即开始索引或切片：

  Yes：

  ```python
  dct['key'] = lst[index]
  ```

  No：

  ```python
  dct ['key'] = lst [index]
  ```

- 赋值（或其他）运算符周围有多个空格，以使其与另一个对齐。

  Yes：

  ```python
  x = 1
  y = 2
  long_variable = 3
  ```

  No：

  ```python
  x             = 1
  y             = 2
  long_variable = 3
  ```

## 其他建议

- 避免在任何地方拖尾空格。因为它通常是不可见的，所以可能会造成混淆：例如，反斜杠后跟一个空格和一个换行符不算作行继续标记。一些编辑器没有保留它，并且许多项目（例如CPython本身）都具有拒绝它的预提交钩子。

- 总是围绕这些二元运算符在任一侧的单个空间：分配（`=`），增量赋值（`+=`，`-=`等），比较（`==`，`<`，`>`，`!=`，`<>`，`<=`，`>=`，`in`，`not in`，`is`，`is not`），布尔值（`and`，`or`，`not`）。

- 如果使用优先级不同的运算符，请考虑在优先级最低的运算符周围添加空格。使用您自己的判断；但是，永远不要使用一个以上的空间，并且在二进制运算符的两边总是具有相同数量的空白。

  Yes：

  ```python
  i = i + 1
  submitted += 1
  x = x*2 - 1
  hypot2 = x*x + y*y
  c = (a+b) * (a-b)
  ```

  No：

  ```python
  i=i+1
  submitted +=1
  x = x * 2 - 1
  hypot2 = x * x + y * y
  c = (a + b) * (a - b)
  ```

- `=`当用于指示关键字参数或默认参数值时，请勿在符号周围使用空格。

  Yes：

  ```python
  def complex(real, imag=0.0):
      return magic(r=real, i=imag)
  ```

  No：

  ```python
  def complex(real, imag = 0.0):
      return magic(r = real, i = imag)
  ```

- 函数注释应使用冒号的常规规则，并且`->`如果有的话，箭头周围总是有空格。（有关[功能注释](https://pep8.org/#function-annotations)的更多信息，请参见下面的功能注释。）

  Yes：

  ```python
  def munge(input: AnyStr): ...
  def munge() -> AnyStr: ...
  ```

  No：

  ```python
  def munge(input:AnyStr): ...
  def munge()->PosInt: ...
  ```

- 将参数注释与默认值组合时，请在`=`符号周围使用空格（但仅适用于同时具有注释和默认值的参数）。

  Yes：

  ```python
  def munge(sep: AnyStr = None): ...
  def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
  ```

  No：

  ```python
  def munge(input: AnyStr=None): ...
  def munge(input: AnyStr, limit = 1000): ...
  ```

- 通常不建议使用复合语句（同一行上的多个语句）。

  Yes：

  ```python
  if foo == 'blah':
      do_blah_thing()
  do_one()
  do_two()
  do_three()
  ```

  No：

  ```python
  if foo == 'blah': do_blah_thing()
  do_one(); do_two(); do_three()
  ```

- 虽然有时可以将if / for / while的小主体放在同一行上是可以的，但对于多子句语句则永远不要这样做。也要避免折叠这么长的线！

  Rather not:

  ```python
  if foo == 'blah': do_blah_thing()
  for x in lst: total += x
  while t < 10: t = delay()
  ```

  Definitely not:

  ```python
  if foo == 'blah': do_blah_thing()
  else: do_non_blah_thing()
  
  try: something()
  finally: cleanup()
  
  do_one(); do_two(); do_three(long, argument,
                               list, like, this)
  
  if foo == 'blah': one(); two(); three()
  ```



# 何时使用尾随逗号

尾部的逗号通常是可选的，但当组成一个元素的元组时它们是必需的（并且在Python 2中，它们具有该`print`语句的语义）。为了清楚起见，建议将后者用（技术上多余的）括号括起来。

Yes：

```python
FILES = ('setup.cfg',)
```

OK，但是令人困惑：

```python
FILES = 'setup.cfg',
```

如果结尾的逗号多余，则在使用版本控制系统时，当值，参数或导入项的列表预计会随着时间扩展时，它们通常会很有用。模式是将每个值（等）单独放在一行上，始终添加尾随逗号，并在下一行上添加右括号/括号/花括号。但是，在与结束定界符相同的行上使用尾随逗号是没有意义的（在上述单例元组的情况下除外）。

Yes：

```python
FILES = [
    'setup.cfg',
    'tox.ini',
    ]
initialize(FILES,
           error=True,
           )
```

No：

```python
FILES = ['setup.cfg', 'tox.ini',]
initialize(FILES, error=True,)
```



# 评论

与代码矛盾的注释比没有注释更糟糕。当代码更改时，始终优先考虑最新注释！

评论应为完整句子。如果注释是短语或句子，则除非注释是以小写字母开头的标识符，否则其第一个单词应大写（切勿更改标识符的大小写！）。

如果评论简短，则可以省略结尾的句点。整体注释通常由一个或多个完整句子组成的段落组成，每个句子都应以句点结尾。

句子结尾后应使用两个空格。

编写英语时，请遵循Strunk和White。

来自非英语国家的Python编码人员：请用英语写您的评论，除非您有120％的把握确保不会说这种语言的人不会阅读该代码。

## 阻止评论

块注释通常适用于其后的一些（或全部）代码，并且缩进到与该代码相同的级别。块注释的每一行都以`#`和开头（除非注释内的文本是缩进的）。

块注释中的段落由包含单个的行分隔`#`。

## 内联评论

谨慎使用内联注释。

内联注释是与语句在同一行上的注释。内联注释应与该语句至少分隔两个空格。它们应以＃和单个空格开头。

内联注释是不必要的，并且如果它们表明显而易见，则实际上会分散注意力。

不要这样做：

```python
x = x + 1                 # Increment x
```

但是有时候，这很有用：

```python
x = x + 1                 # Compensate for border
```

## 文档字符串

在[PEP 257中](https://www.python.org/dev/peps/pep-0257/)，编写好的文档字符串（也称为“文档字符串”）的约定很好。

- 为所有公共模块，函数，类和方法编写文档字符串。对于非公共方法，文档字符串不是必需的，但是您应该具有描述该方法功能的注释。该注释应出现在该`def`行之后。

- [PEP 257](https://www.python.org/dev/peps/pep-0257/)描述了良好的文档字符串约定。请注意，最重要的是`"""`，以多行docstring结尾的本身应位于一行上，例如：

  ```python
  """Return a foobang
  
  Optional plotz says to frobnicate the bizbaz first.
  """
  ```

- 对于一个内衬文档字符串，请使结尾处保持`"""`同一行。



# 命名约定

Python库的命名约定有些混乱，因此我们永远都无法做到完全一致–尽管如此，这是当前推荐的命名标准。新的模块和软件包（包括第三方框架）应按照这些标准编写，但是如果现有库具有不同的样式，则首选内部一致性。

## 首要原则

对于用户而言，作为API公共部分可见的名称应遵循反映用法而不是实现的约定。

## 描述性：命名样式

有很多不同的命名样式。能够独立于它们的用途来识别正在使用的命名样式。

通常区分以下命名样式：

- `b` （单个小写字母）
- `B` （单个大写字母）
- `lowercase`
- `lower_case_with_underscores`
- `UPPERCASE`
- `UPPER_CASE_WITH_UNDERSCORES`
- `CapitalizedWords`（或CapWords，CamelCase [5](https://pep8.org/#fn5)和StudlyCaps）
- `mixedCase` （与大小写字母的首字母小写字母不同！）
- `Capitalized_Words_With_Underscores` （丑陋！）

**注意：**

在CapWords中使用缩写词时，将所有缩写词大写。因此`HTTPServerError`比`HttpServerError`更好。

还有一种使用短的唯一前缀将相关名称组合在一起的样式。这在Python中使用不多，但是为了完整起见提到它。例如，`os.stat()`函数返回一个元组，其项目通常有类似的名字`st_mode`，`st_size`，`st_mtime`等等。（这样做是为了强调与POSIX系统调用结构的字段的对应关系，这有助于程序员熟悉该结构。）

X11库将前导X用于其所有公共功能。在Python中，这种样式通常被认为是不必要的，因为属性和方法名称以对象为前缀，函数名称以模块名作为前缀。

此外，还可以识别出以下使用前划线或后划线的特殊形式（通常可以将它们与任何大小写惯例结合使用）：

- `_single_leading_underscore`：“内部使用”指示器较弱。例如`from M import *`，不导入名称以下划线开头的对象。

- `single_trailing_underscore_`：按惯例用于避免与Python关键字冲突，例如：

  ```python
  Tkinter.Toplevel(master, class_='ClassName')
  ```

- `__double_leading_underscore`：在命名类属性时，调用名称修饰（在类FooBar内部，`__boo`变为`_FooBar__boo`;见下文）。

- `__double_leading_and_trailing_underscore__`：位于用户控制的名称空间中的“魔术”对象或属性。例如`__init__`，`__import__`或`__file__`。请勿发明此类名称；仅按记录使用它们。

## 说明性：命名约定

### 避免使用的名称

切勿将字符“ l”（小写字母l），“ O”（大写字母o）或“ I”（大写字母i）用作单个字符变量名称。

在某些字体中，这些字符与数字1和零没有区别。当尝试使用“ l”时，请改用“ L”。

### ASCII兼容性

标准库中使用的标识符必须与[PEP 3131](https://www.python.org/dev/peps/pep-3131)的[策略部分](https://www.python.org/dev/peps/pep-3131/#policy-specification)中所述的ASCII兼容。

### 软件包和模块名称

模块应使用简短的全小写名称。如果模块名称可以提高可读性，则可以在模块名称中使用下划线。尽管不鼓励使用下划线，但Python软件包也应使用短的全小写名称。

当用C或C ++编写的扩展模块具有随附的Python模块提供更高级别（例如，面向对象）的接口时，C / C ++模块具有一个下划线（例如`_socket`）。

### 类名

类名通常应使用CapWords约定。

在接口被记录并主要用作可调用函数的情况下，可以代替使用函数的命名约定。

请注意，内置名称有一个单独的约定：大多数内置名称是单个单词（或两个单词一起运行），而CapWords约定仅用于异常名称和内置常量。

### 类型变量名称

在PEP 484引入的类型变量的名称通常应当使用CapWords宁愿短名称：`T`，`AnyStr`，`Num`。建议在用于声明协变或反变行为的变量中添加后缀`_co`或`_contra`变量。例子

```python
from typing import TypeVar

  VT_co = TypeVar('VT_co', covariant=True)
  KT_contra = TypeVar('KT_contra', contravariant=True)
```

### 异常名称

因为异常应该是类，所以此处使用类命名约定。但是，您应该在异常名称上使用后缀“ Error”（如果异常实际上是一个错误）。

### 全局变量名

（我们希望这些变量只能在一个模块内使用。）约定与函数的约定大致相同。

设计用于via的模块`from M import *`应使用`__all__`防止导出全局变量的机制，或使用较早的约定在此类全局变量前加下划线（您可能需要这样做以指示这些全局变量是“模块非公共”）。

### 功能名称

函数名称应小写，必要时用下划线分隔单词，以提高可读性。

仅在已经是主流样式（例如threading.py）的上下文中才允许使用mixedCase，以保持向后兼容性。

### 函数和方法参数

始终使用`self`实例方法的第一个参数。

始终使用`cls`类方法的第一个参数。

如果函数参数的名称与保留关键字发生冲突，通常最好在其后附加一个下划线，而不要使用缩写或拼写错误。因此`class_`比更好`clss`。（也许更好的办法是使用同义词来避免此类冲突。）

### 方法名称和实例变量

使用函数命名规则：小写字母，单词以下划线分隔，以提高可读性。

仅对非公共方法和实例变量使用前导下划线。

为避免名称与子类发生冲突，请使用两个下划线来调用Python的名称处理规则。

Python用类名来修饰这些名称：如果Foo类具有一个名为的属性`__a`，则不能通过来访问它`Foo.__a`。（坚持的用户仍然可以通过调用获得访问权限`Foo._Foo__a`。）通常，双引号下划线仅应用于避免名称与设计为子类的类中的属性发生冲突。

**注意：**关于__name的使用存在一些争议（请参见下文）。

### 常数

常量通常在模块级别定义，并以所有大写字母书写，并用下划线分隔单词。示例包括`MAX_OVERFLOW`和`TOTAL`。

### 为继承而设计

始终确定类的方法和实例变量（统称为“属性”）应该是公共的还是非公共的。如有疑问，请选择非公开；稍后将其公开比使公共属性不公开要容易。

公共属性是您期望班级中不相关的客户端使用的属性，并承诺避免向后不兼容的更改。非公开属性是指不打算由第三方使用的属性；您不保证非公共属性不会更改甚至被删除。

我们在这里不使用术语“私有”，因为在Python中没有任何属性是真正私有的（通常没有不必要的工作量）。

另一类属性是属于“子类API”（在其他语言中通常称为“受保护”）的那些属性。某些类被设计为可继承的，以扩展或修改类行为的各个方面。在设计这样的类时，请务必明确决定哪些属性是公共属性，哪些是子类API的一部分，哪些属性仅真正由您的基类使用。

考虑到这一点，以下是Python准则：

- 公共属性不应包含前导下划线。

- 如果您的公共属性名称与保留关键字冲突，请在属性名称后附加一个下划线。这优于缩写或拼写错误。（但是，尽管有此规则，对于已知为类的任何变量或参数，尤其是类方法的第一个参数，“ cls”是首选的拼写。）

  **注1**：有关类方法，请参见上面的参数名称建议。

- 对于简单的公共数据属性，最好仅公开属性名称，而不使用复杂的访问器/更改器方法。请记住，如果您发现简单的数据属性需要增强功能行为，那么Python为将来的增强提供了一条简便的途径。在那种情况下，使用属性将功能实现隐藏在简单的数据属性访问语法之后。

  **注1**：属性仅适用于新型类。

  **注2**：尽量保持功能行为的副作用，尽管诸如缓存之类的副作用通常很好。

  **注3**：避免将属性用于计算昂贵的操作；属性符号使调用者认为访问（相对）便宜。

- 如果您的类打算被子类化，并且您具有不希望使用子类的属性，请考虑使用双引号和下划线来命名它们。这将调用Python的名称修改算法，其中将类的名称修改为属性名称。这有助于避免属性名称冲突，如果子类无意中包含具有相同名称的属性。

  **注1**：请注意，整齐的名称中仅使用简单的类名，因此，如果子类同时选择相同的类名和属性名，则仍会发生名称冲突。

  **注2**：名称修饰可以使某些用途，例如调试和使用`__getattr__()`不太方便。但是，名称修饰算法已被详细记录，并且易于手动执行。

  **注3**：并非每个人都喜欢改名。尝试在避免意外名称冲突与高级呼叫者潜在使用之间进行权衡。

## 公共和内部接口

任何向后兼容性保证都仅适用于公共接口。因此，重要的是用户能够清楚地区分公共接口和内部接口。

除非文档明确声明它们是临时接口或内部接口不受通常的向后兼容性保证，否则文档化接口被视为公共接口。所有未记录的接口都应假定为内部接口。

为了更好地支持自省，模块应该使用`__all__`属性在其公共API中显式声明名称。设置`__all__`为空列表表示该模块没有公共API。

即使`__all__`设置适当，内部接口（包，模块，类，函数，属性或其他名称）仍应以单个下划线作为前缀。

如果任何包含名称空间（包，模块或类）的内部接口都被视为内部接口，则该接口也被视为内部接口。

导入的名称应始终被视为实现细节。其他模块不得依赖对此类导入名称的间接访问，除非它们是包含模块的API中明确记录的一部分，例如`os.path`或`__init__`暴露了子模块功能的软件包模块。

# 编程建议

- 应该以不损害Python其他实现（PyPy，Jython，IronPython，Cython，Psyco等）的方式编写代码。

  例如，不要依赖CPython对`a += b`或形式的语句的就地字符串连接的有效实现`a = a + b`。即使在CPython中，这种优化也是脆弱的（仅适用于某些类型），并且在不使用引用计数的实现中根本不存在这种优化。在库的性能敏感部分中，`''.join()`应使用表格代替。这将确保在各种实现方式中串联发生在线性时间内。

- 与单例（如None）的比较应始终使用`is`或进行`is not`，绝不能使用相等运算符进行。

  另外，当心`if x`您的意思`if x is not None`，例如当测试是否将默认设置为None的变量或参数设置为其他值时，请当心编写。另一个值可能具有在布尔上下文中可能为false的类型（例如容器）！

- 使用`is not`运算符而不是`not ... is`。尽管两个表达式在功能上相同，但前者更易读和首选。

  Yes：

  ```python
  if foo is not None:
  ```

  No：

  ```python
  if not foo is None:
  ```

- 当有比较丰富排序执行的操作，最好是实现所有六个操作（`__eq__`，`__ne__`，`__lt__`，`__le__`，`__gt__`，`__ge__`）而不是依靠其他代码，只行使特定的比较。

  为了最大程度地减少工作量，`functools.total_ordering()`装饰器提供了一种生成缺少的比较方法的工具。

  [PEP 207](https://www.python.org/dev/peps/pep-0207/)表明，反身性的规则*是*由Python的假设。因此，解释器可以交换`y > x`与`x < y`，`y >= x`与`x <= y`，并且可以交换的参数`x == y`和`x != y`。在`sort()`和`min()`保证操作使用`<`操作符和`max()`函数使用的`>`运营商。但是，最好实现所有六个操作，以免在其他情况下不会造成混淆。

- 始终使用def语句而不是将lambda表达式直接绑定到标识符的赋值语句。

  Yes：

  ```python
  def f(x): return 2*x
  ```

  No：

  ```python
  f = lambda x: 2*x
  ```

  第一种形式表示结果函数对象的名称专门为“ f”，而不是通用的“ <lambda>”。通常，这对于回溯和字符串表示形式更为有用。使用赋值语句消除了lambda表达式相对于显式def语句（即，可以将其嵌入较大的表达式中）提供的唯一好处。

- 从而`Exception`不是从派生异常`BaseException`。直接继承自`BaseException`保留给异常，在这些异常中捕获错误几乎总是错误的事情。

  基于可能需要*捕获*异常的代码的区别来设计异常层次结构，而不是根据引发异常的位置进行设计。旨在回答“出了什么问题？”的问题 以编程方式，而不是仅说明“发生了问题”（有关内置异常层次结构正在学习的课程的示例，请参阅[PEP 3151](https://www.python.org/dev/peps/pep-3151/)）

  类命名约定在此处适用，但是如果异常是错误，则应在异常类中添加后缀“ Error”。用于非本地流控制或其他形式的信令的非错误异常不需要特殊的后缀。

- 适当使用异常链接。在Python 3中，应使用“从Y提高X”来表示显式替换，而不会丢失原始回溯。

  故意替换内部异常时（在Python 2中使用“提高X”或在Python 3.3+中使用“从无提高X”），请确保将相关详细信息转移到新的异常（例如在将KeyError转换为AttributeError时保留属性名称） ，或将原始异常的文本嵌入新的异常消息中）。

- 在Python 2中引发异常时，请使用，`raise ValueError('message')`而不要使用旧的形式 `raise ValueError, 'message'`。

  后一种形式不是合法的Python 3语法。

  使用括号的形式还意味着，当异常参数很长或包含字符串格式时，由于包含括号，因此不需要使用行继续符。

- 捕获异常时，请尽可能提及特定的异常，而不要使用裸`except:`子句。

  例如，使用：

  ```python
  try:
      import platform_specific_module
  except ImportError:
      platform_specific_module = None
  ```

  裸露的`except:`子句将捕获SystemExit和KeyboardInterrupt异常，这使得使用Control-C中断程序更加困难，并且可以掩盖其他问题。如果要捕获所有表明程序错误的异常，请使用`except Exception:`（“裸露”等效于`except BaseException:`）。

  一个好的经验法则是将裸'except'子句的使用限制为两种情况：

  1. 如果异常处理程序将打印输出或记录回溯；至少用户会意识到发生了错误。
  2. 如果代码需要做一些清理工作，但是让异常向上传播`raise`。`try...finally`可能是处理这种情况的更好方法。

- 将捕获的异常绑定到名称时，最好使用Python 2.6中添加的显式名称绑定语法：

  ```python
  try:
      process_data()
  except Exception as exc:
      raise DataProcessingFailedError(str(exc))
  ```

  这是Python 3中唯一支持的语法，并且避免了与较早的基于逗号的语法相关的歧义问题。

- 捕获操作系统错误时，与`errno`值的自省相比，更喜欢Python 3.3中引入的显式异常层次结构。

- 此外，对于所有try / except子句，请将`try`子句限制为所需的绝对最小数量的代码。同样，这避免了掩盖错误。

  Yes：

  ```python
  try:
      value = collection[key]
  except KeyError:
      return key_not_found(key)
  else:
      return handle_value(value)
  ```

  No：

  ```python
  try:
      # Too broad!
      return handle_value(collection[key])
  except KeyError:
      # Will also catch KeyError raised by handle_value()
      return key_not_found(key)
  ```

- 当资源位于代码的特定部分本地时，请使用一条`with`语句以确保在使用后迅速，可靠地对其进行清理。try / finally语句也是可以接受的。

- 每当他们执行除获取和释放资源以外的其他操作时，都应通过单独的函数或方法来调用上下文管理器。例如：

  Yes：

  ```python
  with conn.begin_transaction():
      do_stuff_in_transaction(conn)
  ```

  No：

  ```python
  with conn:
      do_stuff_in_transaction(conn)
  ```

  后面的示例没有提供任何信息来指示`__enter__`和`__exit__`方法在事务处理后关闭连接以外的操作。在这种情况下，暴露很重要。

- 在返回语句中保持一致。函数中的所有return语句应该返回一个表达式，或者都不返回。如果任何return语句返回一个表达式，则不返回任何值的任何return语句`return None`都应将其显式声明为，并且在函数末尾（如果可以到达）应存在一个显式return语句。

  Yes：

  ```python
  def foo(x):
      if x >= 0:
          return math.sqrt(x)
      else:
          return None
  
  def bar(x):
      if x < 0:
          return None
      return math.sqrt(x)
  ```

  No：

  ```python
  def foo(x):
      if x >= 0:
          return math.sqrt(x)
  
  def bar(x):
      if x < 0:
          return
      return math.sqrt(x)
  ```

- 使用字符串方法而不是字符串模块。

  字符串方法总是更快，并且与unicode字符串共享相同的API。如果需要与2.0以上的Python向后兼容，请覆盖此规则。

- 使用`''.startswith()`和`''.endswith()`代替字符串切片来检查前缀或后缀。

  `startswith()`而且`endswith()`更干净，更不容易出错。例如：

  Yes：

  ```python
  if foo.startswith('bar'):
  ```

  No：

  ```python
  if foo[:3] == 'bar':
  ```

- 对象类型比较应始终使用`isinstance()`而不是直接比较类型：

  Yes：

  ```python
  if isinstance(obj, int):
  ```

  No：

  ```python
  if type(obj) is type(1):
  ```

  在检查对象是否为字符串时，请记住它也可能是unicode字符串！在Python 2中，str和unicode具有一个公共基类basestring，因此您可以执行以下操作：

  ```python
  if isinstance(obj, basestring):
  ```

  请注意，在Python 3中，`unicode`它`basestring`不再存在（只有`str`），并且bytes对象不再是字符串的一种（而是整数序列）

- 对于序列（字符串，列表，元组），请使用空序列为假的事实：

  Yes：

  ```python
  if not seq:
  if seq:
  ```

  No：

  ```python
  if len(seq):
  if not len(seq):
  ```

- 不要写依赖大量尾随空格的字符串文字。这种尾随的空格在视觉上是无法区分的，某些编辑器（或更近期的reindent.py）将对其进行修剪。

- 不要使用`==`以下方法将布尔值与True或False进行比较：

  Yes：

  ```python
  if greeting:
  ```

  No：

  ```python
  if greeting == True:
  ```

  Worse：

  ```python
  if greeting is True:
  ```



# 参考

[PEP8](https://pep8.org/)

