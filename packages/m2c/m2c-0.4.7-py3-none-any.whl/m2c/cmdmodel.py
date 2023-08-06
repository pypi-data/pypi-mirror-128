
#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2020-09-11
import os

from .conf import *
from .helper import *

CMD_TPL = '''
package cmd

import (
	"flag"
	"fmt"
)

func init() {{
	appcmd.AddCmd("{name}", "{desc}", {name}Cmd)
}}

func {name}Cmd(args []string) (err error) {{
	var (
        {vars}
	)

    {params}

	err = param.Parse(args)
	if err != nil {{
		return
	}}

	if len(args) == 0 {{ // show help
		param.Usage()
		return
	}}

    fmt.Println("cmd: {name} running...")
	// write your code blow

	return
}}
'''


# Api model to code
'''
root cmd
CmdName # comment as cmd description
    param0 fieldType <defaultValue> # comment as param description, fieldType in [bool, str, int, float], option default value
    param1 fieldType <defaultValue> # comment as param description, fieldType in [bool, str, int, float], option default value
    param2 fieldType <defaultValue> # comment as param description, fieldType in [bool, str, int, float], option default value
'''

class CmdParam(object):
    def __init__(self, lineno, line, name, typ, defval, comment):
        self.lineno = lineno
        self.line = line
        self.name = name
        self.typ = typ
        self.defval = defval
        self.comment = comment

    @classmethod
    def fromLine(cls, lineno, line):
        if '#' in line:
            itemsline, comment = line.split('#', 1)
            items = itemsline.split()
        else:
            comment = ''
            items = line.split()
        assert_error(len(items) >= 2, '无效的参数定义', lineno, line)
        name, typ = items[0], items[1]
        assert_error(is_valid_var(name), '无效的参数名定义', lineno, line)
        defval = None
        if len(items) > 2:
            defval = items[2]

        if typ in TYPEMAPPING:
            typ = TYPEMAPPING[typ]
        p = cls(lineno, line, name, typ, defval, comment.strip())
        return p
    
    def __repr__(self):
        return '%s %s %s # %s\n' % (self.name, self.typ, self.defval, self.comment)

    def varcode(self):
        line = '%s %s // %s' % (self.name, self.typ, self.comment)
        return line

    def paramcode(self):
        defval = self.defval
        if self.typ == 'string':
            if defval is None:
                defval = '""'
            else:
                defval = '"%s"' % self.defval
        elif self.typ == 'bool':
            if defval is None:
                defval = false
        else:
            if defval is None:
                defval = 0

        line = 'param.%sVar(&%s, "%s", %s, "%s")' % (upperFirst(self.typ), self.name, self.name, defval, self.comment)
        return line

class CmdDef(object):
    def __init__(self, lineno, line, name, comment):
        self.lineno = lineno
        self.line = line
        self.name = name
        self.comment = comment
        self.cmdParams = []

    def __repr__(self):
        txt = '%s # %s\n' % (self.name, self.comment)
        for param in self.cmdParams:
            isinstance(param, CmdParam)
            txt += ' ' * TAB_WIDTH * 2 + str(param)
        return txt

    def addCmdParam(self, cmdParam):
        assert isinstance(cmdParam, CmdParam)
        self.cmdParams.append(cmdParam)

    def code(self):
        vars = ''
        params = '''
        param := flag.NewFlagSet("{name}", flag.ExitOnError)\n
        '''.format(name=self.name)

        for param in self.cmdParams:
            vars += '%s' % param.varcode()
            params += '%s' % param.paramcode()
        code = CMD_TPL.format(name=self.name, desc=self.comment, vars=vars, params=params)
        return code

    @classmethod
    def fromLine(cls, lineno, line):
        if '#' in line:
            itemsline, comment = line.split('#', 1)
            items = itemsline.split()
        else:
            comment = ''
            items = line.split()
        assert_error(len(items) >= 1, '无效的参数定义', lineno, line)
        name = items[0]
        assert_error(is_valid_var(name), '无效的参数名定义', lineno, line)
        p = cls(lineno, line, name, comment.strip())
        return p

class CmdModel(object):
    def __init__(self, root, cmds):
        self.root = root
        self.cmds = cmds

    def __repr__(self):
        txt = 'root cmd\n'
        for cmd in self.cmds:
            isinstance(cmd, CmdDef)
            txt += str(cmd)
        return txt

    def genCmdCode(self):
        for cmd in self.cmds:
            code = cmd.code()
            cmdPath = '%s/cmd/cmd_%s.go' % (MOD, cmd.name)
            if os.path.exists(cmdPath):
                print(Color.red('%s already exists! skip gen code' % cmdPath))
                continue
            writeCode(cmdPath, code)
        os.system('gofmt -w %s/cmd' % MOD)

    @classmethod
    def fromLines(cls, lines):
        lineno = 1
        root = lines[0].strip()
        assert_error(is_valid_var(root[0]), '开头必须是有效字母', lineno, root)
        items = root.split(' ')
        assert_error(len(items) >= 2, '无效的cmdmodel', lineno, root)
        assert_error(items[0] == 'root', '无效的cmdmodel', lineno, root)
        PREFIX = items[1]
        assert_error(PREFIX == 'cmd', '关键字必须是有效字母', lineno, root)

        cmds = []
        currentCmd = None

        for line in lines[1:]:
            lineno += 1

            if not line.strip():
                continue

            width = len(line) - len(line.lstrip())
            assert_error(width % TAB_WIDTH == 0, '宽带不是%s的倍数' % TAB_WIDTH, lineno, line)
            deep = int(width / TAB_WIDTH)
            assert_error(deep <= 2, '深度不能超过2', lineno, line)

            line = line.strip()
            if line.startswith('#'):
                continue
            # cmd
            if deep == 0:
                currentCmd = CmdDef.fromLine(lineno, line)
                cmds.append(currentCmd)
            # param
            elif deep == 1:
                assert currentCmd
                currentParam = CmdParam.fromLine(lineno, line)
                currentCmd.addCmdParam(currentParam)

        return cls(root, cmds)


if __name__ == "__main__":
    text = '''root cmd
hello # 支持4个类型, 字符串, 整数, 布尔, 浮点 -> name, desc
    name str # 姓名, 必须, 字符串 -> arg, desc
    age int 18 # 年纪, 可选, 默认18, 数字
    isboy bool false # 是否男孩, 默认false
    height float # 身高, 必须
createIndex
    '''
    cm = CmdModle.fromLines(text.splitlines())
    print(cm)
    cm.genCmdCode()
