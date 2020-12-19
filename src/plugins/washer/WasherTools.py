# -*- coding: utf-8 -*-
# create by yihui 16:08 20/5/11

"""
数据清洗器
"""
import re

TAG_MAPPER = [
    {
        "s": "<div",
        "e": '</div>',
        'r': ''
    },
    {
        "s": '<p',
        "e": '</p>',
        'r': '\n'
    },
    {
        "s": '<b',
        "e": '</b>',
        'r': ''
    },
    {
        "s": '<i',
        "e": '</i>',
        'r': ''
    },
    {
        "s": '<span',
        "e": '</span>',
        'r': ''
    },
    {
        "s": '<section',
        "e": '</section>',
        'r': ''
    },
    {
        "s": '<txt',
        "e": '</txt>',
        'r': ''
    },
    {
        "s": "<font",
        "e": '</font>',
        'r': ''
    },
    {
        "s": '<bold',
        "e": '</bold>',
        'r': ''
    },
    {
        "s": "<a",
        "e": "</a>",
        'r': ''
    },
    {
        "s": "<img",
        "e": "</img>",
        'r': ''
    },
    {
        's': '<br>',
        'e': '<br/>',
        'r': '\n'
    },
    {
        's': '<br>',
        'e': '<br>',
        'r': '\n'
    },
    {
        's': '<em',
        'e': '</em>',
        'r': ''
    },
    {
        's': '<hr/>',
        'e': '<hr/>',
        'r': ''
    },
    {
        's': '<strong',
        'e': '</strong>',
        'r': ''
    },
    {
        's': '<table',
        'e': '</table>',
        'r': ''
    },
    {
        's': '<tbody',
        'e': '</tbody>',
        'r': ''
    },
    {
        's': '<tr',
        'e': '</tr>',
        'r': ''
    },
    {
        's': '<td',
        'e': '</td>',
        'r': ''
    },
    {
        's': '<blockquote',
        'e': '</blockquote>',
        'r': ''
    },
    {
        's': '<sup',
        'e': '</sup>',
        'r': ''
    },
    {
        's': '<h1',
        'e': '</h1>',
        'r': ''
    },
    {
        's': '<h2',
        'e': '</h2>',
        'r': ''
    },
    {
        's': '<h3',
        'e': '</h3>',
        'r': ''
    },
    {
        's': '<h4',
        'e': '</h4>',
        'r': ''
    },
    {
        's': '<h5',
        'e': '</h5>',
        'r': ''
    },
    {
        's': '<center',
        'e': '</center>',
        'r': ''
    },
    {
        's': '<!--',
        'e': '-->',
        'r': ''
    }
]


class WasherTools:
    @staticmethod
    def remove_http(content: str):
        """
        替换正则替换
        :param content:
        :return:
        """
        pattern = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|(www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)', re.I)
        content = re.sub(pattern, '', content)
        return content

    @staticmethod
    def english_washer(context: str, remove_line_rule=[]):
        ans = WasherTools.wash_context(context, remove_line_rule)
        return ans.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace("&amp;", "&").replace(
            "&nbsp;", " ")

    @staticmethod
    def wash_context(context: str, remove_line_rule=[]):
        """
        清洗多余的分行，每段固定前置两个空格
        :param context:
        :param remove_line_rule: 如果某一行，包含这里的删除规则，则直接过滤掉；主要是为了清洗内容中的广告
        :return:
        """
        # 删除注释的内容
        context = WasherTools.remove_comment_txt(context)
        for tag in TAG_MAPPER:
            context = context.replace(tag['e'], tag['r'])

        lines = context.splitlines()
        result = []
        for line in lines:
            sub = line.strip()
            if not sub:
                continue

            if washer_tools.__ignore_line(sub, remove_line_rule):
                continue

            # 删除标签
            sub = WasherTools.clear_html_tag(sub)
            if not sub:
                continue

            result.append(sub)

        novel = "\n".join(result)
        # 替换域名
        return WasherTools.remove_http(novel).strip()

    @staticmethod
    def remove_comment_txt(content: str):
        start = content.find('<!--')
        if start > 0:
            end = content.find('-->', start)
            return WasherTools.remove_comment_txt(content[:start] + content[end + 3:])
        else:
            return content

    @staticmethod
    def __ignore_line(line, remove_line_rule):
        if not remove_line_rule:
            return False

        for rule in remove_line_rule:
            if line.find(rule) >= 0:
                return True

        return False

    @staticmethod
    def clear_html_tag(line: str):
        for tag in TAG_MAPPER:
            while True:
                sub = washer_tools.check_tag(line, tag)
                if sub != line:
                    # 命中之后，再来一次，确保所有的都干掉了
                    line = sub
                else:
                    break

        return line.strip()

    @staticmethod
    def check_tag(line, tag):
        start = line.find(tag['s'])
        if start >= 0:
            end = line.find('>', start)
            if end > 0:
                line = line[0:start] + line[end + 1:]
                return line

        return line


washer_tools = WasherTools()
