import unittest
import logging

from textwrap import dedent

from tkmilan import model
from tkmilan import parser


logger = logging.getLogger(__name__)


class Test_LTML(unittest.TestCase):
    # # For copy-paste under "result"
    # print('')
    # print('golden = [')
    # for cmd in result:
    #     print(f'    {cmd},')
    # print(']')
    # print('')
    def test_simple(self):
        html_string = dedent('''\
            Text<a>Link</a>More Text
            Line Break above<a href="clean">Clean Link</a>S1<span>S2</span>S3
        ''')
        golden = [
            model.TextElement_span(text='Text'),
            model.TextElement_span(text='Link', tag='a', tags=['a::0']),
            model.TextElement_span(text='More Text\nLine Break above'),
            model.TextElement_span(text='Clean Link', tag='a', tags=['a-clean', 'a::1']),
            model.TextElement_span(text='S1'),
            model.TextElement_span(text='S2', tag='span', tags=['span::0']),
            model.TextElement_span(text='S3\n'),
        ]

        result = parser.parse_LTML(html_string)
        self.assertListEqual(result, golden)

    def test_data(self):
        html_string = dedent('''<span data-one="1" data-two="2">Text</span>''')
        golden = [
            model.TextElement_span(text='Text', tag='span', tags=['span::0'], data={
                'one': '1',
                'two': '2',
            }),
        ]

        result = parser.parse_LTML(html_string)
        self.assertListEqual(result, golden)

    def test_br(self):
        html_string = dedent('''Text<br/>Text''')
        golden = [
            model.TextElement_span(text='Text'),
            model.TextElement_br(),
            model.TextElement_span(text='Text'),
        ]
        result = parser.parse_LTML(html_string)

        self.assertListEqual(result, golden)


if __name__ == '__main__':
    import sys
    logs_lvl = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=logs_lvl, format='%(levelname)5.5s:%(funcName)s: %(message)s', stream=sys.stderr)
    unittest.main()
