
import re

__version__ = '0.95b'

def convert_text(in_body):
    '''
    You can call convert_text directly to convert shpaml markup
    to HTML markup.
    '''
    return convert_shpaml_tree(in_body)

PASS_SYNTAX = 'PASS'
FLUSH_LEFT_SYNTAX = '|| '
FLUSH_LEFT_EMPTY_LINE = '||'
DOT_FOR_CLASSES = '.'
TAG_WHITESPACE_ATTRS = re.compile('(\S+)(\s*?)(.*)')
TAG_AND_ID = re.compile('(.*)#(.*)')
DIV_SHORTCUT = re.compile('[\.#]')

def AUTO_QUOTE_ATTRIBUTES(attrs):
    return re.sub(r'(\S+)=(?=[^"])(\S*)',r'\1="\2"',attrs)

def syntax(regex):
    def wrap(f):
        f.regex = re.compile(regex)
        return f
    return wrap

@syntax('(\s*)(.*)')
def INDENT(m):
    prefix, line = m.groups()
    line = line.rstrip()
    if line == '':
        prefix = ''
    return prefix, line

@syntax('^([<{]\S.*)')
def RAW_HTML(m):
    return m.group(1).rstrip()

@syntax('^\| (.*)')
def TEXT(m):
    return m.group(1).rstrip()

@syntax('(.*?) > (.*)')
def OUTER_CLOSING_TAG(m):
    tag, text = m.groups()
    text = convert_line(text)
    return enclose_tag(tag, text)

@syntax('(.*?) \| (.*)')
def TEXT_ENCLOSING_TAG(m):
    tag, text = m.groups()
    return enclose_tag(tag, text)

@syntax('> (.*)')
def SELF_CLOSING_TAG(m):
    tag = m.group(1).strip()
    return '<%s />' % apply_jquery(tag)[0]

@syntax('(.*)')
def RAW_TEXT(m):
    return m.group(1).rstrip()

LINE_METHODS = [
        RAW_HTML,
        TEXT,
        OUTER_CLOSING_TAG,
        TEXT_ENCLOSING_TAG,
        SELF_CLOSING_TAG,
        RAW_TEXT,
        ]


def convert_shpaml_tree(in_body):
    return indent(in_body,
            branch_method=html_block_tag,
            leaf_method=convert_line,
            pass_syntax=PASS_SYNTAX,
            flush_left_syntax=FLUSH_LEFT_SYNTAX,
            flush_left_empty_line=FLUSH_LEFT_EMPTY_LINE,
            indentation_method=find_indentation)

def html_block_tag(output, block, recurse):
    append = output.append
    prefix, tag = block[0]
    if RAW_HTML.regex.match(tag):
        append(prefix + tag)
        recurse(block[1:])
    else:
        start_tag, end_tag = apply_jquery_sugar(tag)
        append(prefix + start_tag)
        recurse(block[1:])
        append(prefix + end_tag)

def convert_line(line):
    prefix, line = find_indentation(line.strip())
    for method in LINE_METHODS:
        m = method.regex.match(line)
        if m:
            return prefix + method(m)

def apply_jquery_sugar(markup):
    if DIV_SHORTCUT.match(markup):
        markup = 'div' + markup
    start_tag, tag = apply_jquery(markup)
    return ('<%s>' % start_tag, '</%s>' % tag)

def apply_jquery(markup):
    tag, whitespace, attrs = TAG_WHITESPACE_ATTRS.match(markup).groups()
    tag, id_ = tag_and_id(tag)
    tag, classes = tag_and_classes(tag)
    attrs = AUTO_QUOTE_ATTRIBUTES(attrs)
    if classes:
        attrs += ' class="%s"' % classes
    if id_:
        attrs += ' id="%s"' % id_
    start_tag = tag + whitespace + attrs
    return start_tag, tag

def tag_and_id(tag):
    m = TAG_AND_ID.match(tag)
    if m:
        return m.groups()
    else:
        return tag, None

def tag_and_classes(tag):
    frags = tag.split(DOT_FOR_CLASSES)
    tag = frags[0]
    classes = ' '.join(frags[1:])
    return tag, classes

def enclose_tag(tag, text):
    start_tag, end_tag = apply_jquery_sugar(tag)
    return start_tag + text + end_tag

def find_indentation(line):
    return INDENT(INDENT.regex.match(line))

############ Generic indentation stuff follows

def get_indented_block(prefix_lines):
    prefix, line = prefix_lines[0]
    len_prefix = len(prefix)
    i = 1
    while i < len(prefix_lines):
        new_prefix, line = prefix_lines[i]
        if line and len(new_prefix) <= len_prefix:
            break
        i += 1
    while i-1 > 0 and prefix_lines[i-1][1] == '':
        i -= 1
    return i

def indent(text,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block = get_indented_block,
            ):
    text = text.rstrip()
    lines = text.split('\n')
    output = []
    indent_lines(
            lines,
            output,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block = get_indented_block,
            )
    return '\n'.join(output) + '\n'

def indent_lines(lines,
            output,
            branch_method,
            leaf_method,
            pass_syntax,
            flush_left_syntax,
            flush_left_empty_line,
            indentation_method,
            get_block,
            ):
    append = output.append
    def recurse(prefix_lines):
        while prefix_lines:
            prefix, line = prefix_lines[0]
            if line == '':
                prefix_lines.pop(0)
                append('')
            else:
                block_size = get_block(prefix_lines)
                if block_size == 1:
                    prefix_lines.pop(0)
                    if line == pass_syntax:
                        pass
                    elif line.startswith(flush_left_syntax):
                        append(line[len(flush_left_syntax):])
                    elif line.startswith(flush_left_empty_line):
                        append('')
                    else:
                        append(prefix + leaf_method(line))
                else:
                    block = prefix_lines[:block_size]
                    prefix_lines = prefix_lines[block_size:]
                    branch_method(output, block, recurse)
        return
    prefix_lines = map(indentation_method, lines)
    recurse(prefix_lines)

if __name__ == "__main__":
    # if file name is given convert file, else convert stdin
    import sys
    if len(sys.argv) == 2:
        shpaml_text = open(sys.argv[1]).read()
    else:
        shpaml_text = sys.stdin.read()
    sys.stdout.write(convert_text(shpaml_text))
